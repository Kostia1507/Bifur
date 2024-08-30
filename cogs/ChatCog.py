import os
import random
from datetime import datetime

import aiohttp
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions

from cogs import LogCog

import config
from discordModels.views.ReportView import ReportView
from service.localeService import getLocale, getUserLang, getLocaleByLang


class ChatCog(commands.Cog):

    def __init__(self, bot):
        LogCog.logSystem('Chat cog loaded')
        self.bot = bot
        self.ruleHistory = {}

    @commands.command()
    async def invite(self, ctx):
        await ctx.send(config.invite)

    @commands.command()
    async def animal(self, ctx):
        userLang = getUserLang(ctx.author.id)
        a = await ctx.send(f'{getLocaleByLang("random-animal", userLang)}'
                           f' {str(random.choice(getLocaleByLang("animals", userLang)))}')
        await a.add_reaction('\N{THUMBS UP SIGN}')
        await a.add_reaction('\N{THUMBS DOWN SIGN}')

    @commands.command()
    async def ball(self, ctx):
        userLang = getUserLang(ctx.author.id)
        response = random.choice(getLocaleByLang('8ball', userLang))
        await ctx.send(f'{getLocaleByLang("8ball-answer", userLang)} {response}')

    @commands.command()
    async def roll(self, ctx, *args):
        start, end = 0, 100
        if len(args) > 2:
            start, end, count = min(int(args[0]), int(args[1])), max(int(args[0]), int(args[1])), int(args[2])
            count = min(count, end - start)
            array = list(range(start, end + 1))
            result = []
            for i in range(count):
                choice = random.choice(array)
                array.remove(choice)
                result.append(str(choice))
            result = " ".join(result)
            await ctx.send(
                getLocale('random-number', ctx.author.id).replace('%1', str(start)).replace('%2', str(end))
                .replace('%3', result))
        else:
            if len(args) > 1:
                start, end = min(int(args[0]), int(args[1])), max(int(args[0]), int(args[1]))
            elif len(args) > 0:
                end = int(args[0])
            await ctx.send(getLocale('random-number', ctx.author.id).replace('%1', str(start)).replace('%2', str(end))
                           .replace('%3', str(random.randint(start, end))))

    @commands.command()
    async def randp(self, ctx):
        if len(ctx.message.mentions) > 0:
            await ctx.send(f'{getLocale("chose", ctx.author.id)} {random.choice(ctx.message.mentions).mention}')

    @commands.command()
    async def randw(self, ctx, *args):
        await ctx.send(f'{getLocale("chose", ctx.author.id)} {random.choice(args)}')

    @commands.command()
    async def randm(self, ctx):
        messages = [msg async for msg in ctx.channel.history(limit=200)]
        choose = random.choice(messages)
        await ctx.message.delete()
        await ctx.send(f'**{getLocale("quote", ctx.author.id)} {str(choose.author)}**:\n{choose.content}')
        if choose.attachments:
            await choose.channel.send(content=choose.attachments[0].url)

    @commands.command()
    async def gava(self, ctx):
        await ctx.send(ctx.guild.icon.url)

    @commands.command()
    async def ava(self, ctx):
        if len(ctx.message.mentions) > 0:
            for user in ctx.message.mentions:
                await ctx.send(user.avatar.url)

    @commands.command()
    async def hui(self, ctx):
        size = random.randint(1, 25)
        await ctx.send(f'Хуй {ctx.author.name}\'s\n 8{"=" * size}) [{str(size)}см]')

    @commands.command()
    async def cont(self, ctx, chance, number):
        try:
            res = (1 - pow(1 - float(chance) / 100, int(number))) * 100
            await ctx.send("Шанс: " + str(format(res, '.2f')) + "%")
        except ValueError:
            LogCog.logError("ERROR Помилка конвертації в >cont")
            await ctx.send("Перше число, шанс випадіння(дроб), інше - кількість контейнерів(ціле)")

    @commands.command()
    async def vote(self, ctx):
        await ctx.message.delete()
        messages = ctx.channel.history(limit=1)
        async for message in messages:
            await message.add_reaction('\N{THUMBS UP SIGN}')
            await message.add_reaction('\N{THUMBS DOWN SIGN}')
            await message.add_reaction('🤷‍♂️')

    @has_permissions(manage_messages=True)
    @commands.command(aliases=['clear'])
    async def clean(self, ctx, n: int):
        limit = min(abs(n), 100)
        await ctx.channel.purge(limit=limit + 1)
        LogCog.logInfo(f"Видалено {limit} повідомлень в чаті {ctx.channel.id}", ctx.author.name)

    @commands.command()
    async def report(self, ctx, *args):
        embed = discord.Embed(title="Report form",
                              description=("You can use this form to send a complaint.\n"
                                           "Try to describe all your actions and the time when it happened."))
        embed.set_footer(text=f"Thank you! Together we will make {self.bot.user.name} better!")
        await ctx.send(embed=embed, view=ReportView(self.bot))

    @commands.command()
    @commands.is_nsfw()
    async def rule34(self, ctx, *args):
        limit = 1000
        link = f'https://api.rule34.xxx/index.php?page=dapi&s=post&q=index&limit={limit}&json=1&pid=1&tags='
        tags = ""
        for tag in args:
            tags += f'{tag}*+'
        answer = ""
        async with aiohttp.ClientSession() as session:
            async with session.get(link + tags) as response:
                if response.status == 200:
                    answer = await response.json()
        async with aiohttp.ClientSession() as session:
            while len(answer) <= 0 < limit:
                limit = limit // 2
                link = f'https://api.rule34.xxx/index.php?page=dapi&s=post&q=index&limit={limit}&json=1&pid=1&tags='
                async with session.get(link + tags) as response:
                    if response.status == 200:
                        answer = await response.json()
        try:
            n = random.randint(0, len(answer) - 1)
            # bypass check if array is too small
            if len(answer) > 20 and ctx.channel.id in self.ruleHistory.keys():
                loop = self.ruleHistory[ctx.channel.id].copy()
                while len(loop) > limit // 5:
                    loop = loop[1:]
                self.ruleHistory[ctx.channel.id] = loop
                while n in loop:
                    LogCog.logDebug("Wow prevent same picture")
                    n = random.randint(0, len(answer) - 1)
            res = answer[n]
            fileLink = res['sample_url']
            async with aiohttp.ClientSession() as session:
                async with session.get(fileLink) as response:
                    if response.status == 200:
                        content_type = response.headers['Content-Type']
                        img_data = await response.read()
            fileName = f'temp/{ctx.message.id}.jpg'
            if content_type == 'image/png':
                fileName = f'temp/{ctx.message.id}.png'
            elif content_type == 'image/tiff':
                fileName = f'temp/{ctx.message.id}.tiff'
            elif content_type == 'image/gif':
                fileName = f'temp/{ctx.message.id}.gif'
            with open(fileName, 'wb') as handler:
                handler.write(img_data)
            embed = discord.Embed(
                title=" ".join(args)
            )
            embed.set_image(url=f'attachment://{fileName[5:len(fileName)]}')
            embed.set_footer(text=res['tags'] + f'\nPicked {n} in array of {len(answer)}')
            if ctx.channel.id in self.ruleHistory.keys():
                self.ruleHistory[ctx.channel.id].append(n)
            else:
                self.ruleHistory[ctx.channel.id] = [n]
            await ctx.send(file=discord.File(fileName), embed=embed)
            os.remove(fileName)
        except Exception as e:
            LogCog.logDebug(f'Exception on rule: {e}')
            await ctx.send(getLocale("nothing", ctx.author.id))

    @commands.command()
    async def reply(self, ctx, *args):
        await ctx.reply(f'<t:{str(int(datetime.now().timestamp()))}>  ' + " ".join(args))

    @commands.command()
    @has_permissions(manage_messages=True)
    async def embed(self, ctx):
        context = ctx.message.content.split('|')
        if len(context) < 2:
            embed = discord.Embed(
                title=context[0][7:len(context[0])],
            )
        elif len(context) < 3:
            embed = discord.Embed(
                description=context[1],
                title=context[0][7:len(context[0])],
            )
        else:
            embed = discord.Embed(
                colour=discord.Colour.from_str(context[2].strip()),
                description=context[1],
                title=context[0][7:len(context[0])],
            )
        embed.set_footer(text=f'{ctx.author.name}')
        if len(ctx.message.attachments) > 0:
            file = ctx.message.attachments[0]
            embed.set_image(url=file)
            await ctx.send(embed=embed)
        else:
            await ctx.send(embed=embed)

    @commands.command()
    async def cube(self, ctx, *args):
        if len(args) > 0 and args[0].isnumeric():
            n = min(9, int(args[0]))
            res = ""
            suma = 0
            for i in range(0, n):
                cube = random.randint(0, 5)
                suma += 1 + cube
                res += config.cubesEmojis[cube]
            await ctx.send(f'{res} = {suma}')
        else:
            await ctx.send(random.choice(config.cubesEmojis))
