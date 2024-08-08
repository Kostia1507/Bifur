import os

import discord
from discord.ext import commands

from cogs import LogCog
from models import Radio
from service import musicService, musicViewService
from service.localeService import getLocale


async def connect_to_user_voice(ctx):
    if not ctx.guild.voice_client:
        if ctx.message.author.voice is not None:
            channel = ctx.message.author.voice.channel
            await channel.connect()
            return 1
        else:
            await ctx.send(getLocale('not-connected-to-voice', ctx.author.id))
            return 0


async def connect_to_user_voiceInteraction(interaction):
    if not interaction.guild.voice_client:
        if interaction.user.voice is not None:
            channel = interaction.user.voice.channel
            await channel.connect()
            return 1
        else:
            await interaction.response.send_message(
                getLocale('not-connected-to-voice', interaction.user.id), ephemeral=True, delete_after=15)
            return 0


class RadioCog(commands.Cog):

    def __init__(self, bot):
        LogCog.logSystem('Radio cog loaded')
        self.bot = bot

    @commands.command()
    async def radio(self, ctx, radio_name):
        res = await connect_to_user_voice(ctx)
        if res == 0:
            return 0
        retStatus = musicService.startRadio(radio_name, ctx.guild.id, ctx.author.name,
                                            ctx.channel.id, ctx.author.id, True)
        if retStatus:
            await ctx.message.add_reaction('✅')
            await musicViewService.createPlayer(ctx)
        else:
            await ctx.message.add_reaction('❌')

    @commands.command()
    async def addradio(self, ctx, radio_name):
        res = await connect_to_user_voice(ctx)
        if res == 0:
            return 0
        retStatus = musicService.startRadio(radio_name, ctx.guild.id, ctx.author.name,
                                            ctx.channel.id, ctx.author.id, False)
        if retStatus:
            await ctx.message.add_reaction('✅')
        else:
            await ctx.message.add_reaction('❌')
