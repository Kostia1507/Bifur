import traceback

import discord

from models.ReversiGame import ReversiGame, convert_str_to_cords, count_marks
from service import localeService


class ReversiView(discord.ui.View):

    def __init__(self, bot, game: ReversiGame):
        super().__init__(timeout=None)
        self.bot = bot
        self.game = game

    @discord.ui.button(label="Move", style=discord.ButtonStyle.primary)
    async def moveCallback(self, interaction, button):
        user_id = self.game.players[self.game.turn % 2]
        if interaction.user.id == user_id:
            await interaction.response.send_modal(ReversiModal(self.bot, self.game))
        else:
            await interaction.response.send_message(content="It's not your turn!", ephemeral=True)

    @discord.ui.button(label="Surrender", style=discord.ButtonStyle.gray)
    async def surrenderCallback(self, interaction, button):
        user_id = self.game.players[self.game.turn % 2]
        if interaction.user.id == user_id:
            await interaction.response.send_modal(SurrenderConfirmModal(self.bot, self.game))
        else:
            await interaction.response.send_message(content="It's not your turn!", ephemeral=True)


class ReversiModal(discord.ui.Modal, title='Reversi'):

    def __init__(self, bot, game: ReversiGame):
        super().__init__()
        self.bot = bot
        self.game = game

    moveInput = discord.ui.TextInput(
        label='Write your move in coordinates like "c5"'
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True, ephemeral=True)
        move = self.moveInput.value
        x, y = convert_str_to_cords(move)
        ret = self.game.handle_move(x, y, interaction.user.id)
        if ret:
            img = discord.File(self.game.generate_picture(), "reversi.jpg")
            embed = discord.Embed(title="Reversi", description=self.game.get_text())
            embed.set_image(url=f'attachment://reversi.jpg')
            await interaction.message.edit(content="", embed=embed, view=ReversiView(self.bot, self.game),
                                           attachments=[img])
            await interaction.followup.send(await localeService.getLocale('ready', interaction.user.id))
        else:
            await interaction.followup.send(await localeService.getLocale('ready', interaction.user.id))
            img = discord.File(self.game.generate_picture(), "reversi.jpg")
            embed = discord.Embed(title="Reversi", description=self.game.get_text())
            embed.set_image(url=f'attachment://reversi.jpg')
            white, black = count_marks(self.game.board)
            if white > black:
                await interaction.message.edit(content="Game finished! White won the game!", embed=embed,
                                               attachments=[img])
            elif black > white:
                await interaction.message.edit(content="Game finished! Black won the game!", embed=embed,
                                               attachments=[img])
            else:
                await interaction.message.edit(content="Game finished! Draw.", embed=embed, attachments=[img])

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        await interaction.response.send_message('Something wrong!', ephemeral=True)
        traceback.print_exception(type(error), error, error.__traceback__)


class SurrenderConfirmModal(discord.ui.Modal, title='Surrender'):

    def __init__(self, bot, game: ReversiGame):
        super().__init__()
        self.bot = bot
        self.game = game

    messageInput = discord.ui.TextInput(
        label='Leave your message if you want',
        required = False,
        placeholder="Your comment"
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True, thinking=True)
        embed = discord.Embed(title="Reversi", description=self.game.get_text())
        embed.set_image(url=f'attachment://reversi.jpg')
        img = discord.File(self.game.generate_picture(), "reversi.jpg")
        if self.game.turn % 2 == 0:
            if self.messageInput.value is not None and len(self.messageInput.value) > 0:
                await interaction.message.edit(content=f"{interaction.user.name} gave up! White won the game!\n"
                                                       f"{interaction.user.name}'s comment: {self.messageInput.value}",
                                               embed=embed, attachments=[img], view=None)
            else:
                await interaction.message.edit(content=f"{interaction.user.name} gave up! White won the game!",
                                               embed=embed, attachments=[img], view=None)
        else:
            if self.messageInput.value is not None and len(self.messageInput.value) > 0:
                await interaction.message.edit(content=f"{interaction.user.name} gave up! Black won the game!\n"
                                                       f"{interaction.user.name}'s comment: {self.messageInput.value}",
                                               embed=embed, attachments=[img], view=None)
            else:
                await interaction.message.edit(content=f"{interaction.user.name} gave up! Black won the game!",
                                               embed=embed, attachments=[img], view=None)
        await interaction.followup.send(await localeService.getLocale('ready', interaction.user.id))