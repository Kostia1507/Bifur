import os
from datetime import datetime

import discord
from discord import Embed, Colour
from discord.ext import commands, tasks

import config

delayedLogs = []

colors = {
    "info": "#00ccff",
    "debug": "#ffcc00",
    "system": "#78fb5c",
    "error": "#b20000"
}


class MyLog:

    def __init__(self, log_type, author, content):
        self.content = content
        self.logType = log_type
        self.author = author

    def prepareToSend(self):
        embed = Embed(description=str(datetime.now()) + ":" + self.content, colour=Colour.from_str(colors[self.logType]))
        embed.set_footer(text=self.author)
        return embed


def addLog(text):
    log = MyLog("info", "system", text)
    delayedLogs.append(log)


def logInfo(text, author):
    log = MyLog("info", author, text)
    delayedLogs.append(log)


def logError(text):
    log = MyLog("error", "system", text)
    delayedLogs.append(log)


def logDebug(text):
    log = MyLog("debug", "system", text)
    delayedLogs.append(log)


def logSystem(text):
    log = MyLog("system", "system", text)
    delayedLogs.append(log)


class LogCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.log_channel = bot.get_channel(config.log_channel)
        delayedLogs.append(MyLog("system", "system", "Log cog loaded"))
        self.checkForLogs.start()

    async def sendLog(self, log):
        if len(log.content) > 4000:
            with open('templogfile.txt', "w") as file:
                file.write(log.author + "\n\n" + log.content)
            with open('templogfile.txt', "rb") as file:
                await self.log_channel.send(file=discord.File(file, 'templogfile.txt'))
            os.remove('templogfile.txt')
        else:
            await self.log_channel.send(embed=log.prepareToSend())

    @tasks.loop(seconds=5)
    async def checkForLogs(self):
        try:
            loop_list = delayedLogs.copy()
            delayedLogs.clear()
            for log in loop_list:
                await self.sendLog(log)
        except Exception as e:
            logError("Exception on checkForLogs " + str(e))
