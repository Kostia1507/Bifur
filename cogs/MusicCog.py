import discord
from discord.ext import commands, tasks

from cogs import LogCog

from models.Song import Song
from service import musicService, pagedMessagesService
from service.localeService import getLocale

ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn',
}


async def is_in_vc(ctx):
    vc = ctx.guild.voice_client
    if vc is not None:
        members = vc.channel.members
        for member in members:
            if member.id == ctx.author.id:
                return True
    await ctx.send(getLocale('not-in-voice', ctx.author.id))
    return False


async def is_in_vcInteraction(interaction):
    vc = interaction.guild.voice_client
    if vc is not None:
        members = vc.channel.members
        for member in members:
            if member.id == interaction.user.id:
                return True
    await interaction.response.send_message(
        getLocale('not-in-voice', interaction.user.id), ephemeral=True, delete_after=15)
    return False


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
                            vc.play(discord.FFmpegPCMAudio(source=song.stream_url, **ffmpeg_options))
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
        # await createPlayer(ctx)

    @commands.command(aliases=['queue'])
    async def list(self, ctx):
        mp = musicService.findMusicPlayerByGuildId(ctx.guild.id)
        if mp is not None:
            ret = mp.formatList(ctx.author.id)
            pagedMsg = pagedMessagesService.initPagedMessage(self.bot, ret[0], ret[1])
            embed = discord.Embed(title=pagedMsg.title, description=pagedMsg.pages[0])
            embed.set_footer(text=f'Page 1 of {len(pagedMsg.pages)}')
            await ctx.send(embed=embed, view=pagedMsg.view)
