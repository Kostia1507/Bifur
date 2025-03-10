import asyncpg

import config

autoroles = {}

async def init():
    conn = await asyncpg.connect(
        host=config.host,
        database=config.database,
        user=config.user,
        password=config.password,
        port=config.port
    )
    rows = conn.fetch("SELECT * from autoroles")
    for row in rows:
        autoroles[row[0]] = row[1]
    await conn.close()

async def add_role(guild_id, role_id):
    conn = await asyncpg.connect(
        host=config.host,
        database=config.database,
        user=config.user,
        password=config.password,
        port=config.port
    )
    row = await conn.fetchrow("SELECT * from autoroles WHERE guild_id = $1", guild_id)
    if row is None:
        await conn.execute("INSERT INTO autoroles(guild_id, role_id) VALUES ($1, $2);",
                    (guild_id, role_id))
    else:
        await conn.execute("UPDATE autoroles SET role_id= $1 WHERE guild_id=$2", role_id, guild_id)
    await conn.close()