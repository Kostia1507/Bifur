import codecs
import gc
import os
import psutil
from datetime import datetime

import discord
import asyncpg
from discord.ext import commands, tasks

import config
from utils import commandUtils
from cogs import LogCog
from service import cooldownService, pagedMessagesService, premiumService

import matplotlib
import matplotlib.pyplot as plt

# imports for >eval
from discord.utils import get
import math


class AdminCog(commands.Cog):

    def __init__(self, bot):
        matplotlib.use('Agg')
        self.RAMHistory = []
        self.SystemRAMHistory = []
        self.RAMTime = []
        LogCog.logSystem('Admin cog loaded')
        self.checkHealth.start()
        self.bot = bot
        self.stTime = datetime.utcnow()

    @commands.command()
    @commands.check(commandUtils.is_owner)
    async def log(self, ctx, *args):
        LogCog.logInfo(" ".join(args), ctx.author.name)
        await ctx.message.add_reaction('✅')

    @commands.command()
    @commands.check(commandUtils.is_owner)
    async def cooldowns(self, ctx):
        await ctx.send(cooldownService.toString())

    @commands.command()
    @commands.check(commandUtils.is_owner)
    async def eval(self, ctx, *args):
        res = eval(" ".join(args))
        if res is not None:
            await ctx.send(res)
        else:
            await ctx.send("Success!")

    @commands.command()
    @commands.check(commandUtils.is_owner)
    async def say(self, ctx, *args):
        await ctx.send(" ".join(args))
        await ctx.message.delete()

    @commands.command()
    @commands.check(commandUtils.is_owner)
    async def status(self, ctx):
        startInfo = f'<t:{str(int(self.stTime.timestamp()))}>'
        nowInfo = f'<t:{str(int(datetime.utcnow().timestamp()))}>'
        seconds = int(datetime.utcnow().timestamp()) - int(self.stTime.timestamp())
        status = f'Я запустився о {startInfo}\nЗараз: {nowInfo}\nВсього: {str(seconds // 3600)}h' \
                 f' {str(seconds // 60 % 60)}m {str(seconds % 60)}s\n'
        count = -1
        for path in os.listdir('temp'):
            if os.path.isfile(os.path.join('temp', path)):
                count += 1
        mCount = -1
        for path in os.listdir('music'):
            if os.path.isfile(os.path.join('music', path)):
                mCount += 1
        status += f'Тимчасових файлів: {str(count)}\n'
        status += f'MP3 файлів: {str(mCount)}\n'
        status += f'Кількість унікальних користувачів: {str(len(cooldownService.cooldownUser))}\n'
        await ctx.send(status)

    @commands.command()
    @commands.check(commandUtils.is_owner)
    async def guilds(self, ctx):
        res = ""
        for guild in self.bot.guilds:
            res += f'{guild.name} : {guild.id}\n'
        pagedMsg = pagedMessagesService.initPagedMessage(self.bot, "All guilds", res)
        embed = discord.Embed(title=pagedMsg.title, description=pagedMsg.pages[0])
        embed.set_footer(text=f'Page 1 of {len(pagedMsg.pages)}')
        await ctx.send(embed=embed, view=pagedMsg.view)

    @commands.command()
    @commands.check(commandUtils.is_owner)
    async def guildinfo(self, ctx, guild_id: int):
        guild = self.bot.get_guild(guild_id)
        fetchGuild = await self.bot.fetch_guild(guild_id)
        message = f'Created at {guild.created_at.strftime("%d/%m/%Y")}\n' \
                  f'Members count: {fetchGuild.approximate_member_count}\n' \
                  f'Online members: {fetchGuild.approximate_presence_count}\n' \
                  f'Emojis {len(guild.emojis)}/{guild.emoji_limit}\n' \
                  f'Stickers {len(guild.stickers)}/{guild.sticker_limit}\n' \
                  f'Owner: {guild.owner.name}\n'

        pagedMsg = pagedMessagesService.initPagedMessage(self.bot, guild.name, message)
        embed = discord.Embed(title=pagedMsg.title, description=pagedMsg.pages[0])
        embed.set_footer(text=f'Page 1 of {len(pagedMsg.pages)}')
        if guild.icon is not None:
            pagedMsg.imageUrl = guild.icon.url
            embed.set_image(url=guild.icon.url)
        await ctx.send(embed=embed, view=pagedMsg.view)

    @commands.command(alliases=['listofallcommands', 'listallcommands'])
    @commands.check(commandUtils.is_owner)
    async def listallcmds(self, ctx):
        text = ""
        for command in self.bot.commands:
            text += f"{command}\n"

        pagedMsg = pagedMessagesService.initPagedMessage(self.bot, "All commands", text)
        embed = discord.Embed(title=pagedMsg.title, description=pagedMsg.pages[0])
        embed.set_footer(text=f'Page 1 of {len(pagedMsg.pages)}')
        await ctx.send(embed=embed, view=pagedMsg.view)

    @commands.command()
    @commands.check(commandUtils.is_owner)
    async def sql(self, ctx, *args):
        conn = await asyncpg.connect(
            host=config.host,
            database=config.database,
            user=config.user,
            password=config.password,
            port=config.port
        )
        loop = " ".join(args)
        if loop.lower().find("select") == -1:
            await conn.execute((" ".join(args)).strip())
            await conn.close()
            return
        outputrows = await conn.fetch((" ".join(args)).strip())
        await conn.close()
        output = ""
        for row in outputrows:
            output += str(row) + "\n"

        pagedMsg = pagedMessagesService.initPagedMessage(self.bot, "SQL Request", output)
        embed = discord.Embed(title=pagedMsg.title, description=pagedMsg.pages[0])
        embed.set_footer(text=f'Page 1 of {len(pagedMsg.pages)}')
        await ctx.send(embed=embed, view=pagedMsg.view)

    @commands.command()
    @commands.check(commandUtils.is_owner)
    async def rawoutput(self, ctx):
        with open(f'{ctx.message.id}.txt', "w") as file:
            file.write(str(ctx.message.content))
        with open(f'{ctx.message.id}.txt', "rb") as file:
            await ctx.send(file=discord.File(file, f'{ctx.message.id}.txt'))
        os.remove(f'{ctx.message.id}.txt')

    @tasks.loop(minutes=20)
    async def checkHealth(self):
        # I don't want to run it at local machine
        gc.collect()
        if not config.release:
            return
        process = psutil.Process()
        RAMBytes = process.memory_info().rss
        currentRAM = RAMBytes // 1048576
        sysUsage = dict(psutil.virtual_memory()._asdict())
        currentSystemRam = int(sysUsage["total"] * sysUsage["percent"] / 100 // 1048576)
        self.RAMHistory.append(currentRAM)
        self.SystemRAMHistory.append(currentSystemRam)
        self.RAMTime.append(f'{datetime.now().hour}:{datetime.now().minute}')
        seconds = int(datetime.utcnow().timestamp()) - int(self.stTime.timestamp())
        status = f'Бот живий вже: {str(seconds // 3600)}h' \
                 f' {str(seconds // 60 % 60)}m {str(seconds % 60)}s\n'
        status += f'Кількість унікальних користувачів: {str(len(cooldownService.cooldownUser))}\n'
        status += f'Кількість серверів: {len(self.bot.guilds)}\n'
        status += f'Преміум користувачів: {await premiumService.get_premium_count()}\n'
        status += f'Зараз я використовую {currentRAM} МБ\n'
        status += f'Система {currentSystemRam} МБ\n'
        while len(self.RAMHistory) > 12:
            self.RAMHistory = self.RAMHistory[1:]
            self.RAMTime = self.RAMTime[1:]
            self.SystemRAMHistory = self.SystemRAMHistory[1:]

        channel = self.bot.get_channel(config.status_channel)
        if len(self.RAMHistory) >= 2:
            try:
                ax = plt.gca()
                ax.set_ylim([min(self.RAMHistory) - 10, max(self.SystemRAMHistory) + 10])
                plt.plot(self.RAMTime, self.RAMHistory, label=f'Bot RAM')
                plt.plot(self.RAMTime, self.SystemRAMHistory, label=f'System RAM')
                plt.title('Bifur RAM Usage')
                plt.xlabel('Time UTC')
                plt.ylabel('RAM')
                plt.legend()
                plt.savefig('temp/ram-usage.png')
                plt.close()
                await channel.send(status, file=discord.File("temp/ram-usage.png"))
                os.remove('temp/ram-usage.png')
            except Exception as e:
                await channel.send(status)
                LogCog.logError(f'Exception in checkHealth {e}')
        else:
            await channel.send(status)

    @commands.command()
    @commands.check(commandUtils.is_owner)
    async def sync(self, ctx):
        count = len(await self.bot.tree.sync())
        await ctx.send(f'Synced {count} commands')

    @commands.command()
    @commands.check(commandUtils.is_owner)
    async def tempfiles(self, ctx):
        try:
            res = ""
            files = [f for f in os.listdir("temp") if os.path.isfile(os.path.join("temp", f))]
            for file in files:
                res += f"{file}\n"

            if len(res) == 0:
                res = "There is no files"
            pagedMsg = pagedMessagesService.initPagedMessage(self.bot, "Temp files", res)
            embed = discord.Embed(title=pagedMsg.title, description=pagedMsg.pages[0])
            embed.set_footer(text=f'Page 1 of {len(pagedMsg.pages)}')
            await ctx.send(embed=embed, view=pagedMsg.view)
        except FileNotFoundError:
            LogCog.logError(f"Папка temp не знайдена.")
        except PermissionError:
            LogCog.logError(f"Немає доступу до папки temp.")
