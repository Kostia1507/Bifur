from datetime import datetime

import config
from cogs import LogCog
from cogs.AdminCog import AdminCog
from cogs.CalcCog import CalcCog
from cogs.ChatCog import ChatCog
from cogs.GamesCog import GamesCog
from cogs.HelpCog import HelpCog
from cogs.LangCog import LangCog
from cogs.MusicCog import MusicCog
from cogs.RadioCog import RadioCog
from cogs.TranslatorCog import TranslatorCog
from cogs.chatGPTCog import ChatGPTCog
from discordModels.views.ReportView import ReportView
from service import cooldownService, chatGPTService, pagedMessagesService
from utils import commandUtils, botUtils

import discord
from discord import HTTPException
from discord.ext import commands, tasks
from discord.ext.commands import CommandNotFound

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.reactions = True


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
    await bot.add_cog(LangCog(bot))
    print("Bot started")


@bot.event
async def on_message(message):
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

    await bot.process_commands(message)


bot.run(config.token, reconnect=True)
