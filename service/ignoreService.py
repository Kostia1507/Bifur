import psycopg2

import config
from service.localeService import getLocale

ignoredChannels = []


def initFromDB():
    conn = psycopg2.connect(
        host=config.host,
        database=config.database,
        user=config.user,
        password=config.password,
        port=config.port
    )
    cur = conn.cursor()
    cur.execute("SELECT * FROM ignored_channels")
    channels = cur.fetchall()
    for channel in channels:
        ignoredChannels.append(channel[0])
    cur.close()
    conn.close()


async def manageIgnoredChannels(ctx, channel_id):
    if channel_id in ignoredChannels:
        ignoredChannels.remove(channel_id)
        conn = psycopg2.connect(
            host=config.host,
            database=config.database,
            user=config.user,
            password=config.password,
            port=config.port
        )
        cur = conn.cursor()
        cur.execute('DELETE FROM ignored_channels WHERE channel_id = %s', (ctx.channel.id,))
        conn.commit()
        cur.close()
        conn.close()
        await ctx.send(getLocale("ignore-off", ctx.author.id))
    else:
        ignoredChannels.append(channel_id)
        conn = psycopg2.connect(
            host=config.host,
            database=config.database,
            user=config.user,
            password=config.password,
            port=config.port
        )
        cur = conn.cursor()
        cur.execute("INSERT INTO ignored_channels(channel_id) VALUES (%s);", (channel_id,))
        conn.commit()
        cur.close()
        conn.close()
        await ctx.send(getLocale("ignore-on", ctx.author.id))
