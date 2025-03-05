import os
import random
from datetime import datetime

import aiohttp
import discord
import psycopg2
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions

import config
from service.localeService import getLocale
from utils import commandUtils
from cogs import LogCog
from service.currencyService import currency
from service.prefixService import setPrefix
from cogs.WeatherCog import getCoordinates, getWeather
from service import pagedMessagesService, autoReactionService, ignoreService
from models.PendingCommand import PendingCommand, get_pending_command, get_pending_commands_by_channel


class ServerAdministrationCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        ignoreService.initFromDB()
        LogCog.logSystem('Server Administration cog loaded')

    @commands.command()
    @has_permissions(manage_messages=True)
    async def autoreaction(self, ctx, emoji):
        autoReactionService.add(ctx.channel.id, emoji)
        await ctx.message.add_reaction('✅')

    @commands.command()
    @has_permissions(manage_messages=True)
    async def removereactions(self, ctx):
        autoReactionService.remove(ctx.channel.id)
        await ctx.message.add_reaction('✅')

    @commands.command()
    @has_permissions(manage_guild=True)
    async def setcmd(self, ctx, channel: discord.TextChannel):
        try:
            chnl = await ctx.guild.fetch_channel(channel.id)
            if chnl is not None:
                pc = PendingCommand(chnl.id, 1, datetime.now().hour, None, "")
                pc.insert()
                await ctx.message.add_reaction('✅')
            else:
                await ctx.message.add_reaction('❌')
        except discord.errors.NotFound or discord.errors.DiscordServerError:
            await ctx.message.add_reaction('❌')

    @commands.command()
    @has_permissions(manage_guild=True)
    async def getcmds(self, ctx, channel: discord.TextChannel):
        cmds = get_pending_commands_by_channel(channel.id)
        res = ""
        for cmd in cmds:
            res += f'ID: {cmd.id}; {cmd.cmdType}:{cmd.args}\n'
        if len(res) < 0:
            res = "List is empty. There is no auto-commands."
        await ctx.send(res)

    @commands.command()
    @has_permissions(manage_guild=True)
    async def editcmd(self, ctx, channel: discord.TextChannel, cmdId: int):
        cmd = get_pending_command(cmdId)
        if cmd.channelId != channel.id:
            await ctx.message.add_reaction('❌')
        else:
            pass

    @commands.command()
    @has_permissions(manage_guild=True)
    async def delcmd(self, ctx, channel: discord.TextChannel, cmdId: int):
        conn = psycopg2.connect(
            host=config.host,
            database=config.database,
            user=config.user,
            password=config.password,
            port=config.port
        )
        cur = conn.cursor()
        cur.execute('DELETE FROM autocmds WHERE channel_id = %s and id = %s', (channel.id, cmdId))
        conn.commit()
        cur.close()
        conn.close()
        await ctx.message.add_reaction('✅')

    @commands.command()
    @has_permissions(manage_guild=True)
    async def ignore(self, ctx, channel: discord.TextChannel):
        await ignoreService.manageIgnoredChannels(ctx, channel.id)

    @commands.command()
    @has_permissions(manage_guild=True)
    async def setprefix(self, ctx, prefix):
        setPrefix(ctx.guild.id, prefix)
        await ctx.send(f'{getLocale("set-prefix", ctx.author.id)} {prefix}')

    @ignore.error
    async def missing_channel(self, ctx, error):
        await ignoreService.manageIgnoredChannels(ctx, ctx.channel.id)
        return

    @commands.command()
    async def guildstat(self, ctx):
        guild = self.bot.get_guild(ctx.guild.id)
        fetchGuild = await self.bot.fetch_guild(ctx.guild.id)
        message = f'Created at {guild.created_at.strftime("%d/%m/%Y")}\n' \
                  f'Members count: {fetchGuild.approximate_member_count}\n' \
                  f'Online members: {fetchGuild.approximate_presence_count}\n' \
                  f'Emojis {len(guild.emojis)}/{guild.emoji_limit}\n' \
                  f'Stickers {len(guild.stickers)}/{guild.sticker_limit}\n\n'
        roles = await guild.fetch_roles()
        for role in roles:
            if not role.name == '@everyone' and not role.is_bot_managed():
                message += f'**{len(role.members)}** members has role **{role.name}**' \
                           f' created at {role.created_at.strftime("%d/%m/%Y")}\n'

        pagedMsg = pagedMessagesService.initPagedMessage(self.bot, guild.name, message)
        embed = discord.Embed(title=pagedMsg.title, description=pagedMsg.pages[0])
        embed.set_footer(text=f'Page 1 of {len(pagedMsg.pages)}')
        if guild.icon is not None:
            pagedMsg.imageUrl = guild.icon.url
            embed.set_image(url=guild.icon.url)
        await ctx.send(embed=embed, view=pagedMsg.view)

    @tasks.loop(minutes=13)
    async def checkForCommands(self):
        conn = psycopg2.connect(
            host=config.host,
            database=config.database,
            user=config.user,
            password=config.password,
            port=config.port
        )
        cur = conn.cursor()
        cur.execute("SELECT value from settings WHERE name='executed-auto-cmds'")
        value = cur.fetchone()[0]
        if int(value) == int(datetime.utcnow().hour):
            cur.close()
            conn.close()
            return
        LogCog.logSystem('execute checkForCommands in ServerAdministrationCog')
        cur.execute("UPDATE public.settings SET value= %s WHERE name='executed-auto-cmds'",
                    (datetime.utcnow().hour,))
        conn.commit()
        cur.close()
        conn.close()
        for cmd in self.pcs:
            try:
                await commandUtils.run_blocking(cmd.update_counter)
                channel = self.bot.get_channel(cmd.channelId)
                if cmd.counter >= cmd.interval:
                    await commandUtils.run_blocking(cmd.init_counter)
                    if cmd.cmdType == 'rule34' and channel.is_nsfw():
                        limit = 1000
                        link = 'https://api.rule34.xxx/index.php?page=dapi&s=post&q=index&json=1&pid=1&tags='
                        for tag in cmd.args.split(' '):
                            link += f'{tag}*+'
                        answer = ""
                        async with aiohttp.ClientSession() as session:
                            async with session.get(link) as response:
                                if response.status == 200:
                                    answer = await response.json()
                        async with aiohttp.ClientSession() as session:
                            while len(answer) <= 0 < limit:
                                limit = limit // 2
                                link = f'https://api.rule34.xxx/index.php?page=dapi&s=post&q=index&limit={limit}&json=1&pid=1&tags='
                                async with session.get(link) as response:
                                    if response.status == 200:
                                        answer = await response.json()
                        try:
                            res = random.choice(answer)
                            fileLink = res['sample_url']
                            async with aiohttp.ClientSession() as session:
                                async with session.get(fileLink) as response:
                                    if response.status == 200:
                                        content_type = response.headers['Content-Type']
                                        img_data = await response.read()
                            fileName = f'temp/{cmd.channelId}.jpg'
                            if content_type == 'image/png':
                                fileName = f'temp/{cmd.channelId}.png'
                            elif content_type == 'image/tiff':
                                fileName = f'temp/{cmd.channelId}.tiff'
                            elif content_type == 'image/gif':
                                fileName = f'temp/{cmd.channelId}.gif'
                            with open(fileName, 'wb') as handler:
                                handler.write(img_data)
                            embed = discord.Embed(
                                title=cmd.args
                            )
                            embed.set_image(url=f'attachment://{fileName[5:len(fileName)]}')
                            embed.set_footer(text=res['tags'])
                            os.remove(fileName)
                        except Exception as e:
                            LogCog.logDebug(f'Exception on rule: {e}')
                            await channel.send(getLocale("nothing", 0))
                    elif cmd.cmdType == 'time':
                        await channel.send(f'<t:{str(int(datetime.now().timestamp()))}>')
                    elif cmd.cmdType == 'weather':
                        nameOfCity = " ".join(cmd.args.split(" "))
                        lat, lon, nameOfCity = await getCoordinates(nameOfCity)
                        weather = await getWeather(lat, lon, nameOfCity, 2, 24, 0)
                        await channel.send(weather)
                    elif cmd.cmdType == 'weatherd':
                        nameOfCity = " ".join(cmd.args.split(" "))
                        lat, lon, nameOfCity = await getCoordinates(nameOfCity)
                        weather = await getWeather(lat, lon, nameOfCity, 1, 40, 0)
                        await channel.send(weather)
                    elif cmd.cmdType == 'say':
                        text = " ".join(cmd.args.split(" "))
                        if len(text) > 0:
                            await channel.send(text)
                        else:
                            await channel.send("Noting to say. Delete this commands and try it with args")
                    elif cmd.cmdType == 'currency':
                        loop = cmd.args.split()
                        fromValue = str(loop[0]).upper()
                        res = 1 / currency[fromValue]
                        i = 1
                        output = f'1{fromValue}'
                        while i < len(loop):
                            try:
                                toValue = str(loop[i]).upper()
                                i += 1
                                currentRes = res * currency[toValue]
                                output = f'{output}={round(currentRes, 4)}{toValue}'
                            except KeyError:
                                LogCog.logError(
                                    f'Wrong Key in currency autocmd. {channel.id}, values: {fromValue}->{toValue}')
                                return 0
                        await channel.send(output)
            except Exception as e:
                LogCog.logError(f'Exception in checkForCommands {e}')
