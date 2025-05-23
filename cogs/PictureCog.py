import io
import os
import re

import discord
from discord.ext import commands

from cogs import LogCog
from service import pictureService
from service.localeService import getLocale
from utils.commandUtils import is_owner


class PictureCog(commands.Cog):

    def __init__(self, bot):
        LogCog.logSystem('Picture cog loaded')
        self.bot = bot

    @commands.command()
    async def black(self, ctx, *args):
        url = None
        if len(ctx.message.attachments) > 0:
            url = ctx.message.attachments[0].url
        elif len(ctx.message.mentions) > 0:
            url = ctx.message.mentions[0].avatar.url
        elif len(args) > 0:
            url = args[0]
        if url is not None:
            file = await pictureService.black(url, ctx.message.id)
            await ctx.send("Paint it Black", file=discord.File(file))
            os.remove(file)

    @commands.command()
    async def imgsearch(self, ctx, *args):
        ret = await pictureService.searchPhoto(" ".join(args))
        if ret is not None:
            embed = discord.Embed(
                title=" ".join(args)
            )
            embed.set_image(url=ret['src']['large'])
            embed.set_author(url=ret['photographer_url'], name=ret['photographer'])
            await ctx.send(embed=embed)
        else:
            await ctx.send(await getLocale('nothing-found', ctx.author.id))

    @commands.command()
    async def totext(self, ctx, *args):
        url = None
        if len(ctx.message.attachments) > 0:
            url = ctx.message.attachments[0].url
        elif len(ctx.message.mentions) > 0:
            url = ctx.message.mentions[0].avatar.url
        elif len(args) > 0:
            url = args[0]
        if url is not None:
            text = await pictureService.totext(url, ctx.message.id, 'n')
            await ctx.send(text)

    @commands.command()
    async def filetotext(self, ctx, *args):
        url = None
        if len(ctx.message.attachments) > 0:
            url = ctx.message.attachments[0].url
        elif len(ctx.message.mentions) > 0:
            url = ctx.message.mentions[0].avatar.url
        elif len(args) > 0:
            url = args[0]
        if url is not None:
            text = await pictureService.filetotext(url, ctx.message.id, 'n')
            file = io.BytesIO(text.encode('utf-8'))
            file = discord.File(file, "result.txt")
            await ctx.send(file=file)

    @commands.command()
    async def rtotext(self, ctx, *args):
        url = None
        if len(ctx.message.attachments) > 0:
            url = ctx.message.attachments[0].url
        elif len(ctx.message.mentions) > 0:
            url = ctx.message.mentions[0].avatar.url
        elif len(args) > 0:
            url = args[0]
        if url is not None:
            text = await pictureService.totext(url, ctx.message.id, 'r')
            await ctx.send(text)

    @commands.command()
    async def red(self, ctx, *args):
        url = None
        if len(ctx.message.attachments) > 0:
            url = ctx.message.attachments[0].url
        elif len(ctx.message.mentions) > 0:
            url = ctx.message.mentions[0].avatar.url
        elif len(args) > 0:
            url = args[0]
        if url is not None:
            file = await pictureService.get_channel(url, 'r', ctx.message.id)
            await ctx.send(file=discord.File(file))
            os.remove(file)

    @commands.command()
    async def green(self, ctx, *args):
        url = None
        if len(ctx.message.attachments) > 0:
            url = ctx.message.attachments[0].url
        elif len(ctx.message.mentions) > 0:
            url = ctx.message.mentions[0].avatar.url
        elif len(args) > 0:
            url = args[0]
        if url is not None:
            file = await pictureService.get_channel(url, 'g', ctx.message.id)
            await ctx.send(file=discord.File(file))
            os.remove(file)

    @commands.command()
    async def blue(self, ctx, *args):
        url = None
        if len(ctx.message.attachments) > 0:
            url = ctx.message.attachments[0].url
        elif len(ctx.message.mentions) > 0:
            url = ctx.message.mentions[0].avatar.url
        elif len(args) > 0:
            url = args[0]
        if url is not None:
            file = await pictureService.get_channel(url, 'b', ctx.message.id)
            await ctx.send(file=discord.File(file))
            os.remove(file)

    @commands.command()
    async def alpha(self, ctx, *args):
        url = None
        if len(ctx.message.attachments) > 0:
            url = ctx.message.attachments[0].url
        elif len(ctx.message.mentions) > 0:
            url = ctx.message.mentions[0].avatar.url
        elif len(args) > 0:
            url = args[0]
        if url is not None:
            file = await pictureService.get_channel(url, 'a', ctx.message.id)
            await ctx.send(file=discord.File(file))
            os.remove(file)

    @commands.command()
    async def cyan(self, ctx, *args):
        url = None
        if len(ctx.message.attachments) > 0:
            url = ctx.message.attachments[0].url
        elif len(ctx.message.mentions) > 0:
            url = ctx.message.mentions[0].avatar.url
        elif len(args) > 0:
            url = args[0]
        if url is not None:
            file = await pictureService.get_CMYKchannel(url, 'c', ctx.message.id)
            await ctx.send(file=discord.File(file))
            os.remove(file)

    @commands.command()
    async def magenta(self, ctx, *args):
        url = None
        if len(ctx.message.attachments) > 0:
            url = ctx.message.attachments[0].url
        elif len(ctx.message.mentions) > 0:
            url = ctx.message.mentions[0].avatar.url
        elif len(args) > 0:
            url = args[0]
        if url is not None:
            file = await pictureService.get_CMYKchannel(url, 'm', ctx.message.id)
            await ctx.send(file=discord.File(file))
            os.remove(file)

    @commands.command()
    async def yellow(self, ctx, *args):
        url = None
        if len(ctx.message.attachments) > 0:
            url = ctx.message.attachments[0].url
        elif len(ctx.message.mentions) > 0:
            url = ctx.message.mentions[0].avatar.url
        elif len(args) > 0:
            url = args[0]
        if url is not None:
            file = await pictureService.get_CMYKchannel(url, 'y', ctx.message.id)
            await ctx.send(file=discord.File(file))
            os.remove(file)

    @commands.command()
    async def key(self, ctx, *args):
        url = None
        if len(ctx.message.attachments) > 0:
            url = ctx.message.attachments[0].url
        elif len(ctx.message.mentions) > 0:
            url = ctx.message.mentions[0].avatar.url
        elif len(args) > 0:
            url = args[0]
        if url is not None:
            file = await pictureService.get_CMYKchannel(url, 'k', ctx.message.id)
            await ctx.send(file=discord.File(file))
            os.remove(file)

    @commands.command()
    async def swap(self, ctx, url, mode):
        file = await pictureService.change_channel(url, mode, ctx.message.id)
        await ctx.send(file=discord.File(file))
        os.remove(file)

    @commands.command()
    async def opacity(self, ctx, url, alpha):
        file = await pictureService.set_alpha(url, alpha, ctx.message.id)
        await ctx.send(file=discord.File(file))
        os.remove(file)

    @commands.command()
    async def blur(self, ctx, *args):
        url = None
        power = None
        if len(ctx.message.attachments) > 0 and len(args) > 0:
            url = ctx.message.attachments[0].url
            power = int(args[0])
        elif len(ctx.message.mentions) > 0 and len(args) > 0:
            url = ctx.message.mentions[0].avatar.url
            power = int(args[0])
        elif len(args) >= 2:
            url = args[0]
            power = int(args[1])
        if url is not None:
            file = await pictureService.blur(power, url, ctx.message.id)
            await ctx.send(file=discord.File(file))
            os.remove(file)

    @commands.command()
    async def spread(self, ctx, *args):
        url = None
        power = None
        if len(ctx.message.attachments) > 0 and len(args) > 0:
            url = ctx.message.attachments[0].url
            power = int(args[0])
        elif len(ctx.message.mentions) > 0 and len(args) > 0:
            url = ctx.message.mentions[0].avatar.url
            power = int(args[0])
        elif len(args) >= 2:
            url = args[0]
            power = int(args[1])
        if url is not None:
            file = await pictureService.spread(power, url, ctx.message.id)
            await ctx.send(file=discord.File(file))
            os.remove(file)

    @commands.command()
    async def contrast(self, ctx, *args):
        url = None
        power = None
        if len(ctx.message.attachments) > 0 and len(args) > 0:
            url = ctx.message.attachments[0].url
            power = int(args[0])
        elif len(ctx.message.mentions) > 0 and len(args) > 0:
            url = ctx.message.mentions[0].avatar.url
            power = int(args[0])
        elif len(args) >= 2:
            url = args[0]
            power = int(args[1])
        if url is not None:
            file = await pictureService.contrast(power, url, ctx.message.id)
            await ctx.send(file=discord.File(file))
            os.remove(file)

    @commands.command()
    async def invers(self, ctx, *args):
        url = None
        if len(ctx.message.attachments) > 0:
            url = ctx.message.attachments[0].url
        elif len(ctx.message.mentions) > 0:
            url = ctx.message.mentions[0].avatar.url
        elif len(args) > 0:
            url = args[0]
        if url is not None:
            file = await pictureService.inversion(url, ctx.message.id)
            await ctx.send(file=discord.File(file))
            os.remove(file)

    @commands.command()
    async def crop(self, ctx, left: int, top: int, right: int, bottom: int, url):
        file = await pictureService.crop(left, top, right, bottom, url, ctx.message.id)
        await ctx.send(file=discord.File(file))
        os.remove(file)

    @commands.command()
    async def vietnam(self, ctx, *args):
        url = None
        if len(ctx.message.attachments) > 0:
            url = ctx.message.attachments[0].url
        elif len(ctx.message.mentions) > 0:
            url = ctx.message.mentions[0].avatar.url
        elif len(args) > 0:
            url = args[0]
        if url is not None:
            file = await pictureService.vietnam(url, ctx.message.id)
            await ctx.send(file=discord.File(file))
            os.remove(file)

    @commands.command()
    async def rip(self, ctx, *args):
        url = None
        if len(ctx.message.attachments) > 0:
            url = ctx.message.attachments[0].url
        elif len(ctx.message.mentions) > 0:
            url = ctx.message.mentions[0].avatar.url
        elif len(args) > 0:
            url = args[0]
        if url is not None:
            file = await pictureService.rip(url, ctx.message.id)
            await ctx.send(file=discord.File(file))
            os.remove(file)

    @commands.command()
    async def yae(self, ctx, *args):
        url = None
        if len(ctx.message.attachments) > 0:
            url = ctx.message.attachments[0].url
        elif len(ctx.message.mentions) > 0:
            url = ctx.message.mentions[0].avatar.url
        elif len(args) > 0:
            url = args[0]
        if url is not None:
            file = await pictureService.yae(url, ctx.message.id)
            await ctx.send(file=discord.File(file))
            os.remove(file)

    # Wow this command still exist. I recommend to delete it
    @commands.command()
    async def hans(self, ctx, *args):
        url = None
        if len(ctx.message.attachments) > 0:
            url = ctx.message.attachments[0].url
        elif len(ctx.message.mentions) > 0:
            url = ctx.message.mentions[0].avatar.url
        elif len(args) > 0:
            url = args[0]
        if url is not None:
            if ctx.message.author.id == 593738881804009472 or ctx.message.author.id == 418040057019236353:
                file = await pictureService.hans(url, ctx.message.id)
                await ctx.send(file=discord.File(file))
                os.remove(file)

    @commands.command()
    async def penguin(self, ctx):
        text = ctx.message.content[8:]
        if len(text) > 0:
            file = pictureService.penguin(ctx.message.id, text)
            await ctx.send(file=discord.File(file))
            os.remove(file)
        else:
            await ctx.send(file=discord.File('assets/background/penguin.png'))

    @commands.command()
    async def frameh(self, ctx, *args):
        url = None
        if len(ctx.message.attachments) > 0:
            url = ctx.message.attachments[0].url
        elif len(ctx.message.mentions) > 0:
            url = ctx.message.mentions[0].avatar.url
        elif len(args) > 0:
            url = args[0]
        if url is not None:
            file = await pictureService.frame(url, 'h', ctx.message.id)
            await ctx.send(file=discord.File(file))
            os.remove(file)

    @commands.command()
    async def framev(self, ctx, *args):
        url = None
        if len(ctx.message.attachments) > 0:
            url = ctx.message.attachments[0].url
        elif len(ctx.message.mentions) > 0:
            url = ctx.message.mentions[0].avatar.url
        elif len(args) > 0:
            url = args[0]
        if url is not None:
            file = await pictureService.frame(url, 'v', ctx.message.id)
            await ctx.send(file=discord.File(file))
            os.remove(file)

    @commands.command()
    async def triggered(self, ctx, *args):
        url = None
        if len(ctx.message.attachments) > 0:
            url = ctx.message.attachments[0].url
        elif len(ctx.message.mentions) > 0:
            url = ctx.message.mentions[0].avatar.url
        elif len(args) > 0:
            url = args[0]
        if url is not None:
            file = await pictureService.triggered(url, ctx.message.id)
            await ctx.send(file=discord.File(file))
            os.remove(file)

    @commands.command()
    async def color(self, ctx, red: int, green: int, blue: int, url):
        file = await pictureService.change_color(url, red, green, blue, ctx.message.id)
        await ctx.send(file=discord.File(file))
        os.remove(file)

    @commands.command()
    async def mix(self, ctx, alpha, image_url1, image_url2):
        try:
            file = await pictureService.mix(image_url1, image_url2, int(alpha), ctx.message.id)
            await ctx.send(file=discord.File(file))
            os.remove(file)
        except Exception as e:
            print(str(e))

    @commands.command()
    async def resize(self, ctx, *args):
        if len(args) > 2:
            file = await pictureService.resize(args[2], float(args[0]), float(args[1]), "%", ctx.message.id)
        else:
            file = await pictureService.resize(args[1], float(args[0]), float(args[0]), "%", ctx.message.id)
        await ctx.send(file=discord.File(file))
        os.remove(file)

    @commands.command()
    async def size(self, ctx, *args):
        if len(args) > 2:
            file = await pictureService.resize(args[2], float(args[0]), float(args[1]), "px", ctx.message.id)
        else:
            file = await pictureService.resize(args[1], float(args[0]), float(args[0]), "px", ctx.message.id)
        await ctx.send(file=discord.File(file))
        os.remove(file)

    @commands.command()
    async def sign(self, ctx, *args):
        text = " ".join(args)
        url = None
        if len(ctx.message.attachments) > 0:
            url = ctx.message.attachments[0].url
        elif len(ctx.message.mentions) > 0:
            url = ctx.message.mentions[0].avatar.url
            text = text.replace(args[0] + " ", "", 1)
        elif len(args) > 0 and str(args[0]).startswith("http"):
            url = args[0]
            text = text.replace(url + " ", "", 1)
        if url is not None:
            file = await pictureService.sign(text, url, "bottom", ctx.message.id)
            await ctx.send(file=discord.File(file))
            os.remove(file)

    @commands.command()
    async def poster(self, ctx, *args):
        url = None
        colors = None
        if len(ctx.message.attachments) > 0 and len(args) > 0:
            url = ctx.message.attachments[0].url
            colors = args[0]
        elif len(ctx.message.mentions) > 0 and len(args) > 1:
            url = ctx.message.mentions[0].avatar.url
            colors = args[1]
        elif len(args) >= 2 and str(args[0]).startswith("http"):
            url = args[0]
            colors = args[1]
        if url is not None and colors is not None:
            try:
                file = await pictureService.poster(url, int(colors), ctx.message.id)
                await ctx.send(file=discord.File(file))
                os.remove(file)
            except FileNotFoundError:
                await ctx.send(await getLocale("file-not-found", ctx.author.id))
        else:
            await ctx.send(await getLocale("file-not-found", ctx.author.id))

    @commands.command()
    async def oil(self, ctx, *args):
        url = None
        if len(ctx.message.attachments) > 0:
            url = ctx.message.attachments[0].url
        elif len(ctx.message.mentions) > 0:
            url = ctx.message.mentions[0].avatar.url
        elif len(args) > 0 and str(args[0]).startswith("http"):
            url = args[0]
        if url is not None:
            try:
                file = await pictureService.as_paint(url, ctx.message.id, "oil")
                await ctx.send(file=discord.File(file))
                os.remove(file)
            except FileNotFoundError:
                await ctx.send(await getLocale("file-not-found", ctx.author.id))
        else:
            await ctx.send(await getLocale("file-not-found", ctx.author.id))

    @commands.command()
    async def pencil(self, ctx, *args):
        url = None
        if len(ctx.message.attachments) > 0:
            url = ctx.message.attachments[0].url
        elif len(ctx.message.mentions) > 0:
            url = ctx.message.mentions[0].avatar.url
        elif len(args) > 0 and str(args[0]).startswith("http"):
            url = args[0]
        if url is not None:
            try:
                file = await pictureService.as_paint(url, ctx.message.id, "pencil")
                await ctx.send(file=discord.File(file))
                os.remove(file)
            except FileNotFoundError:
                await ctx.send(await getLocale("file-not-found", ctx.author.id))
        else:
            await ctx.send(await getLocale("file-not-found", ctx.author.id))

    @commands.command()
    async def watercolor(self, ctx, *args):
        url = None
        if len(ctx.message.attachments) > 0:
            url = ctx.message.attachments[0].url
        elif len(ctx.message.mentions) > 0:
            url = ctx.message.mentions[0].avatar.url
        elif len(args) > 0 and str(args[0]).startswith("http"):
            url = args[0]
        if url is not None:
            try:
                file = await pictureService.as_paint(url, ctx.message.id, "watercolor")
                await ctx.send(file=discord.File(file))
                os.remove(file)
            except FileNotFoundError:
                await ctx.send(await getLocale("file-not-found", ctx.author.id))
        else:
            await ctx.send(await getLocale("file-not-found", ctx.author.id))


    @commands.command()
    async def signtop(self, ctx, *args):
        text = " ".join(args)
        url = None
        if len(ctx.message.attachments) > 0:
            url = ctx.message.attachments[0].url
        elif len(ctx.message.mentions) > 0:
            url = ctx.message.mentions[0].avatar.url
            text = text.replace(args[0] + " ", "", 1)
        elif len(args) > 0 and str(args[0]).startswith("http"):
            url = args[0]
            text = text.replace(url + " ", "", 1)
        if url is not None:
            file = await pictureService.sign(text, url, "top", ctx.message.id)
            await ctx.send(file=discord.File(file))
            os.remove(file)



    @commands.command()
    async def card(self, ctx, *args):
        url = "https://miro.medium.com/max/1400/1*9WeJrBj6pp-qnGjRGg2NUw.webp"
        if len(ctx.message.attachments) > 0:
            url = ctx.message.attachments[0].url
        elif len(ctx.message.mentions) > 0:
            url = ctx.message.mentions[0].avatar.url
        elif len(args) > 0:
            url = args[0]

        file = await pictureService.card(url, ctx.message.id)
        await ctx.send(file=discord.File(file))
        os.remove(file)

    @commands.command()
    async def quote(self, ctx, user: discord.Member, *args):
        color = "#ffffff"
        if re.match(r"^#[0-9a-fA-F]{6}$", args[0]):
            color = args[0]
            args = args[1:]
        text =" ".join(args)
        if len(text) > 200:
            text = text[0:200]
        file = await pictureService.quote(user.avatar.url, text, ctx.message.id, user.name, color)
        await ctx.send(file=discord.File(file))
        os.remove(file)
