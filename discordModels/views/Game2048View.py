import traceback

import discord
from discord import ButtonStyle

import config
from models.Game2048 import Game2048, MoveDirection
from service import localeService


class Game2048View(discord.ui.View):

    def __init__(self, bot, game: Game2048):
        super().__init__(timeout=None)
        self.bot = bot
        self.game = game

    # ROW 1

    @discord.ui.button(emoji="▪️", style=ButtonStyle.secondary, label="", row=0)
    async def leftTopButtonCallback(self, interaction, button):
        await interaction.response.send_message(content="just decorative button!", ephemeral=True)

    @discord.ui.button(emoji="⬆", style=ButtonStyle.primary, label="", row=0)
    async def moveTopCallback(self, interaction, button):
        if interaction.user.id == self.game.user_id:
            retStatus = self.game.move(MoveDirection.TOP)
            img = discord.File(self.game.generate_picture(), "board2048.png")
            embed = discord.Embed(title="2048", description=f"Moves: {self.game.moves}")
            embed.set_image(url=f'attachment://board2048.png')
            if retStatus and self.game.is_game_over():
                await interaction.response.edit_message(content=f"Game over\nPoints: {self.game.count_all()}",
                                                        embed=embed, view=None, attachments=[img])
            else:
                await interaction.response.edit_message(content=None, embed=embed, view=Game2048View(self.bot, self.game),
                                               attachments=[img])
        else:
            await interaction.response.send_message(content="It's not your game!", ephemeral=True)

    @discord.ui.button(emoji="▪️", style=ButtonStyle.secondary, label="", row=0)
    async def rightTopButtonCallback(self, interaction, button):
        await interaction.response.send_message(content="just decorative button!", ephemeral=True)

    # ROW 2

    @discord.ui.button(emoji="⬅", style=ButtonStyle.primary, label="", row=1)
    async def moveLeftCallback(self, interaction, button):
        if interaction.user.id == self.game.user_id:
            retStatus = self.game.move(MoveDirection.LEFT)
            img = discord.File(self.game.generate_picture(), "board2048.png")
            embed = discord.Embed(title="2048", description=f"Moves: {self.game.moves}")
            embed.set_image(url=f'attachment://board2048.png')
            if retStatus and self.game.is_game_over():
                await interaction.response.edit_message(content=f"Game over\nPoints: {self.game.count_all()}",
                                                        embed=embed, view=None, attachments=[img])
            else:
                await interaction.response.edit_message(content=None, embed=embed,
                                                        view=Game2048View(self.bot, self.game),
                                                        attachments=[img])
        else:
            await interaction.response.send_message(content="It's not your game!", ephemeral=True)

    @discord.ui.button(emoji="▪️", style=ButtonStyle.secondary, label="", row=1)
    async def centerButtonCallback(self, interaction, button):
        await interaction.response.send_message(content="just decorative button!", ephemeral=True)

    @discord.ui.button(emoji="➡", style=ButtonStyle.primary, label="", row=1)
    async def rightMoveCallback(self, interaction, button):
        if interaction.user.id == self.game.user_id:
            retStatus = self.game.move(MoveDirection.RIGHT)
            img = discord.File(self.game.generate_picture(), "board2048.png")
            embed = discord.Embed(title="2048", description=f"Moves: {self.game.moves}")
            embed.set_image(url=f'attachment://board2048.png')
            if retStatus and self.game.is_game_over():
                await interaction.response.edit_message(content=f"Game over\nPoints: {self.game.count_all()}",
                                                        embed=embed, view=None, attachments=[img])
            else:
                await interaction.response.edit_message(content=None, embed=embed,
                                                        view=Game2048View(self.bot, self.game),
                                                        attachments=[img])
        else:
            await interaction.response.send_message(content="It's not your game!", ephemeral=True)

    # ROW 3

    @discord.ui.button(emoji="▪️", style=ButtonStyle.secondary, label="", row=2)
    async def leftBottomButtonCallback(self, interaction, button):
        await interaction.response.send_message(content="just decorative button!", ephemeral=True)

    @discord.ui.button(emoji="⬇", style=ButtonStyle.primary, label="", row=2)
    async def moveBottomCallback(self, interaction, button):
        if interaction.user.id == self.game.user_id:
            retStatus = self.game.move(MoveDirection.BOTTOM)
            img = discord.File(self.game.generate_picture(), "board2048.png")
            embed = discord.Embed(title="2048", description=f"Moves: {self.game.moves}")
            embed.set_image(url=f'attachment://board2048.png')
            if retStatus and self.game.is_game_over():
                await interaction.response.edit_message(content=f"Game over\nPoints: {self.game.count_all()}",
                                                        embed=embed, view=None, attachments=[img])
            else:
                await interaction.response.edit_message(content=None, embed=embed,
                                                        view=Game2048View(self.bot, self.game),
                                                        attachments=[img])
        else:
            await interaction.response.send_message(content="It's not your game!", ephemeral=True)

    @discord.ui.button(emoji="▪️", style=ButtonStyle.secondary, label="", row=2)
    async def rightBottomButtonCallback(self, interaction, button):
        await interaction.response.send_message(content="just decorative button!", ephemeral=True)