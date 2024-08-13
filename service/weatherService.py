from datetime import datetime

import aiohttp

import config
from cogs import LogCog
from service.localeService import getLocale


async def getCoordinates(city):
    async with aiohttp.ClientSession() as session:
        async with session.get(
                f'https://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={config.weatherKey}') as response:
            if response.status == 200:
                js = await response.json()
                return js[0]['lat'], js[0]['lon'], js[0]['country'] + ':' + js[0]['name']
            else:
                LogCog.logError(f'HTTP STATUS: {response.status} on getCoordinates() for {city}')


# lat and lon you can get from getCoordinates(city)
# interval - 1 = 3 hours.
# maxDT = rows count to output. Max: 40. Remember that dt = 3 hours
# pass userId for getting locales
async def getWeather(lat: str, lon: str, nameOfCity: str, interval, maxDT, userId):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}'
                               f'&lang={getLocale("lang", userId)}&appid={config.weatherKey}') as response:
            if response.status == 200:
                js = await response.json()
                weather = js['weather']
                main = js['main']
                res = f'{getLocale("weather-in", userId)} **{nameOfCity}**\n{getLocale("now", userId)}: **' + \
                      str(round(main['temp'] - 273.15, 1)) + '° **|' + weather[0]['main'] + '|'
        async with session.get('https://api.openweathermap.org/data/2.5/forecast?lat=' + str(lat) + '&lon=' + str(
                lon) + f'&lang={getLocale("lang", userId)}&appid=' + config.weatherKey) as response:
            js = await response.json()
            listW = js['list']
            lastDay = -1
            for i in range(0, min(maxDT, len(listW)), interval):
                if datetime.fromtimestamp(listW[i]['dt']).day != lastDay:
                    res += '**\n' + str(datetime.fromtimestamp(listW[i]['dt']).strftime('%A')) + ' ' + \
                           str(datetime.fromtimestamp(listW[i]['dt']).day) + '.' + str(
                        datetime.fromtimestamp(listW[i]['dt']).month) + '**'
                    lastDay = datetime.fromtimestamp(listW[i]['dt']).day
                res += '\n' + str(datetime.fromtimestamp(listW[i]['dt']).hour) + \
                       ':00** ' + str(round(listW[i]['main']['temp'] - 273.15, 1)) + \
                       '°** |' + listW[i]['weather'][0]['main'] + '|(' + listW[i]['weather'][0]['description'] + ')'
            res = res.replace('|Clouds|', f'{getLocale("clouds", userId)}:cloud:')
            res = res.replace('|Clear|', f'{getLocale("clear", userId)}:sunny:')
            res = res.replace('|Snow|', f'{getLocale("snow", userId)}:snowflake:')
            res = res.replace('|Rain|', f'{getLocale("rain", userId)}:cloud_rain:')
            res = res.replace('Monday', getLocale('monday', userId))
            res = res.replace('Tuesday', getLocale('tuesday', userId))
            res = res.replace('Wednesday', getLocale('wednesday', userId))
            res = res.replace('Thursday', getLocale('thursday', userId))
            res = res.replace('Friday', getLocale('friday', userId))
            res = res.replace('Saturday', getLocale('saturday', userId))
            res = res.replace('Sunday', getLocale('sunday', userId))
            return res
