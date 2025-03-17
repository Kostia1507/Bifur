import functools
import typing

import discord
from discord.ext import commands

import config
from service.localeService import getLocale

# this variable is initialized in main.py
bot = commands.Bot(command_prefix=config.prefix, intents=discord.Intents.default())


async def run_blocking(blocking_func: typing.Callable, *args, **kwargs) -> typing.Any:
    """Runs a blocking function in a non-blocking way"""
    func = functools.partial(blocking_func, *args, **kwargs)
    return await bot.loop.run_in_executor(None, func)


async def is_owner(ctx):
    return ctx.author.id in config.owners


async def is_in_vc(ctx):
    vc = ctx.guild.voice_client
    if vc is not None:
        members = vc.channel.members
        for member in members:
            if member.id == ctx.author.id:
                return True
    await ctx.send(await getLocale('not-in-voice', ctx.author.id))
    return False


async def is_in_vcInteraction(interaction):
    vc = interaction.guild.voice_client
    if vc is not None:
        members = vc.channel.members
        for member in members:
            if member.id == interaction.user.id:
                return True
    await interaction.response.send_message(
        await getLocale('not-in-voice', interaction.user.id), ephemeral=True, delete_after=15)
    return False


def deleteNotNumbers(string):
    result = ''
    for char in string:
        if str(char).isnumeric():
            result += str(char)
    return result
