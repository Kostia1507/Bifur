import codecs
import os

import discord
from discord.ext import commands

from utils import commandUtils
from cogs import LogCog
from service.localeService import getLocale
from service import chatGPTService


class ChatGPTCog(commands.Cog):

    def __init__(self, bot):
        LogCog.logSystem('ChatGPT cog loaded')
        self.bot = bot

    @commands.command()
    async def chat(self, ctx, cmd, *args):
        if cmd == 'clear' or cmd == 'clean':
            chatGPTService.clean(ctx.author.id)
            await ctx.message.add_reaction('✅')
        elif cmd == 'new':
            chatGPTService.createChatWithSystemMessage(ctx.author.id, " ".join(args))
            await ctx.message.add_reaction('✅')
        elif cmd == 'system':
            await ctx.send(chatGPTService.getSystemMessage(ctx.author.id))
        elif cmd == 'history':
            history = chatGPTService.getHistory(ctx.author.id)
            res = ''
            for i in history:
                res += f'{i}\n'
            with codecs.open("history.txt", 'w', "utf-8") as file:
                file.write(res)
            await ctx.send('Ваша історія', file=discord.File('history.txt'))
            os.remove('history.txt')
        elif cmd == 'userhistory' and commandUtils.is_owner(ctx):
            history = chatGPTService.getHistory(int(args[0]))
            res = ''
            for i in history:
                res += f'{i}\n'
            with codecs.open("history.txt", 'w', "utf-8") as file:
                file.write(res)
            await ctx.send(getLocale('your-history', ctx.author.id), file=discord.File('history.txt'))
            os.remove('history.txt')
