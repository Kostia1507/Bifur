import asyncpg

import config
from models.Song import Song


async def getAllLikedSongs(user_id):
    conn = await asyncpg.connect(
        host=config.host,
        database=config.database,
        user=config.user,
        password=config.password,
        port=config.port
    )
    rows = await conn.fetch("SELECT * FROM liked_songs where user_id = '" + str(user_id) + "'")
    await conn.close()
    songs = []
    for entry in rows:
        song = Song(entry[3], False)
        song.name = entry[2]
        song.duration = entry[4]
        song.trackId = entry[0]
        songs.append(song)
    return songs


async def getLikedSongById(user_id, song_id):
    conn = await asyncpg.connect(
        host=config.host,
        database=config.database,
        user=config.user,
        password=config.password,
        port=config.port
    )
    row = await conn.fetchrow("SELECT * FROM liked_songs where user_id = $1 and id = $2", user_id, song_id)
    await conn.close()
    if row is None:
        return None
    song = Song(row[3], False)
    song.name = row[2]
    song.duration = row[4]
    song.trackId = row[0]
    return song


async def likeSong(user_id, url):
    song = Song(url, False)
    await song.updateFromWeb()
    if song.stream_url is None:
        return False
    conn = await asyncpg.connect(
        host=config.host,
        database=config.database,
        user=config.user,
        password=config.password,
        port=config.port
    )
    check = await conn.fetch("SELECT * from liked_songs where link = %s and user_id = %s", (song.original_url, user_id))
    if check is not None and len(check) > 0:
        return False
    await conn.execute("INSERT INTO liked_songs(user_id, name, link, duration) VALUES ($1, $2, $3, $4);",
                       user_id, song.name, song.original_url, song.duration)
    await conn.close()
    return True


async def unlikeSong(user_id, song_id):
    conn = await asyncpg.connect(
        host=config.host,
        database=config.database,
        user=config.user,
        password=config.password,
        port=config.port
    )
    await conn.execute("DELETE FROM liked_songs WHERE id = $1 and user_id = $2", song_id, user_id)
    await conn.close()
    return True
