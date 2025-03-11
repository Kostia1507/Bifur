from discord.ext import commands

from service import localeService
from cogs import LogCog


class LangCog(commands.Cog):

    def __init__(self, bot):
        LogCog.logSystem('Lang cog loaded')
        self.bot = bot

    @commands.command()
    async def lang(self, ctx, lang):
        ret = await localeService.setLang(lang=lang, user_id=ctx.author.id)
        await ctx.send(ret)

    @commands.command()
    async def langs(self, ctx):
        languages = ""
        for lang in localeService.langs:
            if lang == 'en':
                languages += f'\n:flag_gb: {lang}'
            else:
                languages += f'\n:flag_{lang}: {lang}'
        await ctx.send(f'Available languages: {languages}\nUse >lang [language] to choose your language')

    @commands.command()
    async def mylang(self, ctx):
        await ctx.send(await localeService.getLocale("lang", ctx.author.id))
