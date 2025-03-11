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