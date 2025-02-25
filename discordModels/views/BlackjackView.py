import discord

from models.BlackjackGame import BlackjackGame


class BlackjackView(discord.ui.View):

    def __init__(self, bot, game: BlackjackGame):
        super().__init__(timeout=None)
        self.bot = bot
        self.game = game

    @discord.ui.button(label="Hit", style=discord.ButtonStyle.blurple, row=0)
    async def hitCallback(self, interaction, button):
        pass

    @discord.ui.button(label="Pass", style=discord.ButtonStyle.gray, row=0)
    async def passCallback(self, interaction, button):
        pass

