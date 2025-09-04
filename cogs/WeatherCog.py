from datetime import datetime

import aiohttp
from discord.ext import commands

import config
from cogs import LogCog
from service.weatherService import getCoordinates, getWeather


class WeatherCog(commands.Cog):

    def __init__(self, bot):
        LogCog.logSystem('Weather cog loaded')
        self.bot = bot

    @commands.command()
    async def weather(self, ctx, *args):
        nameOfCity = " ".join(args)
        lat, lon, nameOfCity = await getCoordinates(nameOfCity)
        weather = await getWeather(lat, lon, nameOfCity, 2, 24, ctx.author.id)
        await ctx.send(view=weather)

    @commands.command()
    async def weatherd(self, ctx, *args):
        nameOfCity = " ".join(args)
        lat, lon, nameOfCity = await getCoordinates(nameOfCity)
        weather = await getWeather(lat, lon, nameOfCity, 1, 40, ctx.author.id)
        await ctx.send(view=weather)
