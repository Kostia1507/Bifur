import asyncio
from datetime import datetime, time, timezone

import discord
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions

import config
from discordModels.views.AutoCmdView import AutoCmdView
from service.localeService import getLocale
from cogs import LogCog
from service.currencyService import currency
from service.customPrefixService import setPrefix, delPrefix
from cogs.WeatherCog import getCoordinates, getWeather
from service import pagedMessagesService, autoReactionService, ignoreService
from models.PendingCommand import PendingCommand, get_pending_command, get_pending_commands_by_channel, \
    get_all_pending_commands, delete_pending_command, check_execute

taskTimeConfig = [
    time(hour=0, minute=0, tzinfo=timezone.utc),
    time(hour=0, minute=30, tzinfo=timezone.utc),
    time(hour=1, minute=0, tzinfo=timezone.utc),
    time(hour=1, minute=30, tzinfo=timezone.utc),
    time(hour=2, minute=0, tzinfo=timezone.utc),
    time(hour=2, minute=30, tzinfo=timezone.utc),
    time(hour=3, minute=0, tzinfo=timezone.utc),
    time(hour=3, minute=30, tzinfo=timezone.utc),
    time(hour=4, minute=0, tzinfo=timezone.utc),
    time(hour=4, minute=30, tzinfo=timezone.utc),
    time(hour=5, minute=0, tzinfo=timezone.utc),
    time(hour=5, minute=30, tzinfo=timezone.utc),
    time(hour=6, minute=0, tzinfo=timezone.utc),
    time(hour=6, minute=30, tzinfo=timezone.utc),
    time(hour=7, minute=0, tzinfo=timezone.utc),
    time(hour=7, minute=30, tzinfo=timezone.utc),
    time(hour=8, minute=0, tzinfo=timezone.utc),
    time(hour=8, minute=30, tzinfo=timezone.utc),
    time(hour=9, minute=0, tzinfo=timezone.utc),
    time(hour=9, minute=30, tzinfo=timezone.utc),
    time(hour=10, minute=0, tzinfo=timezone.utc),
    time(hour=10, minute=30, tzinfo=timezone.utc),
    time(hour=11, minute=0, tzinfo=timezone.utc),
    time(hour=11, minute=30, tzinfo=timezone.utc),
    time(hour=12, minute=0, tzinfo=timezone.utc),
    time(hour=12, minute=30, tzinfo=timezone.utc),
    time(hour=13, minute=0, tzinfo=timezone.utc),
    time(hour=13, minute=30, tzinfo=timezone.utc),
    time(hour=14, minute=0, tzinfo=timezone.utc),
    time(hour=14, minute=30, tzinfo=timezone.utc),
    time(hour=15, minute=0, tzinfo=timezone.utc),
    time(hour=15, minute=30, tzinfo=timezone.utc),
    time(hour=16, minute=0, tzinfo=timezone.utc),
    time(hour=16, minute=30, tzinfo=timezone.utc),
    time(hour=17, minute=0, tzinfo=timezone.utc),
    time(hour=17, minute=30, tzinfo=timezone.utc),
    time(hour=18, minute=0, tzinfo=timezone.utc),
    time(hour=18, minute=30, tzinfo=timezone.utc),
    time(hour=19, minute=0, tzinfo=timezone.utc),
    time(hour=19, minute=30, tzinfo=timezone.utc),
    time(hour=20, minute=0, tzinfo=timezone.utc),
    time(hour=20, minute=30, tzinfo=timezone.utc),
    time(hour=21, minute=0, tzinfo=timezone.utc),
    time(hour=21, minute=30, tzinfo=timezone.utc),
    time(hour=22, minute=0, tzinfo=timezone.utc),
    time(hour=22, minute=30, tzinfo=timezone.utc),
    time(hour=23, minute=0, tzinfo=timezone.utc),
    time(hour=23, minute=30, tzinfo=timezone.utc),
]


class ServerAdministrationCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        asyncio.create_task(autoReactionService.init())
        asyncio.create_task(ignoreService.initFromDB())
        self.checkForCommands.start()
        LogCog.logSystem('Server Administration cog loaded')

    @commands.command()
    @has_permissions(manage_messages=True)
    async def autoreaction(self, ctx, emoji):
        await autoReactionService.add(ctx.channel.id, emoji)
        await ctx.message.add_reaction('✅')

    @commands.command()
    @has_permissions(manage_messages=True)
    async def removereactions(self, ctx):
        await autoReactionService.remove(ctx.channel.id)
        await ctx.message.add_reaction('✅')

    @commands.command()
    @has_permissions(manage_guild=True)
    async def setcmd(self, ctx, channel: discord.TextChannel):
        try:
            chnl = await ctx.guild.fetch_channel(channel.id)
            if chnl is not None:
                pc = PendingCommand(chnl.id, 1, datetime.now().hour, None, "")
                await pc.insert()
                await ctx.message.add_reaction('✅')
            else:
                await ctx.message.add_reaction('❌')
        except discord.errors.NotFound or discord.errors.DiscordServerError:
            await ctx.message.add_reaction('❌')

    @commands.command()
    @has_permissions(manage_guild=True)
    async def getcmds(self, ctx, channel: discord.TextChannel):
        cmds = await get_pending_commands_by_channel(channel.id)
        res = ""
        for cmd in cmds:
            res += f'ID: {cmd.id}; {cmd.cmdType}:{cmd.args}\n'
        if len(res) < 0:
            res = "List is empty. There is no auto-commands."
        await ctx.send(res)

    @commands.command()
    @has_permissions(manage_guild=True)
    async def editcmd(self, ctx, channel: discord.TextChannel, cmdId: int):
        cmd = await get_pending_command(cmdId)
        if cmd.channelId != channel.id:
            await ctx.message.add_reaction('❌')
        else:
            embed = discord.Embed(title="AutoCommand", description=f"Command: {cmd.cmdType}\n"
                                                                   f"Arguments: {cmd.args}\n"
                                                                   f"All autocommands is similar to usual cmds.\n"
                                                                   f"So if you need args, use it like any usual command in Bifur or read the docs\n"
                                                                   f"Start hour (UTC): {cmd.startHour}\n"
                                                                   f"Interval: {cmd.interval} hours\n")
            await ctx.channel.send(embed=embed, view=AutoCmdView(self.bot, cmd))

    @commands.command()
    @has_permissions(manage_guild=True)
    async def delcmd(self, ctx, channel: discord.TextChannel, cmdId: int):
        await delete_pending_command(channel.id, cmdId)
        await ctx.message.add_reaction('✅')

    @commands.command()
    @has_permissions(manage_guild=True)
    async def ignore(self, ctx, channel: discord.TextChannel):
        await ignoreService.manageIgnoredChannels(ctx, channel.id)

    @commands.command()
    @has_permissions(manage_guild=True)
    async def setprefix(self, ctx, prefix):
        await setPrefix(ctx.guild.id, prefix)
        await ctx.send(f'{getLocale("set-prefix", ctx.author.id)} {prefix}')

    @commands.command(aliases=['defaultprefix', 'delprefix'])
    @has_permissions(manage_guild=True)
    async def defprefix(self, ctx):
        await delPrefix(ctx.guild.id)
        await ctx.send(f'{getLocale("set-prefix", ctx.author.id)} {config.prefix}')

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

    @tasks.loop(time=taskTimeConfig)
    async def checkForCommands(self):
        is_execute = await check_execute()
        if not is_execute:
            return
        LogCog.logSystem('execute checkForCommands in ServerAdministrationCog')
        pcs = await get_all_pending_commands()
        currentHour = int(datetime.utcnow().hour)
        for cmd in pcs:
            try:
                channel = self.bot.get_channel(cmd.channelId)
                if (currentHour - cmd.startHour) % cmd.interval == 0:
                    if cmd.cmdType == 'time':
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
