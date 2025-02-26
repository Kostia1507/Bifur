import discord

from cogs import LogCog
from discordModels.views.BlackjackView import BlackjackView

from models.BlackjackGame import BlackjackGame


class LobbyView(discord.ui.View):

    def __init__(self, bot, gameType, count, user_id, players=None):
        super().__init__(timeout=None)
        self.bot = bot
        self.gameType = gameType
        self.count = count
        if players is None:
            self.players = [user_id]
        else:
            self.players = players
        self.admin = user_id

    @discord.ui.button(label="Join", style=discord.ButtonStyle.green, row=0)
    async def joinCallback(self, interaction, button):
        if interaction.user.id not in self.players:
            self.players.append(interaction.user.id)
            await self.updateMessage(interaction)
            await interaction.response.send_message("Joined to lobby", ephemeral=True)
        else:
            await interaction.response.send_message("You are already in this lobby", ephemeral=True)

    @discord.ui.button(label="Leave", style=discord.ButtonStyle.red, row=0)
    async def leaveCallback(self, interaction, button):
        if interaction.user.id == self.admin:
            await interaction.response.send_message("Admin can't leave the lobby", ephemeral=True)
        else:
            if interaction.user.id in self.players:
                self.players.remove(interaction.user.id)
                await interaction.response.send_message("Ok, you left from the lobby!", ephemeral=True)
                await self.updateMessage(interaction)
            else:
                await interaction.response.send_message("You aren't in lobby", ephemeral=True)

    @discord.ui.button(label="Start", style=discord.ButtonStyle.green, row=1)
    async def startCallback(self, interaction, button):
        if self.admin != interaction.user.id:
            await interaction.response.send_message("Only creator can start the game!", ephemeral=True)
            return
        if self.gameType == "Blackjack":
            playersNicknames = []
            players = []
            for user_id in self.players:
                try:
                    user = await interaction.guild.fetch_member(user_id)
                    playersNicknames.append(user.display_name)
                    players.append(user_id)
                except discord.errors.NotFound:
                    LogCog.logError(f"User not found while creating Blackjack {user_id}")
            game = BlackjackGame(players, playersNicknames)
            embed = discord.Embed(title="Blackjack", description=game.get_description())
            await interaction.message.edit(content=None, embed=embed, view=BlackjackView(self.bot, game))

    @discord.ui.button(label="Delete", style=discord.ButtonStyle.red, row=1)
    async def deleteCallback(self, interaction, button):
        if interaction.user.id == self.admin:
            await interaction.message.delete()
        else:
            await interaction.response.send_message("You are not admin", ephemeral=True)

    async def updateMessage(self, interaction):
        users = []
        remove = []
        for user_id in self.players:
            try:
                user = await interaction.guild.fetch_member(user_id)
                users.append(user)
            except discord.errors.NotFound:
                remove.append(user_id)
        # User left from the guild or the error happened. Anyway I hate @everyone
        for i in remove:
            self.players.remove(i)
        text = f"Players: {len(users)}/{self.count}\n"
        for user in users:
            text += f"{user.display_name}\n"
        embed = discord.Embed(title=self.gameType, description=text)
        await interaction.message.edit(content=None, embed=embed, view=LobbyView(self.bot, self.gameType, self.count, self.admin, self.players))
