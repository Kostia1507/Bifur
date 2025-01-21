import os

import discord

import config


class PagedMessageView(discord.ui.View):

    def __init__(self, pagedMessage):
        super().__init__()
        self.pagedMessage = pagedMessage

    @discord.ui.button(label="", style=discord.ButtonStyle.gray, emoji=config.previousPageEmoji)
    async def leftCallback(self, interaction: discord.Interaction, button):
        await interaction.response.defer(ephemeral=True)
        page = self.pagedMessage.getPage(self.pagedMessage.currentPage - 1)
        embed = discord.Embed(title=self.pagedMessage.title, description=page)
        embed.set_footer(text=f'Page {self.pagedMessage.currentPage + 1} of {len(self.pagedMessage.pages)}')
        if self.pagedMessage.imageUrl is not None:
            embed.set_image(url=self.pagedMessage.imageUrl)
        await interaction.message.edit(embed=embed)

    @discord.ui.button(label="", style=discord.ButtonStyle.gray, emoji=config.nextPageEmoji)
    async def rightCallback(self, interaction: discord.Interaction, button):
        await interaction.response.defer(ephemeral=True)
        page = self.pagedMessage.getPage(self.pagedMessage.currentPage + 1)
        embed = discord.Embed(title=self.pagedMessage.title, description=page)
        embed.set_footer(text=f'Page {self.pagedMessage.currentPage + 1} of {len(self.pagedMessage.pages)}')
        if self.pagedMessage.imageUrl is not None:
            embed.set_image(url=self.pagedMessage.imageUrl)
        await interaction.message.edit(embed=embed)

    @discord.ui.button(label="", style=discord.ButtonStyle.green, emoji=config.saveEmoji)
    async def saveCallback(self, interaction: discord.Interaction, button):
        res = "\n".join(self.pagedMessage.pages)
        with open(f'{interaction.message.id}.txt', "w") as file:
            file.write(res)
        with open(f'{interaction.message.id}.txt', "rb") as file:
            await interaction.response.send_message(file=discord.File(file, f'{interaction.message.id}.txt'))
            os.remove(f'{interaction.message.id}.txt')



