import psycopg2

import config


def is_premium(user_id):
    conn = psycopg2.connect(
        host=config.host,
        database=config.database,
        user=config.user,
        password=config.password,
        port=config.port
    )
    cur = conn.cursor()
    cur.execute("SELECT * from premium_users WHERE user_id=%s", (user_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return False if row is None else True


def add_premium(user_id):
    conn = psycopg2.connect(
        host=config.host,
        database=config.database,
        user=config.user,
        password=config.password,
        port=config.port
    )
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO premium_users(user_id) VALUES (%s);", (user_id,))
    except psycopg2.OperationalError:
        cur.close()
        conn.close()
        return True
    conn.commit()
    cur.close()
    conn.close()
    return True


def delete_premium(user_id):
    conn = psycopg2.connect(
        host=config.host,
        database=config.database,
        user=config.user,
        password=config.password,
        port=config.port
    )
    cur = conn.cursor()
    try:
        cur.execute("DELETE from premium_users WHERE user_id=%s;", (user_id,))
    except psycopg2.OperationalError:
        cur.close()
        conn.close()
        return True
    conn.commit()
    cur.close()
    conn.close()
    return True
