import discord

import config
from models.MusicPlayer import RepeatType
from service import musicService, musicViewService, likedSongsService
from service.localeService import getLocale

VOLUME_CHANGE_ON_CLICK = 20


async def is_in_vcInteraction(interaction):
    vc = interaction.guild.voice_client
    if vc is not None:
        members = vc.channel.members
        for member in members:
            if member.id == interaction.user.id:
                return True
    await interaction.response.send_message(
        await getLocale('not-in-voice', interaction.user.id), ephemeral=True, delete_after=15)
    return False


class MusicViewBlue(discord.ui.View):

    def __init__(self, bot, guildId):
        super().__init__(timeout=None)

        # init pause button
        for child in self.children:
            if isinstance(child, discord.ui.Button):
                if child.custom_id == "mp:pause_button":
                    mp = musicService.findMusicPlayerByGuildId(guildId)
                    if mp.isStopped:
                        child.emoji = config.playEmoji
                    else:
                        child.emoji = config.pauseEmoji
                    break
        self.bot = bot

    @discord.ui.button(label="", style=discord.ButtonStyle.primary, emoji=config.previousEmoji, row=0)
    async def previousCallback(self, interaction, button):
        if await is_in_vcInteraction(interaction):
            guild = interaction.guild
            if guild.voice_client:
                musicService.getMusicPlayer(guild.id, interaction.channel.id).toPrevious()
                guild.voice_client.stop()
                await interaction.response.send_message(f"{interaction.user.display_name} switched to previous song", delete_after=15)

    @discord.ui.button(label="", style=discord.ButtonStyle.primary, emoji=config.pauseEmoji, row=0,
                       custom_id="mp:pause_button")
    async def pauseCallback(self, interaction, button):
        if await is_in_vcInteraction(interaction):
            if interaction.guild.voice_client.is_paused():
                interaction.guild.voice_client.resume()
                mp = musicService.findMusicPlayerByGuildId(interaction.guild.id)
                if mp is not None:
                    mp.isStopped = False
                await interaction.response.send_message(f"{interaction.user.display_name} resumed the player", delete_after=15)
            else:
                interaction.guild.voice_client.pause()
                mp = musicService.findMusicPlayerByGuildId(interaction.guild.id)
                if mp is not None:
                    mp.isStopped = True
                await interaction.response.send_message(f"{interaction.user.display_name} put player on pause", delete_after=15)
            await musicViewService.updatePlayer(musicService.findMusicPlayerByGuildId(interaction.guild_id), self.bot)

    @discord.ui.button(label="", style=discord.ButtonStyle.primary, emoji=config.skipEmoji, row=0)
    async def skipCallback(self, interaction, button):
        if await is_in_vcInteraction(interaction):
            guild = interaction.guild
            if guild.voice_client:
                musicService.getMusicPlayer(guild.id, interaction.channel_id).skip()
                guild.voice_client.stop()
                await interaction.response.send_message(f"{interaction.user.display_name} skipped song", delete_after=15)

    @discord.ui.button(label="", style=discord.ButtonStyle.primary, emoji=config.shuffleEmoji, row=1)
    async def shuffleCallback(self, interaction, button):
        if await is_in_vcInteraction(interaction):
            musicService.getMusicPlayer(interaction.guild_id, interaction.channel_id).shuffle()
            await interaction.response.send_message(f"{interaction.user.display_name} shuffled the list!", delete_after=15)

    @discord.ui.button(label="", style=discord.ButtonStyle.primary, emoji=config.repeatEmoji, row=1)
    async def repeatCallback(self, interaction, button):
        if await is_in_vcInteraction(interaction):
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

    @discord.ui.button(label="", style=discord.ButtonStyle.primary, emoji=config.likeEmoji, row=1)
    async def likeCallback(self, interaction, button):
        await interaction.response.defer(ephemeral=True, thinking=True)
        mp = musicService.findMusicPlayerByGuildId(guild_id=interaction.guild.id)
        flag = await likedSongsService.likeSong(interaction.user.id, mp.playing.original_url)
        if mp.playing is not None and flag:
            await interaction.followup.send(await getLocale('ready', interaction.user.id), ephemeral=True)
        else:
            await interaction.followup.send(await getLocale('something-wrong', interaction.user.id), ephemeral=True)

    @discord.ui.button(label="", style=discord.ButtonStyle.primary, emoji=config.volumeDownEmoji, row=2)
    async def volumeDownCallback(self, interaction, button):
        await interaction.response.defer(ephemeral=True, thinking=True)
        vc = interaction.guild.voice_client
        if await is_in_vcInteraction(interaction) and vc is not None:
            mp = musicService.getMusicPlayer(interaction.guild_id, interaction.channel_id)
            if mp is None:
                await interaction.followup.send(await getLocale('something-wrong', interaction.user.id), ephemeral=True)
            else:
                new_volume = max(0, mp.volume - VOLUME_CHANGE_ON_CLICK)
                mp.volume = new_volume
                if vc.source is not None:
                    vc.source.volume = new_volume / 100
                if mp.musicPlayerChannelId is not None:
                    await musicViewService.updatePlayer(mediaPlayer=mp, bot=self.bot)
                await interaction.followup.send(await getLocale('ready', interaction.user.id), ephemeral=True)

    @discord.ui.button(label="", style=discord.ButtonStyle.danger, emoji=config.stopEmoji, row=2)
    async def stopCallback(self, interaction, button):
        if await is_in_vcInteraction(interaction):
            mp = musicService.getMusicPlayer(interaction.guild_id, interaction.channel_id)
            mp.songs = []
            mp.repeating = RepeatType.NOT_REPEATING
            if interaction.guild.voice_client:
                musicService.getMusicPlayer(interaction.guild_id, interaction.channel_id).skip()
                interaction.guild.voice_client.stop()
                await interaction.response.send_message(f"{interaction.user.display_name} stopped the player!", delete_after=15)

    @discord.ui.button(label="", style=discord.ButtonStyle.primary, emoji=config.volumeUpEmoji, row=2)
    async def volumeUpCallback(self, interaction, button):
        await interaction.response.defer(ephemeral=True, thinking=True)
        vc = interaction.guild.voice_client
        if await is_in_vcInteraction(interaction) and vc is not None:
            mp = musicService.getMusicPlayer(interaction.guild_id, interaction.channel_id)
            if mp is None:
                await interaction.followup.send(await getLocale('something-wrong', interaction.user.id), ephemeral=True)
            else:
                new_volume = min(200, mp.volume + VOLUME_CHANGE_ON_CLICK)
                mp.volume = new_volume
                if vc.source is not None:
                    vc.source.volume = new_volume / 100
                if mp.musicPlayerChannelId is not None:
                    await musicViewService.updatePlayer(mediaPlayer=mp, bot=self.bot)
                await interaction.followup.send(await getLocale('ready', interaction.user.id), ephemeral=True)
