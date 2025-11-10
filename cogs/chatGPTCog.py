import codecs
import os

import discord
from discord.ext import commands

from cogs.HelpCog import ENhelpPages, RUhelpPages, UAhelpPages
from utils import commandUtils
from cogs import LogCog
from service.localeService import getLocale
from service import chatGPTService, localeService, pagedMessagesService


class ChatGPTCog(commands.Cog):

    def __init__(self, bot):
        LogCog.logSystem('ChatGPT cog loaded')
        self.bot = bot

    @commands.command()
    async def chat(self, ctx, *args):
        if len(args) == 0:
            cmd = "help"
        else:
            cmd = args[0]
            args = args[1:]
        if cmd == 'clear' or cmd == 'clean':
            chatGPTService.clean(ctx.author.id)
            await ctx.message.add_reaction('✅')
        elif cmd == 'new':
            chatGPTService.createChatWithSystemMessage(ctx.author.id, " ".join(args))
            await ctx.message.add_reaction('✅')
        elif cmd == 'system':
            await ctx.send(await chatGPTService.getSystemMessage(ctx.author.id))
        elif cmd == 'history':
            history = await chatGPTService.getHistory(ctx.author.id)
            res = ''
            for i in history:
                res += f'{i}\n'
            with codecs.open("history.txt", 'w', "utf-8") as file:
                file.write(res)
            await ctx.send('Ваша історія', file=discord.File('history.txt'))
            os.remove('history.txt')
        elif cmd == 'userhistory' and commandUtils.is_owner(ctx):
            history = await chatGPTService.getHistory(int(args[0]))
            res = ''
            for i in history:
                res += f'{i}\n'
            with codecs.open("history.txt", 'w', "utf-8") as file:
                file.write(res)
            await ctx.send(await getLocale('your-history', ctx.author.id), file=discord.File('history.txt'))
            os.remove('history.txt')
        else:
            locale = await localeService.getUserLang(ctx.author.id)
            if locale == "en":
                pagedMsg = pagedMessagesService.setPagedMessage(self.bot, "Communication", ENhelpPages["Communication"])
            elif locale == "ua":
                pagedMsg = pagedMessagesService.setPagedMessage(self.bot, "Спілкування", UAhelpPages["Спілкування"])
            elif locale == "ru":
                pagedMsg = pagedMessagesService.setPagedMessage(self.bot, "Общение", RUhelpPages["Общение"])
            else:
                pagedMsg = pagedMessagesService.setPagedMessage(self.bot, "Communication", ENhelpPages["Communication"])
            await ctx.send(view=pagedMsg.view)
