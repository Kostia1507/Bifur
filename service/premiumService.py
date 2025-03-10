import asyncpg

import config


async def get_all_premiums():
    conn = await asyncpg.connect(
        host=config.host,
        database=config.database,
        user=config.user,
        password=config.password,
        port=config.port
    )
    rows = await conn.fetch("SELECT * from premium_users")
    await conn.close()
    return rows


async def is_premium(user_id):
    conn = await asyncpg.connect(
            host=config.host,
            database=config.database,
            user=config.user,
            password=config.password,
            port=config.port
    )
    row = await conn.fetchrow("SELECT * from premium_users WHERE user_id=$1", user_id)
    await conn.close()
    return False if row is None else True



async def add_premium(user_id):
    conn = await asyncpg.connect(
        host=config.host,
        database=config.database,
        user=config.user,
        password=config.password,
        port=config.port
    )
    await conn.execute("INSERT INTO premium_users(user_id) VALUES ($1);", user_id,)
    await conn.close()
    return True


async def delete_premium(user_id):
    conn = await asyncpg.connect(
        host=config.host,
        database=config.database,
        user=config.user,
        password=config.password,
        port=config.port
    )
    await conn.execute("DELETE from premium_users WHERE user_id=$1;", user_id,)
    await conn.close()
    return True

async def get_premium_count():
    conn = await asyncpg.connect(
        host=config.host,
        database=config.database,
        user=config.user,
        password=config.password,
        port=config.port
    )
    count = await conn.fetchrow("SELECT COUNT(user_id) FROM premium_users")
    await conn.close()
    return count[0]
