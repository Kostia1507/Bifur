from discord import Embed
from discord.ext import commands

from service import translateService


class TranslatorCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, event):
        if event.emoji.name in translateService.langs.keys():
            msg = await self.bot.get_channel(event.channel_id).fetch_message(event.message_id)
            loop = ""
            if msg.content is not None and len(msg.content) > 0:
                loop += msg.content + "\n\n"
            for embed in msg.embeds:
                loop += f"{embed.title}\n{embed.description}\n\n"
            if len(loop) > 0:
                user = await self.bot.fetch_user(event.user_id)
                embed = Embed(description=translateService.translateToEmoji(loop, event.emoji.name))
                embed.set_author(name=user.name, icon_url=user.avatar.url)
                embed.set_footer(text=f'original message from {msg.author.name}')
                await msg.reply(embed=embed, mention_author=False)
