import asyncpg
import config

channels = []
reactions = []


async def init():
    channels.clear()
    reactions.clear()
    conn = await asyncpg.connect(
        host=config.host,
        database=config.database,
        user=config.user,
        password=config.password,
        port=config.port
    )
    rows = await conn.fetch("SELECT * FROM reactions")
    await conn.close()
    for react in rows:
        channels.append(react[0])
        reactions.append(react[1])


async def add(channel_id, emoji):
    channels.append(channel_id)
    reactions.append(emoji.strip())
    conn = await asyncpg.connect(
        host=config.host,
        database=config.database,
        user=config.user,
        password=config.password,
        port=config.port
    )
    await conn.execute("INSERT INTO reactions(channel_id, emoji) VALUES (%s, %s);", (channel_id, emoji))
    await conn.commit()
    await conn.close()


async def remove(channel_id):
    conn = await asyncpg.connect(
        host=config.host,
        database=config.database,
        user=config.user,
        password=config.password,
        port=config.port
    )
    await conn.execute("DELETE FROM reactions WHERE channel_id='" + str(channel_id) + "'")
    conn.commit()
    await conn.close()
    await init()


def checkForReaction(channel_id):
    res = []
    for i in range(len(channels)):
        if channels[i] == channel_id:
            res.append(reactions[i])
    return res