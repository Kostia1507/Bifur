import discord
from discord.ext import commands, tasks

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
    def __init__(self, options):
        super().__init__(timeout=None)
        self.add_item(DropdownMusic(options))


class DropdownMusic(discord.ui.Select):
    def __init__(self, options):
        super().__init__(placeholder='Select...', min_values=1, max_values=1,
                         options=options, custom_id='persistent_view:search_track_select')

    async def callback(self, interaction):
        n = int(self.values[0])
        res = await connect_to_user_voiceInteraction(interaction)
        if res == 0:
            return 0
        musicService.addSong(searchQueue[interaction.user.id][n], interaction.channel.guild.id,
                             interaction.user.name, interaction.channel.id)
        await musicViewService.createPlayer(interaction)
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
        self.checkMusicPlayers.start()
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
                            if song.stream_url is None:
                                song.updateFromWeb()
                            vc.play(discord.FFmpegPCMAudio(source=song.stream_url, **ffmpeg_options))
                            if mp.musicPlayerMessageId is not None:
                                await musicViewService.updatePlayer(mediaPlayer=mp, bot=self.bot)
                else:
                    LogCog.logDebug('delete player cause vc is None')
                    musicService.delete(guild.id)
            except Exception as e:
                LogCog.logError('check mp ' + str(e))
                mp.skip()

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
        await musicViewService.createPlayer(ctx)

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
        await ctx.send(embed=embed, view=MusicSelectView(options))

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
