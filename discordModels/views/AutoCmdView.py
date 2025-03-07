import discord
from discord.ui import ChannelSelect

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

    def __init__(self, bot, cmd: PendingCommand):
        self.bot = bot
        self.cmd = cmd
        super().__init__(timeout=None)

    @discord.ui.button(label="Edit", style=discord.ButtonStyle.gray, custom_id='persistent_view:edit_cmd')
    async def previousCallback(self, interaction, button):
        await interaction.response.send_modal(EditCmdModal(self.bot, self.cmd, interaction.message))

    @discord.ui.button(label="Save", style=discord.ButtonStyle.green, custom_id='persistent_view:save_cmd')
    async def saveCallback(self, interaction, button):
        await interaction.response.defer(ephemeral=True, thinking=True)
        self.cmd.update()
        await interaction.followup.send("Saved", ephemeral=True)

    @discord.ui.select(cls=ChannelSelect, channel_types=[discord.ChannelType.text], custom_id="persistent_view:autocmd_channel")
    async def select_channels(self, interaction: discord.Interaction, select: ChannelSelect):
        self.cmd.channelId = select.values[0].id
        await interaction.response.defer()

    @discord.ui.select(options=commandsOptions, placeholder="Select command", custom_id="persistent_view:autocmd_command")
    async def select_command(self, interaction: discord.Interaction, select: ChannelSelect):
        self.cmd.cmdType = select.values[0]
        await interaction.response.defer()

    @discord.ui.select(options=intervalOptions, placeholder="Select interval", custom_id="persistent_view:autocmd_interval")
    async def select_interval(self, interaction: discord.Interaction, select: ChannelSelect):
        self.cmd.interval = select.values[0]
        await interaction.response.defer()


class EditCmdModal(discord.ui.Modal, title='AutoCommand'):

    def __init__(self, bot, cmd, message):
        super().__init__()
        self.bot = bot
        self.cmd = cmd
        self.message = message

    arguments = discord.ui.TextInput(
        label='Arguments',
        required=False
    )

    startHour = discord.ui.TextInput(
        label='Start hour'
    )

    async def on_submit(self, interaction: discord.Interaction):
        arguments = self.arguments.value
        startHour = self.startHour.value
        if startHour.isnumeric() and 0 <= int(startHour) <= 24:
            self.cmd.startHour = int(startHour)%24
            self.cmd.args = arguments
            await interaction.response.send_message("Ok. Updated!\n"
                                                    "**Don't forget to save your command**", ephemeral=True)
            embed = discord.Embed(title="AutoCommand", description=f"Command: {self.cmd.cmdType}\n"
                                                                   f"Arguments: {self.cmd.args}\n"
                                                                   f"All autocommands is similar to usual cmds.\n"
                                                                   f"So if you need args, use it like any usual command in Bifur or read the docs\n"
                                                                   f"Start hour (UTC): {self.cmd.startHour}\n"
                                                                   f"Interval: {self.cmd.interval} hours\n")
            await self.message.edit(embed=embed, view=AutoCmdView(self.bot, self.cmd))
        else:
            await interaction.response.send_message("Start hour must be an Integer from 0 to 24", ephemeral=True)
