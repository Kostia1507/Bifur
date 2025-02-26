import discord

from models.BlackjackGame import BlackjackGame


class BlackjackView(discord.ui.View):

    def __init__(self, bot, game: BlackjackGame):
        super().__init__(timeout=None)
        self.bot = bot
        self.game = game

    @discord.ui.button(label="Hit", style=discord.ButtonStyle.blurple, row=0)
    async def hitCallback(self, interaction, button):
        if interaction.user.id in self.game.players:
            if interaction.user.id == self.game.players[self.game.turn%len(self.game.players)]:
                self.game.board[interaction.user.id].append(self.game.pickRandomCard())
                await interaction.response.send_message("Your cards: " + ", ".join(map(str, self.game.board[interaction.user.id]))
                                                        + " = " + str(sum(self.game.board[interaction.user.id])), ephemeral=True)
                self.game.increase_turn()
                if sum(self.game.board[interaction.user.id]) >= 21:
                    self.game.passed.append(interaction.user.id)
                await self.updateMessage(interaction)
            else:
                await interaction.response.send_message("It's not your turn!", ephemeral=True)
        else:
            await interaction.response.send_message("You are not in this game!", ephemeral=True)

    @discord.ui.button(label="Cards", style=discord.ButtonStyle.blurple, row=0)
    async def cardsCallback(self, interaction, button):
        if interaction.user.id in self.game.players:
            cards = self.game.board[interaction.user.id]
            await interaction.response.send_message("Your cards: "+", ".join(map(str, cards)) + " = "+str(sum(cards)), ephemeral=True)
        else:
            await interaction.response.send_message("You are not in this game!", ephemeral=True)

    @discord.ui.button(label="Pass", style=discord.ButtonStyle.gray, row=0)
    async def passCallback(self, interaction, button):
        if interaction.user.id in self.game.players:
            if interaction.user.id == self.game.players[self.game.turn % len(self.game.players)]:
                await interaction.response.send_message("Passed!", ephemeral=True)
                self.game.passed.append(interaction.user.id)
                self.game.increase_turn()
                await self.updateMessage(interaction)
            else:
                await interaction.response.send_message("It's not your turn!", ephemeral=True)
        else:
            await interaction.response.send_message("You are not in this game!", ephemeral=True)

    async def updateMessage(self, interaction):
        embed = discord.Embed(title="Blackjack", description=self.game.get_description())
        await interaction.message.edit(content=None, embed=embed, view=BlackjackView(self.bot, self.game))
