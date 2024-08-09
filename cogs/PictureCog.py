import os

import discord
from discord.ext import commands

from cogs import LogCog
from service import pictureService
from service.localeService import getLocale


class PictureCog(commands.Cog):

    def __init__(self, bot):
        LogCog.logSystem('Picture cog loaded')
        self.bot = bot

    @commands.command()
    async def black(self, ctx, url):
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
            await ctx.send(getLocale('nothing-found', ctx.author.id))

    @commands.command()
    async def totext(self, ctx, url):
        text = await pictureService.totext(url, ctx.message.id, 'n')
        await ctx.send(text)

    @commands.command()
    async def rtotext(self, ctx, url):
        text = await pictureService.totext(url, ctx.message.id, 'r')
        await ctx.send(text)

    @commands.command()
    async def red(self, ctx, url):
        file = await pictureService.get_channel(url, 'r', ctx.message.id)
        await ctx.send(file=discord.File(file))
        os.remove(file)

    @commands.command()
    async def green(self, ctx, url):
        file = await pictureService.get_channel(url, 'g', ctx.message.id)
        await ctx.send(file=discord.File(file))
        os.remove(file)

    @commands.command()
    async def blue(self, ctx, url):
        file = await pictureService.get_channel(url, 'b', ctx.message.id)
        await ctx.send(file=discord.File(file))
        os.remove(file)

    @commands.command()
    async def alpha(self, ctx, url):
        file = await pictureService.get_channel(url, 'a', ctx.message.id)
        await ctx.send(file=discord.File(file))
        os.remove(file)

    @commands.command()
    async def cyan(self, ctx, url):
        file = await pictureService.get_CMYKchannel(url, 'c', ctx.message.id)
        await ctx.send(file=discord.File(file))
        os.remove(file)

    @commands.command()
    async def magenta(self, ctx, url):
        file = await pictureService.get_CMYKchannel(url, 'm', ctx.message.id)
        await ctx.send(file=discord.File(file))
        os.remove(file)

    @commands.command()
    async def yellow(self, ctx, url):
        file = await pictureService.get_CMYKchannel(url, 'y', ctx.message.id)
        await ctx.send(file=discord.File(file))
        os.remove(file)

    @commands.command()
    async def key(self, ctx, url):
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
    async def blur(self, ctx, url, power):
        file = await pictureService.blur(url, power, ctx.message.id)
        await ctx.send(file=discord.File(file))
        os.remove(file)

    @commands.command()
    async def spread(self, ctx, url, power):
        file = await pictureService.spread(url, power, ctx.message.id)
        await ctx.send(file=discord.File(file))
        os.remove(file)

    @commands.command()
    async def contrast(self, ctx, url, power):
        file = await pictureService.contrast(url, power, ctx.message.id)
        await ctx.send(file=discord.File(file))
        os.remove(file)

    @commands.command()
    async def invers(self, ctx, url):
        file = await pictureService.inversion(url, ctx.message.id)
        await ctx.send(file=discord.File(file))
        os.remove(file)

    @commands.command()
    async def crop(self, ctx, left: int, top: int, right: int, bottom: int, url):
        file = await pictureService.crop(left, top, right, bottom, url, ctx.message.id)
        await ctx.send(file=discord.File(file))
        os.remove(file)

    @commands.command()
    async def vietnam(self, ctx, url):
        file = await pictureService.vietnam(url, ctx.message.id)
        await ctx.send(file=discord.File(file))
        os.remove(file)

    @commands.command()
    async def rip(self, ctx, url):
        file = await pictureService.rip(url, ctx.message.id)
        await ctx.send(file=discord.File(file))
        os.remove(file)

    @commands.command()
    async def yae(self, ctx, url):
        file = await pictureService.yae(url, ctx.message.id)
        await ctx.send(file=discord.File(file))
        os.remove(file)

    @commands.command()
    async def hans(self, ctx, url):
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
    async def frameh(self, ctx, url):
        file = await pictureService.frame(url, 'h', ctx.message.id)
        await ctx.send(file=discord.File(file))
        os.remove(file)

    @commands.command()
    async def framev(self, ctx, url):
        file = await pictureService.frame(url, 'v', ctx.message.id)
        await ctx.send(file=discord.File(file))
        os.remove(file)

    @commands.command()
    async def triggered(self, ctx, url):
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
        file = await pictureService.mix(image_url1, image_url2, alpha, ctx.message.id)
        await ctx.send(file=discord.File(file))
        os.remove(file)

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
    async def sign(self, ctx, url, *args):
        file = await pictureService.sign(" ".join(args), url, "bottom", ctx.message.id)
        await ctx.send(file=discord.File(file))
        os.remove(file)

    @commands.command()
    async def signtop(self, ctx, url, *args):
        file = await pictureService.sign(" ".join(args), url, "top", ctx.message.id)
        await ctx.send(file=discord.File(file))
        os.remove(file)

    @commands.command()
    async def card(self, ctx, *args):
        if len(args):
            file = await pictureService.card(args[0], ctx.message.id)
        else:
            file = await pictureService.card("https://miro.medium.com/max/1400/1*9WeJrBj6pp-qnGjRGg2NUw.webp", ctx.message.id)
        await ctx.send(file=discord.File(file))
        os.remove(file)
