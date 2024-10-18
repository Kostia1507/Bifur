import os

import discord
from discord import ButtonStyle

from models.TicTacToeGame import TicTacToeGame, BLUE_CIRCLE, RED_CROSS
from service import localeService


class TicTacToeButton(discord.ui.Button):

    def __init__(self, x, y, emoji, game: TicTacToeGame):
        super().__init__(emoji=emoji, style=ButtonStyle.secondary, label="", row=x)
        self.x = x
        self.y = y
        self.game = game


    async def callback(self, interaction: discord.Interaction):
        if self.game.makeMove(interaction.user.id, self.x, self.y):
            await interaction.response.defer()
            ret = self.game.isEnd()
            if ret == 1:
                self.game.startText = self.game.startText + "\nRed won!"
                self.game.finished = True
            elif ret == 2:
                self.game.startText = self.game.startText + "\nBlue won!"
                self.game.finished = True
            elif ret == 3:
                self.game.startText = self.game.startText + "\nDraw!"
                self.game.finished = True
            await interaction.message.edit(content=self.game.startText, view=TicTacToeView(self.game))
            await interaction.followup.send(localeService.getLocale("ready", interaction.user.id), ephermal=True)
        else:
            await interaction.response.send_message("It's not your turn!", ephemeral=True)


class TicTacToeView(discord.ui.View):

    def __init__(self, game: TicTacToeGame):
        super().__init__(timeout=None)
        for x in range(0, game.size):
            for y in range(0, game.size):
                if game.board[x][y] == 0:
                    self.add_item(TicTacToeButton(x, y, "▪️", game))
                elif game.board[x][y] == 1:
                    self.add_item(TicTacToeButton(x, y, RED_CROSS, game))
                else:
                    self.add_item(TicTacToeButton(x, y, BLUE_CIRCLE, game))





