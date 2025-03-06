import discord
from discord.ui import ChannelSelect
from numpy.lib.function_base import place

from models import PendingCommand

intervalOptions = [discord.SelectOption(label="1 hour", value="1"),
                   discord.SelectOption(label="2 hours", value="2"),
                   discord.SelectOption(label="3 hours", value="3"),
                   discord.SelectOption(label="4 hours", value="4"),
                   discord.SelectOption(label="6 hours", value="6"),
                   discord.SelectOption(label="8 hours", value="8"),
                   discord.SelectOption(label="12 hours", value="12"),
                   discord.SelectOption(label="24 hours", value="24")]

commandsOptions = [discord.SelectOption(label="Weather", value="weather"),
                   discord.SelectOption(label="Weather detailed", value="weatherd"),
                   discord.SelectOption(label="Say something", value="say"),
                   discord.SelectOption(label="Time UTC", value="time"),
                   discord.SelectOption(label="Currency", value="currency")]


class AutoCmdView(discord.ui.View):

    def __init__(self, bot, cmd):
        self.bot = bot
        self.cmd = cmd
        super().__init__(timeout=None)

    @discord.ui.button(label="Edit", style=discord.ButtonStyle.gray, custom_id='persistent_view:edit_cmd')
    async def previousCallback(self, interaction, button):
        await interaction.response.send_modal(EditCmdModal(self.bot, self.cmd, interaction.message))

    @discord.ui.button(label="Save", style=discord.ButtonStyle.green, custom_id='persistent_view:save_cmd')
    async def saveCallback(self, interaction, button):
        await interaction.response.send_message("Ok")

    @discord.ui.select(cls=ChannelSelect, channel_types=[discord.ChannelType.text], custom_id="persistent_view:autocmd_channel")
    async def select_channels(self, interaction: discord.Interaction, select: ChannelSelect):
        return await interaction.response.send_message(f'You selected {select.values[0].mention}')

    @discord.ui.select(options=commandsOptions, placeholder="Select command", custom_id="persistent_view:autocmd_command")
    async def select_command(self, interaction: discord.Interaction, select: ChannelSelect):
        return await interaction.response.send_message(f'You selected {select.values[0]}')

    @discord.ui.select(options=intervalOptions, placeholder="Select interval", custom_id="persistent_view:autocmd_interval")
    async def select_interval(self, interaction: discord.Interaction, select: ChannelSelect):
        return await interaction.response.send_message(f'You selected {select.values[0]}')


class EditCmdModal(discord.ui.Modal, title='AutoCommand'):

    def __init__(self, bot, cmd, message):
        super().__init__()
        self.bot = bot
        self.cmd = cmd
        self.message = message

    arguments = discord.ui.TextInput(
        label='Arguments'
    )

    startHour = discord.ui.TextInput(
        label='Start hour'
    )

    async def on_submit(self, interaction: discord.Interaction):
        arguments = self.arguments.value
        description = self.startHour.value
        pass
