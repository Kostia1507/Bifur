import discord
from asyncpg import Record
from discord.ext import commands
from discord.utils import remove_markdown

from cogs import LogCog
from service import premiumService, localeService, pagedMessagesService
from utils import commandUtils


class PremiumCog(commands.Cog):

    def __init__(self, bot):
        LogCog.logSystem('Premium cog loaded')
        self.bot = bot

    @commands.command(aliases=['patreon'])
    async def premium(self, ctx, *args):
        if await premiumService.is_premium(ctx.author.id):
            await ctx.send(await localeService.getLocale('you-are-premium', ctx.author.id))
        else:
            await ctx.send(await localeService.getLocale('buy-premium', ctx.author.id))

    @commands.command()
    @commands.check(commandUtils.is_owner)
    async def setpremium(self, ctx, user: discord.User):
        if await premiumService.add_premium(user.id):
            await ctx.message.add_reaction('✅')
        else:
            await ctx.message.add_reaction('❌')

    @commands.command()
    @commands.check(commandUtils.is_owner)
    async def delpremium(self, ctx, user: discord.User):
        if await premiumService.delete_premium(user.id):
            await ctx.message.add_reaction('✅')
        else:
            await ctx.message.add_reaction('❌')

    @commands.command()
    @commands.check(commandUtils.is_owner)
    async def listpremium(self, ctx):
        ids = await premiumService.get_all_premiums()
        if ids is None or len(ids) == 0:
            await ctx.send("List of premium is empty")
        else:
            res = ""
            for premium_id in ids:
                user_id = premium_id
                if isinstance(premium_id, tuple) or isinstance(premium_id, Record):
                    user_id = premium_id[0]
                try:
                    user = await self.bot.fetch_user(user_id)
                    res += f"{remove_markdown(user.name)}\n"
                except discord.errors.NotFound:
                    res += "Discord NotFound\n"
            pagedMsg = pagedMessagesService.initPagedMessage(self.bot, "Premium users", res)
            await ctx.send(view=pagedMsg.view)
