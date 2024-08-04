import functools
import typing

import discord
from discord.ext import commands

import config

# this variable is initialized in main.py
bot = commands.Bot(command_prefix=config.prefix, intents=discord.Intents.default())


async def run_blocking(blocking_func: typing.Callable, *args, **kwargs) -> typing.Any:
    """Runs a blocking function in a non-blocking way"""
    func = functools.partial(blocking_func, *args, **kwargs)
    return await bot.loop.run_in_executor(None, func)
