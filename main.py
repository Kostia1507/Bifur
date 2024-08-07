import config
from cogs import LogCog
from cogs.CalcCog import CalcCog
from cogs.TranslatorCog import TranslatorCog
from utils import commandUtils

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
        pass
        # Register the persistent view for listening here.
        # self.add_view()


bot = BifurBot()
commandUtils.bot = bot


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.CustomActivity(name=">langs || >help"))
    bot.remove_command("help")
    LogCog.logSystem("Bot started")
    await bot.add_cog(CalcCog(bot))
    await bot.add_cog(LogCog.LogCog(bot))
    await bot.add_cog(TranslatorCog(bot))
    print("Bot started")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)


bot.run(config.token, reconnect=True)
