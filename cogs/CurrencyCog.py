from discord.ext import commands, tasks

import config
from cogs import LogCog
from service.localeService import getLocale

from service import currencyService


class CurrencyCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        # Requests to update currency rates are limited!
        if config.release:
            self.getCurrency.start()
        LogCog.logSystem("CurrencyCog started")

    @commands.command()
    async def currency(self, ctx, value: float, fromCurrency: str, *args: str):
        try:
            fromCurrency = fromCurrency.upper()
            res = value / currencyService.currency[fromCurrency]
        except KeyError:
            await ctx.send(getLocale("wrong", ctx.author.id) + " " + str(fromCurrency))
            return 0
        try:
            output = f'{value}{fromCurrency}'
            for loop in args:
                toCurrency = loop.upper()
                currentRes = res * currencyService.currency[toCurrency]
                output = f'{output}={round(currentRes, 4)}{toCurrency}'
            await ctx.send(output)
        except KeyError:
            await ctx.send(getLocale("wrong", ctx.author.id) + " " + str(toCurrency))
            return 0

    @tasks.loop(hours=12)
    async def getCurrency(self):
        LogCog.logSystem("Update currency rates")
        await currencyService.updateCurrency()
