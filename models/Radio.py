import psycopg2

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

    def getTracks(self, user_id):
        if self.is_shared or user_id == self.owner or user_id in self.getEditors():
            conn = psycopg2.connect(
                host=config.host,
                database=config.database,
                user=config.user,
                password=config.password,
                port=config.port
            )
            cur = conn.cursor()
            cur.execute("SELECT * FROM tracks where list = '" + str(self.radio_id) + "'")
            rows = cur.fetchall()
            cur.close()
            conn.close()

            songs = []
            for entry in rows:
                song = Song(entry[2], False)
                song.name = entry[1]
                song.duration = entry[4]
                song.trackId = entry[0]
                song.radioId = entry[3]
                songs.append(song)
            return songs

    def getInfo(self, user_id):
        if self.is_shared or user_id == self.owner or user_id in self.getEditors():
            tracks = self.getTracks(user_id)
            tracks.sort(key=lambda radioEntry: radioEntry.trackId)
            result = ""
            for t in tracks:
                if t.name is None or len(str(t.name)) == 0:
                    t.updateFromWeb()
                    t.updateInDB()
                result += f'{t.trackId} - {t.name}\n'
            return f'ID: {self.radio_id} Name: {self.name}', result
        else:
            return getLocale("list-not-found", user_id)

    def getEditors(self):
        conn = psycopg2.connect(
            host=config.host,
            database=config.database,
            user=config.user,
            password=config.password,
            port=config.port
        )
        cur = conn.cursor()
        cur.execute("SELECT user_id FROM radioeditors where radio_id = '" + str(self.radio_id) + "'")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        editors = []
        for i in rows:
            editors.append(i[0])
        return editors

    def addEditor(self, user_id):
        rows = self.getEditors()
        if user_id in rows:
            LogCog.logDebug(f'{user_id} already is an editor of radio {self.radio_id}')
            return 0
        else:
            conn = psycopg2.connect(
                host=config.host,
                database=config.database,
                user=config.user,
                password=config.password,
                port=config.port
            )
            cur = conn.cursor()
            cur.execute("INSERT INTO radioeditors(radio_id, user_id) VALUES (%s, %s);", (self.radio_id, user_id))
            conn.commit()
            cur.close()
            conn.close()
            return 1

    def removeEditor(self, user_id):
        conn = psycopg2.connect(
            host=config.host,
            database=config.database,
            user=config.user,
            password=config.password,
            port=config.port
        )
        cur = conn.cursor()
        cur.execute("DELETE FROM radioeditors WHERE radio_id = %s and user_id = %s", (self.radio_id, user_id))
        conn.commit()
        cur.close()
        conn.close()

    def rename(self, newname, user_id):
        if user_id == self.owner:
            conn = psycopg2.connect(
                host=config.host,
                database=config.database,
                user=config.user,
                password=config.password,
                port=config.port
            )
            cur = conn.cursor()
            cur.execute("UPDATE radios SET name = %s where id = %s", (newname, self.radio_id))
            conn.commit()
            cur.close()
            conn.close()

    def delete(self, user_id):
        if user_id == self.owner:
            tracks = self.getTracks(user_id)
            conn = psycopg2.connect(
                host=config.host,
                database=config.database,
                user=config.user,
                password=config.password,
                port=config.port
            )
            cur = conn.cursor()
            for i in tracks:
                cur.execute("DELETE FROM tracks WHERE id='" + str(i[0]) + "'")
            cur.execute("DELETE FROM radios WHERE id='" + str(self.radio_id) + "'")
            conn.commit()
            cur.close()
            conn.close()
            return True
        else:
            return False
