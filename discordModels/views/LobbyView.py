import discord

class LobbyView(discord.ui.View):

    def __init__(self, bot, gameType, count, user_id):
        super().__init__(timeout=None)
        self.bot = bot
        self.gameType = gameType
        self.count = count
        self.players = [user_id]
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
                await interaction.response.send_message("Ok, you left from the lobby!", ephemeral=True)
                await self.updateMessage(interaction)
            else:
                await interaction.response.send_message("You aren't in lobby", ephemeral=True)

    @discord.ui.button(label="Start", style=discord.ButtonStyle.green, row=1)
    async def startCallback(self, interaction, button):
        await interaction.response.send_message("IN PROGRESS", ephemeral=True)

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
        text = f"Players: {len(users)}/{self.count}\n"
        for user in users:
            text += f"{user.display_name}\n"
        embed = discord.Embed(title=self.gameType, description=text)
        await interaction.message.edit(content=None, embed=embed, view=LobbyView(self.bot, self.gameType, self.count, self.admin))
