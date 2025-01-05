import io
import os

import discord
from discord.ext import commands

from cogs import LogCog
from service import pictureService, premiumService, localeService


class PremiumCog(commands.Cog):

    def __init__(self, bot):
        LogCog.logSystem('Premium cog loaded')
        self.bot = bot

    @commands.command(aliases=['patreon'])
    async def premium(self, ctx, *args):
        if premiumService.is_premium(ctx.author.id):
            await ctx.send(localeService.getLocale('you-are-premium', ctx.author.id))
        else:
            await ctx.send(localeService.getLocale('buy-premium', ctx.author.id))

