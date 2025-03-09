import psycopg2
import asyncpg

import config


async def get_pending_command(command_id):
    conn = await asyncpg.connect(
        host=config.host,
        database=config.database,
        user=config.user,
        password=config.password,
        port=config.port
    )
    rows = await conn.fetch("SELECT id, channel_id, interval, start_hour_utc, cmd_type, args FROM autocmds WHERE id=$1",
                            command_id)
    await conn.close()
    if rows is not None and len(rows) > 0:
        row = rows[0]
        pc = PendingCommand(row[1], row[2], row[3], row[4], row[5])
        pc.id = row[0]
        return pc
    return None


async def get_pending_commands_by_channel(channel_id):
    conn = await asyncpg.connect(
        host=config.host,
        database=config.database,
        user=config.user,
        password=config.password,
        port=config.port
    )
    rows = await conn.fetch(
        "SELECT id, channel_id, interval, start_hour_utc, cmd_type, args FROM autocmds WHERE channel_id=$1", channel_id)
    await conn.close()
    cmds = []
    for row in rows:
        pc = PendingCommand(row[1], row[2], row[3], row[4], row[5])
        pc.id = row[0]
        cmds.append(pc)
    return cmds


async def get_all_pending_commands():
    conn = await asyncpg.connect(
        host=config.host,
        database=config.database,
        user=config.user,
        password=config.password,
        port=config.port
    )
    rows = await conn.fetch("SELECT id, channel_id, interval, start_hour_utc, cmd_type, args FROM autocmds")
    await conn.close()
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

    async def insert(self):
        conn = await asyncpg.connect(
            host=config.host,
            database=config.database,
            user=config.user,
            password=config.password,
            port=config.port
        )
        await conn.execute("INSERT INTO autocmds(channel_id, interval, cmd_type, args, start_hour_utc)"
                           " VALUES ($1, $2, $3, $4, $5)",
                           self.channelId, int(self.interval), self.cmdType, self.args, int(self.startHour))
        last = await conn.fetchrow('SELECT LASTVAL()')
        self.id = last[0]
        await conn.close()

    async def update(self):
        conn = await asyncpg.connect(
            host=config.host,
            database=config.database,
            user=config.user,
            password=config.password,
            port=config.port
        )
        await conn.execute(
            "UPDATE autocmds SET start_hour_utc = $1, cmd_type = $2, args = $3, interval = $4 where id = $5",
            int(self.startHour), self.cmdType, self.args, int(self.interval), int(self.id))
        await conn.close()
