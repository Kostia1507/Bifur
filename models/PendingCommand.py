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
    cur.execute("SELECT id, channel_id, interval, start_hour_utc, cmd_type, args FROM autocmds WHERE id=%s", (command_id,))
    row = cur.fetchone()
    if row is not None:
        pc = PendingCommand(row[1], row[2], row[3], row[4], row[5])
        pc.id = row[0]
        return pc
    return None

def get_pending_commands_by_channel(channel_id):
    conn = psycopg2.connect(
        host=config.host,
        database=config.database,
        user=config.user,
        password=config.password,
        port=config.port
    )
    cur = conn.cursor()
    cur.execute("SELECT id, channel_id, interval, start_hour_utc, cmd_type, args FROM autocmds WHERE channel_id=%s", (channel_id,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    cmds = []
    for row in rows:
        pc = PendingCommand(row[1], row[2], row[3], row[4], row[5])
        pc.id = row[0]
        cmds.append(pc)
    return cmds

def get_all_pending_commands():
    conn = psycopg2.connect(
        host=config.host,
        database=config.database,
        user=config.user,
        password=config.password,
        port=config.port
    )
    cur = conn.cursor()
    cur.execute("SELECT id, channel_id, interval, start_hour_utc, cmd_type, args FROM autocmds")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    cmds = []
    for row in rows:
        pc = PendingCommand(row[1], row[2], row[3], row[4], row[5])
        pc.id = row[0]
        cmds.append(pc)
    return cmds

class PendingCommand:

    def __init__(self, channelId, interval, startHour, cmdType, args):
        self.channelId = channelId
        self.interval = interval
        self.cmdType = cmdType
        self.startHour = startHour
        self.args = args
        self.id = None

    def insert(self):
        conn = psycopg2.connect(
            host=config.host,
            database=config.database,
            user=config.user,
            password=config.password,
            port=config.port
        )
        cur = conn.cursor()
        cur.execute("INSERT INTO autocmds(channel_id, interval, cmd_type, args, start_hour_utc)"
                    " VALUES (%s, %s, %s, %s, %s)", (self.channelId, self.interval, self.cmdType, self.args, self.startHour))
        cur.execute('SELECT LASTVAL()')
        self.id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()

    def update(self):
        conn = psycopg2.connect(
            host=config.host,
            database=config.database,
            user=config.user,
            password=config.password,
            port=config.port
        )
        cur = conn.cursor()
        cur.execute("UPDATE autocmds SET start_hour_utc = %s, cmd_type = %s, args = %s, interval = %s where id = %s",
                    (self.startHour, self.cmdType, self.args, self.interval, self.id))
        conn.commit()
        cur.close()
        conn.close()
