import discord
from discord.ext import commands

from cogs import LogCog
from service.localeService import getLocale
from service.GIFService import GifCreator


class GifCog(commands.Cog):

    def __init__(self, bot):
        LogCog.logSystem('Gif cog loaded')
        self.bot = bot

    @commands.command()
    async def pat(self, ctx, *args):
        url = None
        if len(ctx.message.attachments) > 0:
            url = ctx.message.attachments[0].url
        elif len(ctx.message.mentions) > 0:
            url = ctx.message.mentions[0].avatar.url
        elif len(args) > 0:
            url = args[0]
        if url is not None:
            try:
                patpat_buffer = await GifCreator(image_url=url).create_pat_gif()
                patpat_gif = discord.File(patpat_buffer, filename=f'temp/{ctx.message.id}pat.gif')
                await ctx.send(file=patpat_gif)
            except FileNotFoundError:
                await ctx.send(await getLocale("file-not-found", ctx.author.id))

    @commands.command(aliases=['vibel'])
    async def vibe(self, ctx, *args):
        url = None
        if len(ctx.message.attachments) > 0:
            url = ctx.message.attachments[0].url
        elif len(ctx.message.mentions) > 0:
            url = ctx.message.mentions[0].avatar.url
        elif len(args) > 0:
            url = args[0]
        if url is not None:
            try:
                vibe_buffer = await GifCreator(image_url=url).create_vibe_gif(side='l')
                vibe_gif = discord.File(vibe_buffer, filename=f'temp/{ctx.message.id}vibe.gif')
                await ctx.send(file=vibe_gif)
            except FileNotFoundError:
                await ctx.send(await getLocale("file-not-found", ctx.author.id))

    @commands.command()
    async def viber(self, ctx, *args):
        url = None
        if len(ctx.message.attachments) > 0:
            url = ctx.message.attachments[0].url
        elif len(ctx.message.mentions) > 0:
            url = ctx.message.mentions[0].avatar.url
        elif len(args) > 0:
            url = args[0]
        if url is not None:
            try:
                vibe_buffer = await GifCreator(image_url=url).create_vibe_gif(side='r')
                vibe_gif = discord.File(vibe_buffer, filename=f'temp/{ctx.message.id}vibe.gif')
                await ctx.send(file=vibe_gif)
            except FileNotFoundError:
                await ctx.send(await getLocale("file-not-found", ctx.author.id))

    @commands.command()
    async def slap(self, ctx, *args):
        url = None
        if len(ctx.message.attachments) > 0:
            url = ctx.message.attachments[0].url
        elif len(ctx.message.mentions) > 0:
            url = ctx.message.mentions[0].avatar.url
        elif len(args) > 0:
            url = args[0]
        if url is not None:
            try:
                slap_buffer = await GifCreator(image_url=url).create_slap_gif()
                slap_gif = discord.File(slap_buffer, filename=f'temp/{ctx.message.id}slap.gif')
                await ctx.send(file=slap_gif)
            except FileNotFoundError:
                await ctx.send(await getLocale("file-not-found", ctx.author.id))

    @commands.command()
    async def work(self, ctx, *args):
        url = None
        if len(ctx.message.attachments) > 0:
            url = ctx.message.attachments[0].url
        elif len(ctx.message.mentions) > 0:
            url = ctx.message.mentions[0].avatar.url
        elif len(args) > 0:
            url = args[0]
        if url is not None:
            try:
                work_buffer = await GifCreator(image_url=url).create_work_gif()
                work_gif = discord.File(work_buffer, filename=f'temp/{ctx.message.id}work.gif')
                await ctx.send(file=work_gif)
            except FileNotFoundError:
                await ctx.send(await getLocale("file-not-found", ctx.author.id))

    @commands.command()
    async def hammer(self, ctx, *args):
        url = None
        if len(ctx.message.attachments) > 0:
            url = ctx.message.attachments[0].url
        elif len(ctx.message.mentions) > 0:
            url = ctx.message.mentions[0].avatar.url
        elif len(args) > 0:
            url = args[0]
        if url is not None:
            try:
                hammer_buffer = await GifCreator(image_url=url).create_hammer_gif()
                hammer_gif = discord.File(hammer_buffer, filename=f'temp/{ctx.message.id}hammer.gif')
                await ctx.send(file=hammer_gif)
            except FileNotFoundError:
                await ctx.send(await getLocale("file-not-found", ctx.author.id))

    @commands.command()
    async def bonk(self, ctx, *args):
        url = None
        if len(ctx.message.attachments) > 0:
            url = ctx.message.attachments[0].url
        elif len(ctx.message.mentions) > 0:
            url = ctx.message.mentions[0].avatar.url
        elif len(args) > 0:
            url = args[0]
        if url is not None:
            try:
                bonk_buffer = await GifCreator(image_url=url).create_bonk_gif()
                bonk_gif = discord.File(bonk_buffer, filename=f'temp/{ctx.message.id}bonk.gif')
                await ctx.send(file=bonk_gif)
            except FileNotFoundError:
                await ctx.send(await getLocale("file-not-found", ctx.author.id))

    # This code needs a lot of RAM for some gifs, REST IN PEACE
    """"@commands.command()
    async def gifsign(self, ctx, *args):
        url = None
        if len(ctx.message.attachments) > 0:
            url = ctx.message.attachments[0].url
            text = " ".join(args)
        if url is not None:
            try:
                sign_buffer = await GifCreator(image_url=url).sign_gif(ctx.message.id, text)
                gifSigned = discord.File(sign_buffer, filename=f'temp/{ctx.message.id}signed.gif')
                await ctx.send(file=gifSigned)
            except FileNotFoundError:
                await ctx.send(await getLocale("file-not-found", ctx.author.id))
    """