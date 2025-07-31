import discord

from models.RPSGame import RPSGame, SignValue


class RPSView(discord.ui.View):

    def __init__(self, bot, game: RPSGame):
        super().__init__(timeout=None)
        self.bot = bot
        self.game = game

    @discord.ui.button(label="Rock", style=discord.ButtonStyle.primary, emoji="🪨")
    async def rockCallback(self, interaction, button):
        if self.game.make_move(SignValue.ROCK, interaction.user.id):
            await interaction.response.send_message(content="Rock!", ephemeral=True)
            if self.game.is_game_ready_for_result():
                await interaction.message.edit(view=None, content = self.game.get_text())
        else:
            await interaction.response.send_message(content="This is not your game or you have already made your choice!", ephemeral=True)

    @discord.ui.button(label="Paper", style=discord.ButtonStyle.primary, emoji="📰")
    async def paperCallback(self, interaction, button):
        if self.game.make_move(SignValue.PAPER, interaction.user.id):
            await interaction.response.send_message(content="Paper!", ephemeral=True)
            if self.game.is_game_ready_for_result():
                await interaction.message.edit(view=None, content=self.game.get_text())
        else:
            await interaction.response.send_message(
                content="This is not your game or you have already made your choice!", ephemeral=True)

    @discord.ui.button(label="Scissors", style=discord.ButtonStyle.primary, emoji="✂️")
    async def scissorsCallback(self, interaction, button):
        if self.game.make_move(SignValue.SCISSORS, interaction.user.id):
            await interaction.response.send_message(content="Scissors!", ephemeral=True)
            if self.game.is_game_ready_for_result():
                await interaction.message.edit(view=None, content=self.game.get_text())
        else:
            await interaction.response.send_message(
                content="This is not your game or you have already made your choice!", ephemeral=True)
