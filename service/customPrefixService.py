import psycopg2

import config

prefixes = {}


def getPrefix(guild_id):
    if guild_id in prefixes.keys():
        return prefixes[guild_id]
    else:
        return None


def setPrefix(guild_id, prefix):
    prefixes[guild_id] = prefix
    conn = psycopg2.connect(
        host=config.host,
        database=config.database,
        user=config.user,
        password=config.password,
        port=config.port
    )
    cur = conn.cursor()
    cur.execute("DELETE FROM customprefixes WHERE guild_id = %s);", (guild_id, ))
    conn.commit()
    cur.execute("INSERT INTO customprefixes(guild_id, prefix) VALUES (%s, %s);", (guild_id, prefix))
    conn.commit()
    cur.close()
    conn.close()


def init():
    prefixes.clear()
    conn = psycopg2.connect(
        host=config.host,
        database=config.database,
        user=config.user,
        password=config.password,
        port=config.port
    )
    cur = conn.cursor()
    cur.execute("SELECT * FROM customprefixes")
    rows = cur.fetchall()
    for row in rows:
        prefixes[row[0]] = row[1]
    cur.close()
    conn.close()