import asyncpg

import config
from cogs import LogCog
from models.Song import Song
from service.localeService import getLocale


class Radio:

    def __init__(self, radio_id, name, owner, is_shared):
        self.radio_id = radio_id
        self.name = name
        self.owner = owner
        self.is_shared = is_shared

    async def getTracks(self, user_id):
        if self.is_shared or user_id == self.owner or user_id in await self.getEditors():
            conn = await asyncpg.connect(
                host=config.host,
                database=config.database,
                user=config.user,
                password=config.password,
                port=config.port
            )
            rows = await conn.fetch("SELECT * FROM tracks where list = '" + str(self.radio_id) + "'")
            await conn.close()

            songs = []
            for entry in rows:
                song = Song(entry[2], False)
                song.name = entry[1]
                song.duration = entry[4]
                song.trackId = entry[0]
                song.radioId = entry[3]
                songs.append(song)
            return songs

    async def getInfo(self, user_id):
        if self.is_shared or user_id == self.owner or user_id in await self.getEditors():
            tracks = await self.getTracks(user_id)
            tracks.sort(key=lambda radioEntry: radioEntry.trackId)
            result = ""
            for t in tracks:
                if t.name is None or len(str(t.name)) == 0:
                    await t.updateFromWeb()
                    await t.updateInDB()
                result += f'{t.trackId} - {t.name}\n'
            return f'ID: {self.radio_id} Name: {self.name}', result
        else:
            return getLocale("list-not-found", user_id)

    async def getEditors(self):
        conn = await asyncpg.connect(
            host=config.host,
            database=config.database,
            user=config.user,
            password=config.password,
            port=config.port
        )
        rows = await conn.fetch("SELECT user_id FROM radioeditors where radio_id = '" + str(self.radio_id) + "'")
        await conn.close()
        editors = []
        for i in rows:
            editors.append(i[0])
        return editors

    async def addEditor(self, user_id):
        rows = await self.getEditors()
        if user_id in rows:
            LogCog.logDebug(f'{user_id} already is an editor of radio {self.radio_id}')
            return 0
        else:
            conn = await asyncpg.connect(
                host=config.host,
                database=config.database,
                user=config.user,
                password=config.password,
                port=config.port
            )
            await conn.execute("INSERT INTO radioeditors(radio_id, user_id) VALUES ($1, $2);", self.radio_id, user_id)
            await conn.close()
            return 1

    async def removeEditor(self, user_id):
        conn = await asyncpg.connect(
            host=config.host,
            database=config.database,
            user=config.user,
            password=config.password,
            port=config.port
        )
        await conn.execute("DELETE FROM radioeditors WHERE radio_id = $1 and user_id = $2", self.radio_id, user_id)
        await conn.close()

    async def rename(self, newname, user_id):
        if user_id == self.owner:
            conn = await asyncpg.connect(
                host=config.host,
                database=config.database,
                user=config.user,
                password=config.password,
                port=config.port
            )
            await conn.execute("UPDATE radios SET name = $1 where id = $2", newname, self.radio_id)
            await conn.close()

    async def delete(self, user_id):
        if user_id == self.owner:
            tracks = await self.getTracks(user_id)
            conn = await asyncpg.connect(
                host=config.host,
                database=config.database,
                user=config.user,
                password=config.password,
                port=config.port
            )
            for i in tracks:
                await conn.execute("DELETE FROM tracks WHERE id='" + str(i.trackId) + "'")
            await conn.execute("DELETE FROM radios WHERE id='" + str(self.radio_id) + "'")
            await conn.close()
            return True
        else:
            return False
