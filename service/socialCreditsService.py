import traceback

import psycopg2

import config


def get_user_credits(user_id):
    conn = psycopg2.connect(
        host=config.host,
        database=config.database,
        user=config.user,
        password=config.password,
        port=config.port
    )
    cur = conn.cursor()
    try:
        cur.execute("SELECT amount FROM social_credit WHERE user_id=%s", (user_id,))
    except Exception as error:
        traceback.print_exception(type(error), error, error.__traceback__)
        print(error)
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if row is None:
        return 0
    return row[0]


def updateCounter(user_id, value):
    conn = psycopg2.connect(
        host=config.host,
        database=config.database,
        user=config.user,
        password=config.password,
        port=config.port
    )
    cur = conn.cursor()
    try:
        cur.execute("""
                        INSERT INTO social_credit(user_id, amount)
                        VALUES (%s, %s)
                        ON CONFLICT (user_id)
                        DO UPDATE SET amount = social_credit.amount + EXCLUDED.amount;
                        """, (user_id, value))
    except Exception as error:
        traceback.print_exception(type(error), error, error.__traceback__)
        print(error)
    conn.commit()
    cur.close()
    conn.close()
