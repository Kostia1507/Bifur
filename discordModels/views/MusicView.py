import discord

from models.MusicPlayer import RepeatType
from service import musicService
from service.localeService import getLocale


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


class MusicView(discord.ui.View):

    @discord.ui.button(label="", style=discord.ButtonStyle.primary, emoji="⏪")
    async def previousCallback(self, interaction, button):
        if await is_in_vcInteraction(interaction):
            guild = interaction.guild
            if guild.voice_client:
                musicService.getMusicPlayer(guild.id, interaction.channel.id).toPrevious()
                guild.voice_client.stop()
                await interaction.response.send_message("Return to previous song", ephemeral=True, delete_after=15)

    @discord.ui.button(label="", style=discord.ButtonStyle.primary, emoji="⏩")
    async def skipCallback(self, interaction, button):
        if await is_in_vcInteraction(interaction):
            guild = interaction.guild
            if guild.voice_client:
                musicService.getMusicPlayer(guild.id, interaction.channel_id).skip()
                guild.voice_client.stop()
                await interaction.response.send_message("The song is skipped", ephemeral=True, delete_after=15)

    @discord.ui.button(label="", style=discord.ButtonStyle.primary, emoji="⏯")
    async def pauseCallback(self, interaction, button):
        if await is_in_vcInteraction(interaction):
            if interaction.guild.voice_client.is_paused():
                interaction.guild.voice_client.resume()
                await interaction.response.send_message("Resumed playing", ephemeral=True, delete_after=15)
            else:
                interaction.guild.voice_client.pause()
                await interaction.response.send_message("Now on pause", ephemeral=True, delete_after=15)

    @discord.ui.button(label="", style=discord.ButtonStyle.primary, emoji="🔀")
    async def shuffleCallback(self, interaction, button):
        if await is_in_vcInteraction(interaction):
            musicService.getMusicPlayer(interaction.guild_id, interaction.channel_id).shuffle()
            await interaction.response.send_message("Shuffled!", ephemeral=True, delete_after=15)

    @discord.ui.button(label="", style=discord.ButtonStyle.primary, emoji="🔁")
    async def repeatCallback(self, interaction, button):
        if await is_in_vcInteraction(interaction):
            mp = musicService.getMusicPlayer(interaction.guild_id, interaction.channel_id)
            repeatN = mp.repeating.value - 1
            if repeatN == -1:
                repeatN = 2
            mp.repeating = RepeatType(repeatN)
            if mp.repeating == RepeatType.NOT_REPEATING:
                await interaction.response.send_message(
                    getLocale('repeat-off', interaction.user.id), ephemeral=True, delete_after=15)
            elif mp.repeating ==  RepeatType.REPEAT_ONE:
                await interaction.response.send_message(
                    getLocale('repeat-one', interaction.user.id), ephemeral=True, delete_after=15)
            else:
                await interaction.response.send_message(
                    getLocale('repeat-on', interaction.user.id), ephemeral=True, delete_after=15)

    @discord.ui.button(label="", style=discord.ButtonStyle.danger, emoji="⬜")
    async def stopCallback(self, interaction, button):
        if await is_in_vcInteraction(interaction):
            mp = musicService.getMusicPlayer(interaction.guild_id, interaction.channel_id)
            mp.songs = []
            mp.repeating = RepeatType.NOT_REPEATING
            if interaction.guild.voice_client:
                print("hui")
                musicService.getMusicPlayer(interaction.guild_id, interaction.channel_id).skip()
                interaction.guild.voice_client.stop()
                await interaction.response.send_message("Stopped playing", ephemeral=True, delete_after=15)
