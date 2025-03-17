import os

import discord
from discord.ext import commands

from cogs import LogCog
from service import RPNCalculator
from service.localeService import getLocale


class CalcCog(commands.Cog):

    def __init__(self, bot):
        LogCog.logSystem('Calc cog loaded')
        self.bot = bot

    @commands.command()
    async def calcd(self, ctx, *args):
        await ctx.send(RPNCalculator.calcd(args[0], args[1], args[2]))

    @commands.command()
    async def calc(self, ctx, *args):
        expression = "".join(args)
        result = RPNCalculator.calculateRPN(RPNCalculator.toPostfix(RPNCalculator.validate(expression)))
        if len(str(result)) < 1980:
            await ctx.send(f'{await getLocale(locale="result", user_id=ctx.author.id)} {result}')
        else:
            with open(f'{ctx.message.id}.txt', "w") as file:
                file.write(str(result))
            with open(f'{ctx.message.id}.txt', "rb") as file:
                await ctx.send(f'{await getLocale(locale="result", user_id=ctx.author.id)} ',
                               file=discord.File(file, f'{ctx.message.id}.txt'))
            os.remove(f'{ctx.message.id}.txt')

    @commands.command()
    async def avg(self, ctx, *args):
        expression = "".join(args)
        result = 0
        loop = expression.split(',')
        for i in loop:
            result += RPNCalculator.calculateRPN(RPNCalculator.toPostfix(RPNCalculator.validate(i)))
        if len(str(result)) < 1980:
            await ctx.send(f'{await getLocale(locale="result", user_id=ctx.author.id)} {result/len(loop)}')
        else:
            with open(f'{ctx.message.id}.txt', "w") as file:
                file.write(str(result/len(loop)))
            with open(f'{ctx.message.id}.txt', "rb") as file:
                await ctx.send(f'{await getLocale(locale="result", user_id=ctx.author.id)} ',
                               file=discord.File(file, f'{ctx.message.id}.txt'))
            os.remove(f'{ctx.message.id}.txt')

    @commands.command()
    async def sum(self, ctx, *args):
        expression = "".join(args)
        result = 0
        loop = expression.split(',')
        for i in loop:
            result += float(i)
        if len(str(result)) < 1980:
            await ctx.send(f'{await getLocale(locale="result", user_id=ctx.author.id)} {result}')
        else:
            with open(f'{ctx.message.id}.txt', "w") as file:
                file.write(str(result))
            with open(f'{ctx.message.id}.txt', "rb") as file:
                await ctx.send(f'{await getLocale(locale="result", user_id=ctx.author.id)} ',
                               file=discord.File(file, f'{ctx.message.id}.txt'))
            os.remove(f'{ctx.message.id}.txt')
