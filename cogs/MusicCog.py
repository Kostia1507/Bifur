import asyncio
import copy
import os
import traceback
from datetime import datetime, timedelta

import discord
from discord import app_commands
from discord.ext import commands, tasks
from discord.utils import get

import config
from cogs import LogCog
from models.MusicPlayer import RepeatType, ColorTheme

from service import musicService, pagedMessagesService, musicViewService, likedSongsService, downloadSongService
from service.localeService import getLocale, getUserLang, getLocaleByLang
from utils import commandUtils

searchQueue = {}

ffmpeg_options = {
                'before_options': '-nostdin ',
                'options': '-vn',
                }

async def update_music_view(mp, bot):
    await asyncio.sleep(10)  # асинхронна затримка на 10 секунд
    await musicViewService.updatePlayer(mediaPlayer=mp, bot=bot)


def after_player(error):
    if error is not None:
        LogCog.logError("after_player" + str(error))


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
            await ctx.send(await getLocale('not-connected-to-voice', ctx.author.id))
            return 0


async def connect_to_user_voiceInteraction(interaction):
    if not interaction.guild.voice_client:
        if interaction.user.voice is not None:
            channel = interaction.user.voice.channel
            await channel.connect()
            return 1
        else:
            await interaction.response.send_message(
                await getLocale('not-connected-to-voice', interaction.user.id), ephemeral=True, delete_after=15)
            return 0


class MusicCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.emptyVoices = []
        self.checkMusicPlayers.start()
        self.checkForEmptyVoices.start()
        self.deleteOldFiles.start()
        # Bot will skip iteration if previous wasn't finished
        self.canCheckMusicAgain = True
        LogCog.logSystem("MusicCog started")

    @tasks.loop(seconds=2)
    async def checkMusicPlayers(self):
        if self.canCheckMusicAgain:
            self.canCheckMusicAgain = False
            check_players = musicService.players.copy()  # окремий лист, щоб не збив процес інший асинхронний процес
            for mp in check_players.values():
                try:
                    guild = self.bot.get_guild(mp.guildId)
                    if guild.voice_client:
                        vc = guild.voice_client
                        if (vc.is_connected() and not vc.is_playing() and not vc.is_paused()
                                and datetime.now() - mp.playCooldown > timedelta(seconds=10)) and not mp.checked:
                            mp.checked = True
                            song = mp.getNext()
                            if song is not None:
                                error = None
                                if song.stream_url is None or datetime.now() - song.updated >= timedelta(hours=5):
                                    error = await song.updateFromWeb()
                                if error is not None:
                                    embed = discord.Embed(title="Error", description=str(error),
                                                          color=discord.Color.red())
                                    if song.name is not None:
                                        embed.set_footer(text=f"{song.name} {song.original_url}")
                                    else:
                                        embed.set_footer(text=song.original_url)
                                    channel = await self.bot.fetch_channel(mp.channelId)
                                    await channel.send(embed=embed)
                                    mp.skip(saveIfRepeating=False)
                                else:
                                    file = await downloadSongService.get_file_by_url(song.original_url)
                                    if file is not None:
                                        source = discord.PCMVolumeTransformer(
                                            discord.FFmpegPCMAudio(file.filename, **ffmpeg_options),
                                            volume=mp.volume / 100)
                                        vc.play(source, after=after_player)
                                        mp.playCooldown = datetime.now()
                                        if mp.musicPlayerMessageId is not None:
                                            await musicViewService.updatePlayer(mediaPlayer=mp, bot=self.bot)
                                            await asyncio.create_task(update_music_view(mp, self.bot))
                                        await mp.tryPredownload()
                            mp.checked = False
                    else:
                        musicService.delete(guild.id)
                except Exception as e:
                    mp.checked = False
                    LogCog.logError('check mp ' + str(e))
                    traceback.print_exception(type(e), e, e.__traceback__)
                    mp.skip()
            self.canCheckMusicAgain = True

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

    @tasks.loop(minutes=config.delete_songs_after_hours*15)
    async def deleteOldFiles(self):
        loopArr = list(downloadSongService.filesArr.keys())
        for url in loopArr:
            if downloadSongService.filesArr[url].download_time + timedelta(hours=config.delete_songs_after_hours) < datetime.now():
                try:
                    os.remove(downloadSongService.filesArr[url].filename)
                    del downloadSongService.filesArr[url]
                except (FileNotFoundError, PermissionError) as e:
                    LogCog.logError(f'{downloadSongService.filesArr[url].filename} cant delete cause {str(e)}')


    # need to be tested
    # this function must return bot to voice channel if he was disconnected not by user
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel is not None and after.channel is None and member.id == self.bot.user.id:
            # Wait for reconnecting
            await asyncio.sleep(7)
            vc = get(self.bot.voice_clients, guild=before.channel.guild)
            if vc is not None and vc.is_connected() and before.channel.guild.id in musicService.players.keys():
                mp = musicService.players[before.channel.guild.id]
                if mp is not None:
                    LogCog.logSystem(
                        f'I was disconnected by Discord... reconnecting to guild {before.channel.guild.id}')
                    song = mp.getNext()
                    if song is not None:
                        LogCog.logDebug(f'Song is not None {before.channel.guild.id}')
                        error = None
                        if song.stream_url is None or datetime.now() - song.updated >= timedelta(hours=5):
                            error = await song.updateFromWeb()
                        if error is not None:
                            embed = discord.Embed(title="Error", description=str(error), color=discord.Color.red())
                            if song.name is not None:
                                embed.set_footer(text=f"{song.name} {song.original_url}")
                            else:
                                embed.set_footer(text=song.original_url)
                            channel = await self.bot.fetch_channel(mp.channelId)
                            await channel.send(embed=embed)
                            mp.skip(saveIfRepeating=False)
                        else:
                            file = await downloadSongService.get_file_by_url(song.original_url)
                            if file is not None:
                                source = discord.PCMVolumeTransformer(
                                    discord.FFmpegPCMAudio(file.filename),
                                    volume=mp.volume / 100)
                                vc.play(source, after=after_player)
                                if mp.musicPlayerMessageId is not None:
                                    await musicViewService.updatePlayer(mediaPlayer=mp, bot=self.bot)
                    mp.checked = False
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

        if await musicService.addTrack(loop.strip(), ctx.guild.id, ctx.author.name, ctx.channel.id):
            await ctx.message.add_reaction('✅')
        else:
            await ctx.message.add_reaction('❌')
        await musicViewService.createPlayer(ctx, self.bot)

    @commands.command(aliases=['queue'])
    async def list(self, ctx):
        mp = musicService.findMusicPlayerByGuildId(ctx.guild.id)
        if mp is not None:
            ret = await mp.formatList(ctx.author.id)
            pagedMsg = pagedMessagesService.initPagedMessage(self.bot, ret[0], ret[1])
            embed = discord.Embed(title=pagedMsg.title, description=pagedMsg.pages[0])
            embed.set_footer(text=f'Page 1 of {len(pagedMsg.pages)}')
            await ctx.send(embed=embed, view=pagedMsg.view)

    @commands.command()
    async def history(self, ctx):
        mp = musicService.findMusicPlayerByGuildId(ctx.guild.id)
        if mp is not None:
            ret = await mp.formatHistory(ctx.author.id)
            pagedMsg = pagedMessagesService.initPagedMessage(self.bot, "History", ret)
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
        elif len(args) >= 2:
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
            await ctx.send(await getLocale('repeat-off', ctx.author.id))
        elif musicService.getMusicPlayer(ctx.guild.id, ctx.channel.id).repeating == RepeatType.REPEAT_ONE:
            await ctx.send(await getLocale('repeat-one', ctx.author.id))
        else:
            await ctx.send(await getLocale('repeat-on', ctx.author.id))

    @commands.command()
    async def current(self, ctx):
        t = musicService.getMusicPlayer(ctx.guild.id, ctx.channel.id).getPlaying()
        userLang = await getUserLang(ctx.author.id)
        if t is not None:
            embed = discord.Embed(
                title=f'{getLocaleByLang("playing", userLang)} {t.name}',
                description=f'{getLocaleByLang("ordered", userLang)} {t.author}\n'
                            f'{getLocaleByLang("duration", userLang)} {t.getDurationToStr()}')
            embed.set_thumbnail(url=t.icon_link)
            embed.set_footer(text=t.link)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title=f'{getLocaleByLang("playing", userLang)} {getLocaleByLang("nothing", userLang)}'
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
        tList = await musicService.searchFive(loop)
        if tList is not None and len(tList) > 0:
            searchQueue[ctx.message.author.id] = tList
            options = []
            text = ''
            for i in range(0, len(tList)):
                options.append(
                    discord.SelectOption(label=f"{i + 1}. {tList[i].name[0:80]} ({tList[i].getDurationToStr()})",
                                         value=str(i)))
                text += f'{i + 1}. {tList[i].name} ({tList[i].getDurationToStr()})\n'
            embed = discord.Embed(
                title=await getLocale("result", ctx.author.id),
                description=text
            )
            await ctx.send(embed=embed, view=MusicSelectView(options, self.bot))
        else:
            await ctx.send(await getLocale("nothing-found", ctx.author.id))

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
        musicService.getMusicPlayer(ctx.guild.id, ctx.channel.id).songs = []
        await ctx.message.add_reaction('✅')

    @commands.command()
    @commands.check(commandUtils.is_in_vc)
    async def pause(self, ctx):
        if ctx.message.guild.voice_client:
            ctx.message.guild.voice_client.pause()
            mp = musicService.findMusicPlayerByGuildId(ctx.guild.id)
            if mp is not None:
                mp.isStopped = True
                await musicViewService.updatePlayer(mp, self.bot)
            await ctx.message.add_reaction('✅')

    @commands.command()
    @commands.check(commandUtils.is_in_vc)
    async def resume(self, ctx):
        if ctx.message.guild.voice_client:
            ctx.message.guild.voice_client.resume()
            mp = musicService.findMusicPlayerByGuildId(ctx.guild.id)
            if mp is not None:
                mp.isStopped = False
                await musicViewService.updatePlayer(mp, self.bot)
            await ctx.message.add_reaction('✅')

    @commands.command(aliases=["dwlmp3"])
    async def downloadmp3(self, ctx, url):
        filename = await musicService.downloadVideo(url)
        await ctx.send(file=discord.File(filename))
        os.remove(filename)

    @commands.command()
    @commands.check(commandUtils.is_in_vc)
    async def player(self, ctx, *args):
        mp = musicService.getMusicPlayer(ctx.guild.id, ctx.channel.id)
        if len(args) > 0:
            theme = musicViewService.getThemeFromStr(args[0])
            if theme is not None:
                mp.theme = theme
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

    @commands.command()
    async def like(self, ctx, url):
        if await likedSongsService.likeSong(ctx.author.id, url):
            await ctx.message.add_reaction('✅')
        else:
            await ctx.message.add_reaction('❌')

    @commands.command()
    async def unlike(self, ctx, song_id: int):
        if await likedSongsService.unlikeSong(ctx.author.id, song_id):
            await ctx.message.add_reaction('✅')
        else:
            await ctx.message.add_reaction('❌')

    @commands.command(aliases=["likedsongs", "likedlist"])
    async def liked(self, ctx):
        songs = await likedSongsService.getAllLikedSongs(ctx.author.id)
        ret = ""
        for song in songs:
            ret += f'{song.trackId} - {song.name}\n'
        pagedMsg = pagedMessagesService.initPagedMessage(self.bot, await getLocale('favourite', ctx.author.id), ret)
        embed = discord.Embed(title=pagedMsg.title, description=pagedMsg.pages[0])
        embed.set_footer(text=f'Page 1 of {len(pagedMsg.pages)}')
        await ctx.send(embed=embed, view=pagedMsg.view)

    @commands.command()
    async def linfo(self, ctx, track_id: int):
        song = await likedSongsService.getLikedSongById(ctx.author.id, track_id)
        if song is not None:
            await song.updateFromWeb()
            embed = discord.Embed(
                title=f'{song.name}',
                description=f'URL: {song.original_url}\n{await getLocale("duration", ctx.author.id)} {song.getDurationToStr()}'
            )
            embed.set_thumbnail(url=song.icon_link)
            await ctx.send(embed=embed)

    @commands.command(aliases=["pliked"])
    async def playliked(self, ctx):
        res = await connect_to_user_voice(ctx)
        if res == 0:
            return 0
        await musicViewService.createPlayer(ctx, self.bot)
        retStatus = musicService.startLiked(ctx.guild.id, ctx.author.name,
                                            ctx.channel.id, ctx.author.id, True)
        if retStatus:
            await ctx.message.add_reaction('✅')
        else:
            await ctx.message.add_reaction('❌')

    @app_commands.command(name="play", description="Play songs")
    @app_commands.describe(query="video title on youtube")
    async def playSlash(self, interaction: discord.Interaction, query: str):
        if query is not None and len(query) > 0:
            await interaction.response.defer()
            res = await connect_to_user_voiceInteraction(interaction)
            if res == 0:
                return 0
            await musicService.addTrack(query.strip(), interaction.guild.id, interaction.user.name, interaction.channel.id)
            res = await musicViewService.createPlayer(interaction, self.bot)
            if not res:
                await interaction.followup.send(await getLocale('ready', interaction.user.id), ephemeral=True)
        else:
            await interaction.followup.send(await getLocale("nothing-found", interaction.user.id), ephemeral=True)

    @app_commands.command(name="search", description="Let you choose one from 5 songs")
    @app_commands.describe(query="video title on youtube")
    async def searchSlash(self, interaction: discord.Interaction, query: str):
        await interaction.response.defer()
        tList = await musicService.searchFive(query)
        if len(tList) > 0:
            searchQueue[interaction.user.id] = tList
            options = []
            text = ''
            for i in range(0, len(tList)):
                options.append(
                    discord.SelectOption(label=f"{i + 1}. {tList[i].name[0:80]} ({tList[i].getDurationToStr()})",
                                         value=str(i)))
                text += f'{i + 1}. {tList[i].name} ({tList[i].getDurationToStr()})\n'
            embed = discord.Embed(
                title=await getLocale("result", interaction.user.id),
                description=text
            )
            await interaction.followup.send(embed=embed, view=MusicSelectView(options, self.bot))
        else:
            await interaction.followup.send(await getLocale("nothing-found", interaction.user.id), ephermal=True)

    @app_commands.command(name="list", description="List of songs in queue")
    async def listSlash(self, interaction: discord.Interaction):
        mp = musicService.findMusicPlayerByGuildId(interaction.guild.id)
        if mp is not None:
            ret = await mp.formatList(interaction.user.id)
            pagedMsg = pagedMessagesService.initPagedMessage(self.bot, ret[0], ret[1])
            embed = discord.Embed(title=pagedMsg.title, description=pagedMsg.pages[0])
            embed.set_footer(text=f'Page 1 of {len(pagedMsg.pages)}')
            await interaction.response.send_message(embed=embed, view=pagedMsg.view)

    @app_commands.command(name="shuffle", description="Shuffle songs in queue")
    async def shuffleSlash(self, interaction: discord.Interaction):
        if commandUtils.is_in_vcInteraction(interaction):
            musicService.getMusicPlayer(interaction.guild_id, interaction.channel_id).shuffle()
            await interaction.response.send_message(await getLocale('ready', interaction.user.id),
                                                    ephemeral=True, delete_after=15)

    @app_commands.command(name="skip", description="Skip current song")
    async def skipSlash(self, interaction: discord.Interaction):
        if commandUtils.is_in_vcInteraction(interaction):
            guild = interaction.guild
            if guild.voice_client:
                vc = guild.voice_client.stop()
                musicService.getMusicPlayer(interaction.guild_id, interaction.channel_id).skip()
                await interaction.response.send_message(await getLocale('ready', interaction.user.id),
                                                        ephemeral=True, delete_after=15)

    @app_commands.command(name="previous", description="Return to previous song")
    async def previousSlash(self, interaction: discord.Interaction):
        guild = interaction.guild
        if guild.voice_client:
            musicService.getMusicPlayer(guild.id, interaction.channel.id).toPrevious()
            guild.voice_client.stop()
            await interaction.response.send_message(await getLocale('ready', interaction.user.id),
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
                await interaction.response.send_message(await getLocale('ready', interaction.user.id),
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
                    await getLocale('repeat-off', interaction.user.id), ephemeral=True, delete_after=15)
            elif mp.repeating == RepeatType.REPEAT_ONE:
                await interaction.response.send_message(
                    await getLocale('repeat-one', interaction.user.id), ephemeral=True, delete_after=15)
            else:
                await interaction.response.send_message(
                    await getLocale('repeat-on', interaction.user.id), ephemeral=True, delete_after=15)

    @app_commands.command(name="volume", description="Set volume between 0 and 200")
    @app_commands.describe(volume="value between 0% and 200%")
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
            await interaction.followup.send(await getLocale('ready', interaction.user.id), ephemeral=True)

    @app_commands.command(name="player", description="Recreate player with buttons")
    @app_commands.describe(theme="change color of buttons")
    async def playerSlash(self, interaction: discord.Interaction, theme: ColorTheme = ColorTheme.GRAY):
        if await commandUtils.is_in_vcInteraction(interaction):
            mp = musicService.getMusicPlayer(interaction.guild_id, interaction.channel_id)
            if theme is not None:
                mp.theme = theme
            if mp.musicPlayerMessageId is not None:
                message = await self.bot.get_channel(mp.musicPlayerChannelId) \
                    .fetch_message(mp.musicPlayerMessageId)
                await message.delete()
            mp.musicPlayerMessageId = None
            await musicViewService.createPlayer(interaction, self.bot)
