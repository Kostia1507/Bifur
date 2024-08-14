import aiohttp
import discord
from discord.ext import commands

from cogs import LogCog
from service import pictureService


class WarCog(commands.Cog):

    def __init__(self, bot):
        LogCog.logSystem('War cog loaded')
        self.oldMsg = None
        self.bot = bot

    @commands.command(aliases=['alerts'])
    async def alert(self, ctx):
        await pictureService.download_image("https://alerts.com.ua/map.png", "temp/alert.png")
        await ctx.send(file=discord.File("temp/alert.png"))

    @commands.command()
    async def rus(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://russianwarship.rip/api/v1/statistics/latest') as response:
                if response.status == 200:
                    body = await response.json()
                    body = body["data"]
                    s = body['stats']
                    i = body['increase']

                    res = '**День ' + str(body['day']) + '\n**Особовий склад:** ' + \
                          str(s['personnel_units']) + "** +" + str(i['personnel_units'])
                    res += '\nТанки:** ' + str(s['tanks']) + '**'
                    if i['tanks'] > 0:
                        res += ' +' + str(i['tanks'])
                    res += '\nБроньована бойова техніка:** ' + str(s['armoured_fighting_vehicles']) + '**'
                    if i['armoured_fighting_vehicles'] > 0:
                        res += ' +' + str(i['armoured_fighting_vehicles'])
                    res += '\nАртилерійські системи:** ' + str(s['artillery_systems']) + '**'
                    if i['artillery_systems'] > 0:
                        res += ' +' + str(i['artillery_systems'])
                    res += '\nРСЗВ:** ' + str(s['mlrs']) + '**'
                    if i['mlrs'] > 0:
                        res += ' +' + str(i['mlrs'])
                    res += '\nППО:** ' + str(s['aa_warfare_systems']) + '**'
                    if i['aa_warfare_systems'] > 0:
                        res += ' +' + str(i['aa_warfare_systems'])
                    res += '\nЛітаки:** ' + str(s['planes']) + '**'
                    if i['planes'] > 0:
                        res += ' +' + str(i['planes'])
                    res += '\nГелікоптери:** ' + str(s['helicopters']) + '**'
                    if i['helicopters'] > 0:
                        res += ' +' + str(i['helicopters'])
                    res += '\nАвтомобільна техніка:** ' + str(s['vehicles_fuel_tanks']) + '**'
                    if i['vehicles_fuel_tanks'] > 0:
                        res += ' +' + str(i['vehicles_fuel_tanks'])
                    await ctx.send(res)
