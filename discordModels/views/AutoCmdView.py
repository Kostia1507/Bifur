import discord

from models import PendingCommand

class AutoCmdView(discord.ui.View):

    def __init__(self, bot, cmd):
        self.bot = bot
        self.cmd = cmd
        super().__init__(timeout=None)

    @discord.ui.button(label="Edit", style=discord.ButtonStyle.gray, custom_id='persistent_view:edit_cmd')
    async def previousCallback(self, interaction, button):
        await interaction.response.send_modal(EditCmdModal(self.bot, self.cmd, interaction.message))

    @discord.ui.button(label="Save", style=discord.ButtonStyle.gray, custom_id='persistent_view:save_cmd')
    async def saveCallback(self, interaction, button):
        await interaction.response.send_message("Ok")


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
