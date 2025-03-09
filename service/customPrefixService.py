import asyncpg

import config

prefixes = {}


def getPrefix(guild_id):
    if guild_id in prefixes.keys():
        return prefixes[guild_id]
    else:
        return None


async def setPrefix(guild_id, prefix):
    prefixes[guild_id] = prefix
    conn = await asyncpg.connect(
        host=config.host,
        database=config.database,
        user=config.user,
        password=config.password,
        port=config.port
    )
    await conn.execute("DELETE FROM customprefixes WHERE guild_id = $1", guild_id)
    await conn.execute("INSERT INTO customprefixes(guild_id, prefix) VALUES ($1, $2)", guild_id, prefix)
    await conn.close()


async def init():
    prefixes.clear()
    conn = await asyncpg.connect(
        host=config.host,
        database=config.database,
        user=config.user,
        password=config.password,
        port=config.port
    )
    rows = await conn.fetch("SELECT * FROM customprefixes")
    await conn.close()
    for row in rows:
        prefixes[row[0]] = row[1]
