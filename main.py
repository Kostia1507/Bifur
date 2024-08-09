import config
from cogs import LogCog
from cogs.AdminCog import AdminCog
from cogs.CalcCog import CalcCog
from cogs.ChatCog import ChatCog
from cogs.HelpCog import HelpCog
from cogs.MusicCog import MusicCog
from cogs.RadioCog import RadioCog
from cogs.TranslatorCog import TranslatorCog
from discordModels.views.ReportView import ReportView
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
    await bot.add_cog(ChatCog(bot))
    await bot.add_cog(LogCog.LogCog(bot))
    await bot.add_cog(TranslatorCog(bot))
    await bot.add_cog(MusicCog(bot))
    await bot.add_cog(RadioCog(bot))
    print("Bot started")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)


bot.run(config.token, reconnect=True)
