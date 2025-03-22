import asyncio
import traceback

import discord

from models.Song import Song
from service import radioService
from service.localeService import getLocale


class RadioInfoView(discord.ui.View):

    def __init__(self, bot, radio_id):
        super().__init__(timeout=None)
        self.radio_id = radio_id
        self.bot = bot

    @discord.ui.button(label="Rename", style=discord.ButtonStyle.primary, emoji="📝")
    async def renameCallback(self, interaction: discord.Interaction, button):
        await interaction.response.send_modal(RenameModal(self.bot, self.radio_id))

    @discord.ui.button(label="Add song", style=discord.ButtonStyle.green, emoji="➕")
    async def addTrackCallback(self, interaction: discord.Interaction, button):
        await interaction.response.send_modal(AddTrackModal(self.bot, self.radio_id))


class RenameModal(discord.ui.Modal, title='Rename'):

    def __init__(self, bot, radio_id):
        super().__init__()
        self.bot = bot
        self.radio_id = radio_id

    nameInput = discord.ui.TextInput(
        label='New name'
    )

    async def on_submit(self, interaction: discord.Interaction):
        newname = self.nameInput.value
        if not newname[0].isdigit():
            radio = await radioService.getRadioById(self.radio_id)
            await radio.rename(newname, interaction.user.id)
            await interaction.response.send_message(await getLocale("ready", interaction.user.id))
        else:
            await interaction.response.send_message(await getLocale("first-not-number", interaction.user.id))

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Error happened. Report it!', ephemeral=True)
        traceback.print_exception(type(error), error, error.__traceback__)

class AddTrackModal(discord.ui.Modal, title='Add song'):

    def __init__(self, bot, radio_id):
        super().__init__()
        self.bot = bot
        self.radio_id = radio_id

    linkInput = discord.ui.TextInput(
        label='YouTube link'
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True, thinking=True)
        link = self.linkInput.value
        song = Song(link, False)
        await song.updateFromWeb()
        name, duration = song.name, song.duration
        if name is None or duration is None:
            await interaction.followup.send(await getLocale('something-wrong', interaction.user.id))
            return
        retStatus = await radioService.createTrack(name, self.radio_id, link, interaction.user.id, duration)
        if retStatus is None:
            await interaction.followup.send(await getLocale("url-exist", interaction.user.id), ephemeral=True)
        elif retStatus:
            await interaction.followup.send(await getLocale("ready", interaction.user.id), ephemeral=True)
        else:
            await interaction.followup.send(await getLocale('no-playlist', interaction.user.id), ephemeral=True)


    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Error happened. Report it!', ephemeral=True)
        traceback.print_exception(type(error), error, error.__traceback__)


