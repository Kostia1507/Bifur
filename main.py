import asyncio
import logging
from datetime import datetime

import config
from cogs import LogCog
from cogs.AdminCog import AdminCog
from cogs.CalcCog import CalcCog
from cogs.ChatCog import ChatCog
from cogs.CurrencyCog import CurrencyCog
from cogs.GamesCog import GamesCog
from cogs.GifCog import GifCog
from cogs.HelpCog import HelpCog
from cogs.LangCog import LangCog
from cogs.MusicCog import MusicCog
from cogs.PictureCog import PictureCog
from cogs.PremiumCog import PremiumCog
from cogs.RadioCog import RadioCog
from cogs.ServerAdministrationCog import ServerAdministrationCog
from cogs.ServerRoleManagerCog import ServerRoleManagerCog
from cogs.TranslatorCog import TranslatorCog
from cogs.WeatherCog import WeatherCog
from cogs.chatGPTCog import ChatGPTCog
from discordModels.views.ReportView import ReportView
from service import cooldownService, chatGPTService, pagedMessagesService, customPrefixService, autoReactionService, \
    ignoreService
from utils import commandUtils, botUtils

import discord
from discord import HTTPException
from discord.ext import commands
from discord.ext.commands import CommandNotFound, MissingRequiredArgument, MissingPermissions

from webpage.WebHandler import start_aiohttp_server

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.reactions = True

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    datefmt="%d-%m %H:%M:%S",
)

discord_logger = logging.getLogger("discord")
discord_logger.setLevel(logging.INFO)


class BifurBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=config.prefix,
                         intents=intents,
                         case_insensitive=True,
                         strip_after_prefix=True,
                         owner_ids=[418040057019236353])

    async def setup_hook(self) -> None:
        # Register the persistent view for listening here.
        self.add_view(ReportView(self))


bot = BifurBot()
commandUtils.bot = bot


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        await ctx.message.add_reaction("❔")
        LogCog.logDebug(f'Command not exists {ctx.message.content}')
    if isinstance(error, MissingRequiredArgument):
        await ctx.message.add_reaction("❗")
    if isinstance(error, MissingPermissions):
        return
    raise error


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.CustomActivity(name=">langs || >help"))
    bot.remove_command("help")
    LogCog.logSystem("Bot started")
    botUtils.prepareAtStart()
    await bot.add_cog(HelpCog(bot))
    await bot.add_cog(AdminCog(bot))
    await bot.add_cog(CalcCog(bot))
    await bot.add_cog(ChatGPTCog(bot))
    await bot.add_cog(ChatCog(bot))
    await bot.add_cog(GamesCog(bot))
    await bot.add_cog(LogCog.LogCog(bot))
    await bot.add_cog(TranslatorCog(bot))
    await bot.add_cog(MusicCog(bot))
    await bot.add_cog(RadioCog(bot))
    await bot.add_cog(PictureCog(bot))
    await bot.add_cog(PremiumCog(bot))
    await bot.add_cog(GifCog(bot))
    await bot.add_cog(ServerRoleManagerCog(bot))
    await bot.add_cog(LangCog(bot))
    await bot.add_cog(CurrencyCog(bot))
    await bot.add_cog(WeatherCog(bot))
    await bot.add_cog(ServerAdministrationCog(bot))
    print(f"Bot started as {bot.user.name}")
    await customPrefixService.init()


@bot.event
async def on_message(message):
    # check auto-reactions
    reactions = autoReactionService.checkForReaction(message.channel.id)
    for r in reactions:
        try:
            await message.add_reaction(r)
        except HTTPException:
            LogCog.logError(f'Error in auto-reactions. Channel:{message.channel.id}:{message.channel.name}')

    if message.author == bot.user:
        return
    text = message.content.strip()

    # ChatGPT
    if text.startswith(f'<@{bot.user.id}>'):
        if cooldownService.isInCooldown(message.author.id):
            LogCog.logSystem(f'{str(message.author)} cooldown!')
            await message.add_reaction('⏰')
            return
        else:
            async with message.channel.typing():
                await message.add_reaction('👋')
                cooldownService.setSpecialCooldown(message.author.id)
                LogCog.logSystem(f'Send message to openai {datetime.now()}: {message.author} - {message.content}')
                title = message.content[21:]
                if len(title) > 100:
                    title = ""
                answer = await chatGPTService.ask(text[len(f'<@{bot.user.id}>'):len(text)], message.author.id)
                pagedMsg = pagedMessagesService.initPagedMessage(bot, title, answer)
                embed = discord.Embed(title=pagedMsg.title, description=pagedMsg.pages[0])
                embed.set_footer(text=f'Page 1 of {len(pagedMsg.pages)}')
                await message.channel.send(embed=embed, view=pagedMsg.view)
                cooldownService.removeCooldown(message.author.id)

    # custom prefixes
    if message.channel.guild is not None:
        customPrefix = customPrefixService.getPrefix(message.channel.guild.id)
        if customPrefix is not None:
            if text.startswith(customPrefix):
                text = f'{config.prefix}{text[len(customPrefix):len(text)]}'
                message.content = text
            elif text.startswith(config.prefix):
                return

    if message.channel.id in ignoreService.ignoredChannels and not text.startswith(f'{bot.command_prefix}ignore'):
        return

    # check command
    if text.startswith(bot.command_prefix):
        # check is user in cooldown
        if cooldownService.isInCooldown(message.author.id):
            LogCog.logSystem(f'{str(message.author)} cooldown!')
            await message.add_reaction('⏰')
            return
        else:
            # run as user command
            if text.startswith(f'{bot.command_prefix}runas') and message.author.id in config.owners:
                args = text.split(" ")
                message.author = await bot.fetch_user(int(args[1]))
                args = args[2:]
                message.content = bot.command_prefix + " ".join(args)
            cooldownService.setCooldown(message.author.id)
            LogCog.logInfo(f'{str(message.author)}:{text}', message.author.name)
            await bot.process_commands(message)

async def start_app():
    await asyncio.gather(
        start_aiohttp_server(bot),
        bot.start(config.token, reconnect=True)
    )

asyncio.run(start_app())