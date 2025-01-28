import traceback

import discord

from models.WordleGame import WordleGame
from service import localeService


class WordleView(discord.ui.View):

    def __init__(self, bot, game: WordleGame):
        super().__init__(timeout=None)
        self.bot = bot
        self.game = game

    @discord.ui.button(label="Guess", style=discord.ButtonStyle.primary)
    async def moveCallback(self, interaction, button):
        if interaction.user.id == self.game.user_id:
            await interaction.response.send_modal(WordleModal(self.bot, self.game))
        else:
            await interaction.response.send_message(content="It's not your game!", ephemeral=True)

    @discord.ui.button(label="Surrender", style=discord.ButtonStyle.gray)
    async def surrenderCallback(self, interaction, button):
        if interaction.user.id == self.game.user_id:
            await interaction.response.send_modal(SurrenderConfirmModal(self.bot, self.game))
        else:
            await interaction.response.send_message(content="It's not your game!", ephemeral=True)


class WordleModal(discord.ui.Modal, title='Reversi'):

    def __init__(self, bot, game: WordleGame):
        super().__init__()
        self.bot = bot
        self.game = game

    moveInput = discord.ui.TextInput(
        label='Write your guess'
    )

    async def on_submit(self, interaction: discord.Interaction):
        move = self.moveInput.value.lower().strip()
        if len(move) != 5:
            await interaction.response.send_message("Write word with 5 letters")
            return
        await interaction.response.defer(thinking=True, ephemeral=True)
        ret = self.game.makeMove(move)
        if ret is not None:
            img = discord.File(self.game.generetaPicture(), "wordle.png")
            embed = discord.Embed(title="Wordle", description=self.game.get_description())
            embed.set_image(url=f'attachment://wordle.png')
            if self.game.finished:
                await interaction.message.edit(content=None, embed=embed, view=None, attachments=[img])
            else:
                await interaction.message.edit(content=None, embed=embed, view=WordleView(self.bot, self.game), attachments=[img])
        await interaction.followup.send(localeService.getLocale('ready', interaction.user.id))

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Something wrong!', ephemeral=True)
        traceback.print_exception(type(error), error, error.__traceback__)


class SurrenderConfirmModal(discord.ui.Modal, title='Surrender'):

    def __init__(self, bot, game: WordleGame):
        super().__init__()
        self.bot = bot
        self.game = game

    messageInput = discord.ui.TextInput(
        label='Leave your message if you want',
        required = False,
        placeholder="Your comment"
    )

    async def on_submit(self, interaction: discord.Interaction):
        if len(self.messageInput.value) > 0:
            await interaction.response.send_message(f"Word was: {self.game.answer}\nComment: {self.messageInput.value}")
        else:
            await interaction.response.send_message(f"The word was: {self.game.answer}")