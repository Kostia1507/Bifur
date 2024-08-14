import psycopg2
import config

channels = []
reactions = []


def init():
    channels.clear()
    reactions.clear()
    conn = psycopg2.connect(
        host=config.host,
        database=config.database,
        user=config.user,
        password=config.password,
        port=config.port
    )
    cur = conn.cursor()
    cur.execute("SELECT * FROM reactions")
    rows = cur.fetchall()
    for react in rows:
        channels.append(react[0])
        reactions.append(react[1])
    cur.close()
    conn.close()


def add(channel_id, emoji):
    channels.append(channel_id)
    reactions.append(emoji.strip())
    conn = psycopg2.connect(
        host=config.host,
        database=config.database,
        user=config.user,
        password=config.password,
        port=config.port
    )
    cur = conn.cursor()
    cur.execute("INSERT INTO reactions(channel_id, emoji) VALUES (%s, %s);", (channel_id, emoji))
    conn.commit()
    cur.close()
    conn.close()


def remove(channel_id):
    conn = psycopg2.connect(
        host=config.host,
        database=config.database,
        user=config.user,
        password=config.password,
        port=config.port
    )
    cur = conn.cursor()
    cur.execute("DELETE FROM reactions WHERE channel_id='" + str(channel_id) + "'")
    conn.commit()
    cur.close()
    conn.close()
    init()


def checkForReaction(channel_id):
    res = []
    for i in range(len(channels)):
        if channels[i] == channel_id:
            res.append(reactions[i])
    return res