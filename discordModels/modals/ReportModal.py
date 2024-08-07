import traceback
from datetime import datetime, timedelta

import discord

import config
from cogs import LogCog


class ReportModal(discord.ui.Modal, title='Report'):

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    titleInput = discord.ui.TextInput(
        label='Title'
    )

    descriptionInput = discord.ui.TextInput(
        label='Description'
    )

    async def on_submit(self, interaction: discord.Interaction):
        title = self.titleInput.value
        description = self.descriptionInput.value
        print(title)
        print(description)
        # please add paged msg here

        # user = await self.bot.fetch_user(418040057019236353)
        # await user.send(f'{ctx.author} reported: {" ".join(args)}')

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Error happened. Report it, lol!', ephemeral=True)
        traceback.print_exception(type(error), error, error.__traceback__)
