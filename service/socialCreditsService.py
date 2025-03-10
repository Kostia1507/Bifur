import asyncpg

import config


async def get_user_credits(user_id):
    conn = await asyncpg.connect(
        host=config.host,
        database=config.database,
        user=config.user,
        password=config.password,
        port=config.port
    )
    row = await conn.fetchrow("SELECT amount FROM social_credit WHERE user_id=$1", user_id)
    await conn.close()
    if row is None:
        return 0
    return row[0]


async def updateCounter(user_id, value):
    conn = await asyncpg.connect(
        host=config.host,
        database=config.database,
        user=config.user,
        password=config.password,
        port=config.port
    )
    await conn.execute("""
                    INSERT INTO social_credit(user_id, amount)
                    VALUES ($1, $2)
                    ON CONFLICT (user_id)
                    DO UPDATE SET amount = social_credit.amount + EXCLUDED.amount;
                    """, user_id, value)
    await conn.close()
