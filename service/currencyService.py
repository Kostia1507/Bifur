import aiohttp

import config

currency = {}


async def updateCurrency():
    async with aiohttp.ClientSession() as session:
        async with session.get(f'http://data.fixer.io/api/latest?access_key={config.fixerKey}') as response:
            if response.status == 200:
                body = await response.json()
                loop = body["rates"]
                for key in loop.keys():
                    currency[key] = float(loop[key])
