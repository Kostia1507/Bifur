import discord

from discordModels.modals.ReportModal import ReportModal


class ReportView(discord.ui.View):

    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label="Send report", style=discord.ButtonStyle.primary, custom_id='persistent_view:report_view')
    async def previousCallback(self, interaction, button):
        await interaction.response.send_modal(ReportModal(self.bot))
