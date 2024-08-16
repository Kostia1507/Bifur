import asyncio
import os
from datetime import datetime, timedelta

import discord
from discord import app_commands
from discord.ext import commands, tasks
from discord.utils import get

from cogs import LogCog
from models.MusicPlayer import RepeatType

from service import musicService, pagedMessagesService, musicViewService
from service.localeService import getLocale
from utils import commandUtils

ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn',
}

searchQueue = {}


class MusicSelectView(discord.ui.View):
    def __init__(self, options, bot):
        super().__init__(timeout=None)
        self.add_item(DropdownMusic(options, bot))


class DropdownMusic(discord.ui.Select):
    def __init__(self, options, bot):
        super().__init__(placeholder='Select...', min_values=1, max_values=1,
                         options=options, custom_id='persistent_view:search_track_select')
        self.bot = bot

    async def callback(self, interaction):
        n = int(self.values[0])
        res = await connect_to_user_voiceInteraction(interaction)
        if res == 0:
            return 0
        musicService.addSong(searchQueue[interaction.user.id][n], interaction.channel.guild.id,
                             interaction.user.name, interaction.channel.id)
        await musicViewService.createPlayer(interaction, self.bot)
        if not interaction.response.is_done():
            await interaction.response.send_message('✅', ephemeral=True)


async def connect_to_user_voice(ctx):
    if not ctx.guild.voice_client:
        if ctx.message.author.voice is not None:
            channel = ctx.message.author.voice.channel
            await channel.connect()
            return 1
        else:
            await ctx.send(getLocale('not-connected-to-voice', ctx.author.id))
            return 0


async def connect_to_user_voiceInteraction(interaction):
    if not interaction.guild.voice_client:
        if interaction.user.voice is not None:
            channel = interaction.user.voice.channel
            await channel.connect()
            return 1
        else:
            await interaction.response.send_message(
                getLocale('not-connected-to-voice', interaction.user.id), ephemeral=True, delete_after=15)
            return 0


class MusicCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.emptyVoices = []
        self.checkMusicPlayers.start()
        self.checkForEmptyVoices.start()
        LogCog.logSystem("MusicCog started")

    @tasks.loop(seconds=2)
    async def checkMusicPlayers(self):
        check_players = musicService.players.copy()  # окремий лист, щоб не збив процес інший асинхронний процес
        for mp in check_players.values():
            try:
                guild = self.bot.get_guild(mp.guildId)
                if guild.voice_client:
                    vc = guild.voice_client
                    if vc.is_connected() and not vc.is_playing() and not vc.is_paused():
                        song = mp.getNext()
                        if song is not None:
                            if song.stream_url is None or datetime.now() - song.updated >= timedelta(hours=1):
                                LogCog.logDebug("update song")
                                song.updateFromWeb()
                            if song.stream_url is None:
                                mp.skip()
                            else:
                                source = discord.PCMVolumeTransformer(
                                    discord.FFmpegPCMAudio(song.stream_url, **ffmpeg_options), volume=mp.volume/100)
                                vc.play(source)
                                if mp.musicPlayerMessageId is not None:
                                    await musicViewService.updatePlayer(mediaPlayer=mp, bot=self.bot)
                else:
                    musicService.delete(guild.id)
            except Exception as e:
                LogCog.logError('check mp ' + str(e))
                mp.skip()

    @tasks.loop(minutes=5)
    async def checkForEmptyVoices(self):
        for vc in self.bot.voice_clients:
            if len(vc.channel.members) < 2:
                if vc.channel.id in self.emptyVoices:
                    self.emptyVoices.remove(vc.channel.id)
                    LogCog.logSystem(f'leave from voice {vc.channel.id} cause members < 2')
                    await vc.disconnect()
                    mp = musicService.findMusicPlayerByGuildId(vc.channel.guild.id)
                    if mp is not None and mp.musicPlayerMessageId is not None:
                        message = await self.bot.get_channel(mp.musicPlayerChannelId) \
                            .fetch_message(mp.musicPlayerMessageId)
                        await message.delete()
                    musicService.delete(vc.channel.guild.id)
                else:
                    # Add to query for leaving
                    self.emptyVoices.append(vc.channel.id)
            elif vc.channel.id in self.emptyVoices:
                self.emptyVoices.remove(vc.channel.id)

    # need to be tested
    # this function must return bot to voice channel if he was disconnected not by user
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel is not None and after.channel is None and member.id == self.bot.user.id:
            # Wait for reconnecting
            await asyncio.sleep(7)
            vc = get(self.bot.voice_clients, guild=before.channel.guild)
            if vc is not None and vc.is_connected():
                mp = musicService.players[before.channel.guild.id]
                if mp is not None:
                    LogCog.logSystem(
                        f'I was disconnected buy Discord... reconnecting to guild {before.channel.guild.id}')
                    song = mp.getNext()
                    if song is not None:
                        if song.stream_url is None:
                            song.updateFromWeb()
                        vc.play(discord.FFmpegPCMAudio(source=song.stream_url, **ffmpeg_options))
                        if mp.musicPlayerMessageId is not None:
                            await musicViewService.updatePlayer(mediaPlayer=mp, bot=self.bot)
            else:
                # User kicked me so I will delete all his data
                musicService.delete(before.channel.guild.id)
                LogCog.logSystem(f'Delete player for {before.channel.guild.id} cause I was disconnected')

    @commands.command(aliases=['p'])
    async def play(self, ctx, *args):
        res = await connect_to_user_voice(ctx)
        if res == 0:
            return 0
        loop = ' '.join(args)
        if musicService.addTrack(loop.strip(), ctx.guild.id, ctx.author.name, ctx.channel.id):
            await ctx.message.add_reaction('✅')
        else:
            await ctx.message.add_reaction('❌')
        await musicViewService.createPlayer(ctx, self.bot)

    @commands.command(aliases=['queue'])
    async def list(self, ctx):
        mp = musicService.findMusicPlayerByGuildId(ctx.guild.id)
        if mp is not None:
            ret = mp.formatList(ctx.author.id)
            pagedMsg = pagedMessagesService.initPagedMessage(self.bot, ret[0], ret[1])
            embed = discord.Embed(title=pagedMsg.title, description=pagedMsg.pages[0])
            embed.set_footer(text=f'Page 1 of {len(pagedMsg.pages)}')
            await ctx.send(embed=embed, view=pagedMsg.view)

    @commands.command()
    @commands.check(commandUtils.is_in_vc)
    async def skip(self, ctx, *args):
        guild = ctx.guild
        if guild.voice_client:
            if len(args) > 0:
                musicService.getMusicPlayer(ctx.guild.id, ctx.channel.id).skipLine(int(args[0]))
            musicService.getMusicPlayer(ctx.guild.id, ctx.channel.id).skip()
            guild.voice_client.stop()
            await ctx.message.add_reaction('✅')

    @commands.command()
    @commands.check(commandUtils.is_in_vc)
    async def previous(self, ctx):
        guild = ctx.guild
        if guild.voice_client:
            musicService.getMusicPlayer(ctx.guild.id, ctx.channel.id).toPrevious()
            guild.voice_client.stop()
            await ctx.message.add_reaction('✅')

    @commands.command()
    @commands.check(commandUtils.is_in_vc)
    async def stop(self, ctx):
        mp = musicService.getMusicPlayer(ctx.guild.id, ctx.channel.id)
        mp.songs = []
        mp.repeating = RepeatType.NOT_REPEATING
        if ctx.guild.voice_client:
            vc = ctx.guild.voice_client
            musicService.getMusicPlayer(ctx.guild.id, ctx.channel.id).skip()
            vc.stop()
            await ctx.message.add_reaction('✅')

    @commands.command()
    @commands.check(commandUtils.is_in_vc)
    async def remove(self, ctx, *args):
        if len(args) == 1:
            musicService.getMusicPlayer(ctx.guild.id, ctx.channel.id).remove(args[0])
            await ctx.message.add_reaction('✅')
        else:
            musicService.getMusicPlayer(ctx.guild.id, ctx.channel.id).removeLine(args[0], args[1])
            await ctx.message.add_reaction('✅')

    @commands.command()
    @commands.check(commandUtils.is_in_vc)
    async def repeat(self, ctx, *args):
        changed = False
        if len(args) > 0:
            if args[0] == "all" or args[0] == "on":
                musicService.getMusicPlayer(ctx.guild.id, ctx.channel.id).repeating = RepeatType.REPEAT_ALL
                changed = True
            if args[0] == "one":
                musicService.getMusicPlayer(ctx.guild.id, ctx.channel.id).repeating = RepeatType.REPEAT_ONE
                changed = True
            if args[0] == "off":
                musicService.getMusicPlayer(ctx.guild.id, ctx.channel.id).repeating = RepeatType.NOT_REPEATING
                changed = True
        if not changed:
            if musicService.getMusicPlayer(ctx.guild.id, ctx.channel.id).repeating != RepeatType.NOT_REPEATING:
                musicService.getMusicPlayer(ctx.guild.id, ctx.channel.id).repeating = RepeatType.NOT_REPEATING
            else:
                musicService.getMusicPlayer(ctx.guild.id, ctx.channel.id).repeating = RepeatType.REPEAT_ALL
        if musicService.getMusicPlayer(ctx.guild.id, ctx.channel.id).repeating == RepeatType.NOT_REPEATING:
            await ctx.send(getLocale('repeat-off', ctx.author.id))
        elif musicService.getMusicPlayer(ctx.guild.id, ctx.channel.id).repeating == RepeatType.REPEAT_ONE:
            await ctx.send(getLocale('repeat-one', ctx.author.id))
        else:
            await ctx.send(getLocale('repeat-on', ctx.author.id))

    @commands.command()
    async def current(self, ctx):
        t = musicService.getMusicPlayer(ctx.guild.id, ctx.channel.id).getPlaying()
        if t is not None:
            embed = discord.Embed(
                title=f'{getLocale("playing", ctx.author.id)} {t.name}',
                description=f'{getLocale("ordered", ctx.author.id)} {t.author}\n'
                            f'{getLocale("duration", ctx.author.id)} {t.getDurationToStr()}')
            embed.set_thumbnail(url=t.icon_link)
            embed.set_footer(text=t.link)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title=f'{getLocale("playing", ctx.author.id)} {getLocale("nothing", ctx.author.id)}'
            )
            await ctx.send(embed=embed)

    @commands.command()
    async def reset(self, ctx):
        musicService.delete(ctx.message.channel.guild.id)
        await ctx.message.add_reaction('✅')

    @commands.command()
    async def join(self, ctx):
        ret = await connect_to_user_voice(ctx)
        if ret == 1:
            await ctx.message.add_reaction('✅')

    @commands.command(aliases=['leave'])
    @commands.check(commandUtils.is_in_vc)
    async def exit(self, ctx):
        if ctx.message.guild.voice_client:
            await ctx.message.guild.voice_client.disconnect()

    @commands.command()
    async def search(self, ctx, *args):
        await ctx.message.add_reaction('✅')
        loop = ' '.join(args)
        tList = musicService.searchFive(loop)
        searchQueue[ctx.message.author.id] = tList
        options = []
        text = ''
        for i in range(0, len(tList)):
            options.append(discord.SelectOption(label=f"{i + 1}. {tList[i].name[0:80]} ({tList[i].getDurationToStr()})",
                                                value=str(i)))
            text += f'{i + 1}. {tList[i].name} ({tList[i].getDurationToStr()})\n'
        embed = discord.Embed(
            title=getLocale("result", ctx.author.id),
            description=text
        )
        await ctx.send(embed=embed, view=MusicSelectView(options, self.bot))

    @commands.command()
    @commands.check(commandUtils.is_in_vc)
    async def shuffle(self, ctx):
        retStatus = musicService.getMusicPlayer(ctx.guild.id, ctx.channel.id).shuffle()
        if retStatus:
            await ctx.message.add_reaction('✅')
        else:
            await ctx.message.add_reaction('❌')

    @commands.command(aliases=['mclean'])
    @commands.check(commandUtils.is_in_vc)
    async def mclear(self, ctx):
        musicService.getMusicPlayer(ctx.guild.id, ctx.channel.id).clearTrackList()
        await ctx.message.add_reaction('✅')

    @commands.command()
    @commands.check(commandUtils.is_in_vc)
    async def pause(self, ctx):
        if ctx.message.guild.voice_client:
            ctx.message.guild.voice_client.pause()
            await ctx.message.add_reaction('✅')

    @commands.command()
    @commands.check(commandUtils.is_in_vc)
    async def resume(self, ctx):
        if ctx.message.guild.voice_client:
            ctx.message.guild.voice_client.resume()
            await ctx.message.add_reaction('✅')

    @commands.command(aliases=["dwlmp3"])
    async def downloadmp3(self, ctx, url):
        filename = musicService.downloadVideo(url)
        await ctx.send(file=discord.File(filename))
        os.remove(filename)

    @commands.command()
    @commands.check(commandUtils.is_in_vc)
    async def player(self, ctx):
        mp = musicService.getMusicPlayer(ctx.guild.id, ctx.channel.id)
        if mp.musicPlayerMessageId is not None:
            message = await self.bot.get_channel(mp.musicPlayerChannelId) \
                .fetch_message(mp.musicPlayerMessageId)
            await message.delete()
        mp.musicPlayerMessageId = None
        await musicViewService.createPlayer(ctx, self.bot)

    @commands.command()
    @commands.check(commandUtils.is_in_vc)
    async def volume(self, ctx, volume: int):
        mp = musicService.getMusicPlayer(ctx.guild.id, ctx.channel.id)
        if mp is not None and ctx.voice_client is not None and 0 <= volume <= 200:
            mp.volume = volume
            if ctx.voice_client.source is not None:
                ctx.voice_client.source.volume = volume / 100
            if mp.musicPlayerChannelId is not None:
                await musicViewService.updatePlayer(mediaPlayer=mp, bot=self.bot)
            await ctx.message.add_reaction('✅')
        else:
            await ctx.message.add_reaction('❌')

    @app_commands.command(name="play", description="Play songs")
    async def playSlash(self, interaction: discord.Interaction, name: str):
        res = await connect_to_user_voiceInteraction(interaction)
        if res == 0:
            return 0
        await musicService.addTrack(name.strip(), interaction.guild.id, interaction.user.name, interaction.channel.id)
        await interaction.response.send_message(getLocale('ready', interaction.user.id),
                                                ephemeral=True, delete_after=15)
        await musicViewService.createPlayer(interaction, self.bot)

    @app_commands.command(name="search", description="Let you choose one from 5 songs")
    async def searchSlash(self, interaction: discord.Interaction, search: str):
        await interaction.response.defer(ephemeral=True, thinking=True)
        tList = musicService.searchFive(search)
        searchQueue[interaction.user.id] = tList
        options = []
        text = ''
        for i in range(0, len(tList)):
            options.append(discord.SelectOption(label=f"{i + 1}. {tList[i].name[0:80]} ({tList[i].getDurationToStr()})",
                                                value=str(i)))
            text += f'{i + 1}. {tList[i].name} ({tList[i].getDurationToStr()})\n'
        embed = discord.Embed(
            title=getLocale("result", interaction.user.id),
            description=text
        )
        await interaction.followup.send(embed=embed, view=MusicSelectView(options, self.bot))

    @app_commands.command(name="list", description="List of songs in queue")
    async def listSlash(self, interaction: discord.Interaction):
        mp = musicService.findMusicPlayerByGuildId(interaction.guild.id)
        if mp is not None:
            ret = mp.formatList(interaction.user.id)
            pagedMsg = pagedMessagesService.initPagedMessage(self.bot, ret[0], ret[1])
            embed = discord.Embed(title=pagedMsg.title, description=pagedMsg.pages[0])
            embed.set_footer(text=f'Page 1 of {len(pagedMsg.pages)}')
            await interaction.response.send_message(embed=embed, view=pagedMsg.view)

    @app_commands.command(name="shuffle", description="Shuffle songs in queue")
    async def shuffleSlash(self, interaction: discord.Interaction):
        if commandUtils.is_in_vcInteraction(interaction):
            musicService.getMusicPlayer(interaction.guild_id, interaction.channel_id).shuffle()
            await interaction.response.send_message(getLocale('ready', interaction.user.id),
                                                    ephemeral=True, delete_after=15)

    @app_commands.command(name="skip", description="Skip current song")
    async def skipSlash(self, interaction: discord.Interaction):
        if commandUtils.is_in_vcInteraction(interaction):
            guild = interaction.guild
            if guild.voice_client:
                vc = guild.voice_client.stop()
                musicService.getMusicPlayer(interaction.guild_id, interaction.channel_id).skip()
                await interaction.response.send_message(getLocale('ready', interaction.user.id),
                                                        ephemeral=True, delete_after=15)

    @app_commands.command(name="previous", description="Return to previous song")
    async def previousSlash(self, interaction: discord.Interaction):
        guild = interaction.guild
        if guild.voice_client:
            musicService.getMusicPlayer(guild.id, interaction.channel.id).toPrevious()
            guild.voice_client.stop()
            await interaction.response.send_message(getLocale('ready', interaction.user.id),
                                                    ephemeral=True, delete_after=15)

    @app_commands.command(name="stop", description="Stop all songs in queue")
    async def stopSlash(self, interaction: discord.Interaction):
        if commandUtils.is_in_vcInteraction(interaction):
            mp = musicService.getMusicPlayer(interaction.guild_id, interaction.channel_id)
            mp.clearTrackList()
            mp.repeating = 0
            if interaction.guild.voice_client:
                vc = interaction.guild.voice_client
                t = musicService.getMusicPlayer(interaction.guild.id, interaction.channel.id).playing
                if t is not None:
                    t.delete()
                musicService.getMusicPlayer(interaction.guild_id, interaction.channel_id).skip()
                vc.stop()
                await interaction.response.send_message(getLocale('ready', interaction.user.id),
                                                        ephemeral=True, delete_after=15)

    @app_commands.command(name="repeat", description="Switch repeat mode")
    async def repeatSlash(self, interaction: discord.Interaction):
        if await commandUtils.is_in_vcInteraction(interaction):
            mp = musicService.getMusicPlayer(interaction.guild_id, interaction.channel_id)
            repeatN = mp.repeating.value - 1
            if repeatN == -1:
                repeatN = 2
            mp.repeating = RepeatType(repeatN)
            if mp.repeating == RepeatType.NOT_REPEATING:
                await interaction.response.send_message(
                    getLocale('repeat-off', interaction.user.id), ephemeral=True, delete_after=15)
            elif mp.repeating == RepeatType.REPEAT_ONE:
                await interaction.response.send_message(
                    getLocale('repeat-one', interaction.user.id), ephemeral=True, delete_after=15)
            else:
                await interaction.response.send_message(
                    getLocale('repeat-on', interaction.user.id), ephemeral=True, delete_after=15)

    @app_commands.command(name="volume", description="Set volume between 0 and 200")
    @commands.check(commandUtils.is_in_vc)
    async def volumeSlash(self, interaction: discord.Interaction, volume: int):
        await interaction.response.defer(ephemeral=True, thinking=True)
        mp = musicService.getMusicPlayer(interaction.guild.id, interaction.channel.id)
        vc = interaction.guild.voice_client
        if mp is not None and vc is not None and 0 <= volume <= 200:
            mp.volume = volume
            if vc.source is not None:
                vc.source.volume = volume / 100
            if mp.musicPlayerChannelId is not None:
                await musicViewService.updatePlayer(mediaPlayer=mp, bot=self.bot)
            await interaction.followup.send(getLocale('ready', interaction.user.id), ephemeral=True)
