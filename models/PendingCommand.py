import psycopg2

import config


def get_pending_command(command_id):
    conn = psycopg2.connect(
        host=config.host,
        database=config.database,
        user=config.user,
        password=config.password,
        port=config.port
    )
    cur = conn.cursor()
    cur.execute("SELECT * FROM autocommands WHERE id=%s", (command_id,))
    row = cur.fetchone()
    if row is not None:
        pc = PendingCommand(row[1], row[2], row[3], row[4])
        pc.id = row[0]
        pc.counter = row[5]
        return pc
    return None

class PendingCommand:

    def __init__(self, channelId, interval, cmdType, args):
        self.channelId = channelId
        self.interval = interval
        self.cmdType = cmdType
        self.args = args
        self.counter = 0
        self.id = 0

    def insert(self):
        conn = psycopg2.connect(
            host=config.host,
            database=config.database,
            user=config.user,
            password=config.password,
            port=config.port
        )
        cur = conn.cursor()
        cur.execute("INSERT INTO autocommands(channel_id, interval, cmd_type, args, counter)"
                    " VALUES (%s, %s, %s, %s, 0);", (self.channelId, self.interval, self.cmdType, self.args))
        cur.execute('SELECT LASTVAL()')
        self.id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()

    def update_counter(self):
        self.counter += 1
        conn = psycopg2.connect(
            host=config.host,
            database=config.database,
            user=config.user,
            password=config.password,
            port=config.port
        )
        cur = conn.cursor()
        cur.execute("UPDATE autocommands SET counter = %s where id = %s", (self.counter, self.id))
        conn.commit()
        cur.close()
        conn.close()

    def init_counter(self):
        self.counter = 0
        conn = psycopg2.connect(
            host=config.host,
            database=config.database,
            user=config.user,
            password=config.password,
            port=config.port
        )
        cur = conn.cursor()
        cur.execute("UPDATE autocommands SET counter = %s where id = %s", (self.counter, self.id))
        conn.commit()
        cur.close()
        conn.close()
