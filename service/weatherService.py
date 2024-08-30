from datetime import datetime

import aiohttp

import config
from cogs import LogCog
from service.localeService import getUserLang, getLocaleByLang


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
    userLang = getUserLang(userId)
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}'
                               f'&lang={getLocaleByLang("lang", userLang)}&appid={config.weatherKey}') as response:
            if response.status == 200:
                js = await response.json()
                weather = js['weather']
                main = js['main']
                res = f'{getLocaleByLang("weather-in", userLang)} **{nameOfCity}**\n{getLocaleByLang("now", userLang)}: **' + \
                      str(round(main['temp'] - 273.15, 1)) + '° **|' + weather[0]['main'] + '|'
        async with session.get('https://api.openweathermap.org/data/2.5/forecast?lat=' + str(lat) + '&lon=' + str(
                lon) + f'&lang={getLocaleByLang("lang", userLang)}&appid=' + config.weatherKey) as response:
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

            res = res.replace('|Clouds|', f'{getLocaleByLang("clouds", userLang)}:cloud:')
            res = res.replace('|Clear|', f'{getLocaleByLang("clear", userLang)}:sunny:')
            res = res.replace('|Snow|', f'{getLocaleByLang("snow", userLang)}:snowflake:')
            res = res.replace('|Rain|', f'{getLocaleByLang("rain", userLang)}:cloud_rain:')
            res = res.replace('Monday', getLocaleByLang('monday', userLang))
            res = res.replace('Tuesday', getLocaleByLang('tuesday', userLang))
            res = res.replace('Wednesday', getLocaleByLang('wednesday', userLang))
            res = res.replace('Thursday', getLocaleByLang('thursday', userLang))
            res = res.replace('Friday', getLocaleByLang('friday', userLang))
            res = res.replace('Saturday', getLocaleByLang('saturday', userLang))
            res = res.replace('Sunday', getLocaleByLang('sunday', userLang))
            return res
