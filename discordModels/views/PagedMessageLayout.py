import os

import discord

import config


class PagedMessageLayout(discord.ui.LayoutView):

    def __init__(self, pagedMessage):
        super().__init__()
        self.pagedMessage = pagedMessage
        for child in self.children:
            if isinstance(child, discord.ui.Container):
                child.add_item(discord.ui.TextDisplay(f"### Title"))
                child.add_item(discord.ui.Separator(visible=True))
                child.add_item(discord.ui.TextDisplay("your text will be here"))
                child.add_item(discord.ui.Separator(visible=True))
                child.add_item(discord.ui.TextDisplay(f"-# Page 1 of N"))

    container = discord.ui.Container(
    )

    action_row = discord.ui.ActionRow()

    def prepareView(self):
        for child in self.children:
            if isinstance(child, discord.ui.Container):
                child.children = []
                child.add_item(discord.ui.TextDisplay(f"### {self.pagedMessage.title}"))
                child.add_item(discord.ui.Separator(visible=True))
                child.add_item(discord.ui.TextDisplay(self.pagedMessage.getPage(0)))
                if self.pagedMessage.imageUrl is not None:
                    child.add_item(discord.ui.MediaGallery(discord.MediaGalleryItem(media=self.pagedMessage.imageUrl)))
                child.add_item(discord.ui.Separator(visible=True))
                child.add_item(discord.ui.TextDisplay(
                    f"-# Page 1 of {len(self.pagedMessage.pages)}"))

    @action_row.button(label="", style=discord.ButtonStyle.gray, emoji=config.firstPageEmoji)
    async def firstCallback(self, interaction: discord.Interaction, button):
        await interaction.response.defer(ephemeral=True)
        page = self.pagedMessage.getPage(0)
        self.pagedMessage.currentPage = 0
        for child in self.children:
            if isinstance(child, discord.ui.Container):
                child.clear_items()
                child.add_item(discord.ui.TextDisplay(f"### {self.pagedMessage.title}"))
                child.add_item(discord.ui.Separator(visible=True))
                child.add_item(discord.ui.TextDisplay(page))
                if self.pagedMessage.imageUrl is not None:
                    child.add_item(discord.ui.MediaGallery(discord.MediaGalleryItem(media=self.pagedMessage.imageUrl)))
                child.add_item(discord.ui.Separator(visible=True))
                child.add_item(discord.ui.TextDisplay(
                    f"-# Page {self.pagedMessage.currentPage + 1} of {len(self.pagedMessage.pages)}"))
        await interaction.message.edit(view=self)

    @action_row.button(label="", style=discord.ButtonStyle.gray, emoji=config.previousPageEmoji)
    async def leftCallback(self, interaction: discord.Interaction, button):
        await interaction.response.defer(ephemeral=True)
        page = self.pagedMessage.getPage(self.pagedMessage.currentPage - 1)
        for child in self.children:
            if isinstance(child, discord.ui.Container):
                child.clear_items()
                child.add_item(discord.ui.TextDisplay(f"### {self.pagedMessage.title}"))
                child.add_item(discord.ui.Separator(visible=True))
                child.add_item(discord.ui.TextDisplay(page))
                if self.pagedMessage.imageUrl is not None:
                    child.add_item(discord.ui.MediaGallery(discord.MediaGalleryItem(media=self.pagedMessage.imageUrl)))
                child.add_item(discord.ui.Separator(visible=True))
                child.add_item(discord.ui.TextDisplay(
                    f"-# Page {self.pagedMessage.currentPage+1} of {len(self.pagedMessage.pages)}"))
        await interaction.message.edit(view=self)

    @action_row.button(label="", style=discord.ButtonStyle.gray, emoji=config.nextPageEmoji)
    async def rightCallback(self, interaction: discord.Interaction, button):
        await interaction.response.defer(ephemeral=True)
        page = self.pagedMessage.getPage(self.pagedMessage.currentPage + 1)
        for child in self.children:
            if isinstance(child, discord.ui.Container):
                child.clear_items()
                child.add_item(discord.ui.TextDisplay(f"### {self.pagedMessage.title}"))
                child.add_item(discord.ui.Separator(visible=True))
                child.add_item(discord.ui.TextDisplay(page))
                if self.pagedMessage.imageUrl is not None:
                    child.add_item(discord.ui.MediaGallery(discord.MediaGalleryItem(media=self.pagedMessage.imageUrl)))
                child.add_item(discord.ui.Separator(visible=True))
                child.add_item(discord.ui.TextDisplay(
                    f"-# Page {self.pagedMessage.currentPage+1} of {len(self.pagedMessage.pages)}"))
        await interaction.message.edit(view=self)

    @action_row.button(label="", style=discord.ButtonStyle.gray, emoji=config.lastPageEmoji)
    async def lastCallback(self, interaction: discord.Interaction, button):
        await interaction.response.defer(ephemeral=True)
        page = self.pagedMessage.getPage(len(self.pagedMessage.pages)-1)
        self.pagedMessage.currentPage = len(self.pagedMessage.pages)-1
        for child in self.children:
            if isinstance(child, discord.ui.Container):
                child.clear_items()
                child.add_item(discord.ui.TextDisplay(f"### {self.pagedMessage.title}"))
                child.add_item(discord.ui.Separator(visible=True))
                child.add_item(discord.ui.TextDisplay(page))
                if self.pagedMessage.imageUrl is not None:
                    child.add_item(discord.ui.MediaGallery(discord.MediaGalleryItem(media=self.pagedMessage.imageUrl)))
                child.add_item(discord.ui.Separator(visible=True))
                child.add_item(discord.ui.TextDisplay(
                    f"-# Page {self.pagedMessage.currentPage + 1} of {len(self.pagedMessage.pages)}"))
        await interaction.message.edit(view=self)

    @action_row.button(label="", style=discord.ButtonStyle.green, emoji=config.saveEmoji)
    async def saveCallback(self, interaction: discord.Interaction, button):
        res = "\n".join(self.pagedMessage.pages)
        with open(f'{interaction.message.id}.txt', "w") as file:
            file.write(res)
        with open(f'{interaction.message.id}.txt', "rb") as file:
            await interaction.response.send_message(file=discord.File(file, f'{interaction.message.id}.txt'))
            os.remove(f'{interaction.message.id}.txt')
