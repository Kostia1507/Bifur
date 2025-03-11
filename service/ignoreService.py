import asyncpg

import config
from service.localeService import getLocale

ignoredChannels = []


async def initFromDB():
    conn = await asyncpg.connect(
        host=config.host,
        database=config.database,
        user=config.user,
        password=config.password,
        port=config.port
    )
    channels = await conn.fetch("SELECT * FROM ignored_channels")
    await conn.close()
    for channel in channels:
        ignoredChannels.append(channel[0])


async def manageIgnoredChannels(ctx, channel_id):
    if channel_id in ignoredChannels:
        ignoredChannels.remove(channel_id)
        conn = await asyncpg.connect(
            host=config.host,
            database=config.database,
            user=config.user,
            password=config.password,
            port=config.port
        )
        await conn.execute('DELETE FROM ignored_channels WHERE channel_id = %s', (ctx.channel.id,))
        conn.commit()
        await conn.close()
        await ctx.send(await getLocale("ignore-off", ctx.author.id))
    else:
        ignoredChannels.append(channel_id)
        conn = await asyncpg.connect(
            host=config.host,
            database=config.database,
            user=config.user,
            password=config.password,
            port=config.port
        )
        await conn.execute("INSERT INTO ignored_channels(channel_id) VALUES (%s);", (channel_id,))
        await conn.close()
        await ctx.send(await getLocale("ignore-on", ctx.author.id))
