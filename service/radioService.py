import asyncpg
from yt_dlp import YoutubeDL, utils

import config
from cogs import LogCog
from models.Radio import Radio
from models.Song import Song


async def getRadioById(radio_id):
    conn = await asyncpg.connect(
        host=config.host,
        database=config.database,
        user=config.user,
        password=config.password,
        port=config.port
    )
    radio = await conn.fetchrow("SELECT * FROM radios where id = '" + str(radio_id) + "'")
    await conn.close()
    return Radio(radio[0], radio[1], radio[2], radio[3])


async def getRadioByName(playlist, owner_id):
    conn = await asyncpg.connect(
        host=config.host,
        database=config.database,
        user=config.user,
        password=config.password,
        port=config.port
    )
    radio = await conn.fetchrow("SELECT * FROM radios where name = $1 and owner = $2", playlist, owner_id)
    await conn.close()
    return Radio(radio[0], radio[1], radio[2], radio[3])


async def getPlayLists(user_id):
    conn = await asyncpg.connect(
        host=config.host,
        database=config.database,
        user=config.user,
        password=config.password,
        port=config.port
    )
    rows = await conn.fetch("SELECT id,name,shared FROM radios WHERE owner = '" + str(user_id) + "'")
    await conn.close()
    radios = []
    for entry in rows:
        radios.append(Radio(entry[0], entry[1], user_id, entry[2]))
    return radios


async def getSharedPlayLists(user_id):
    conn = await asyncpg.connect(
        host=config.host,
        database=config.database,
        user=config.user,
        password=config.password,
        port=config.port
    )
    rows = await conn.fetch("SELECT id,name FROM radios WHERE owner = '" + str(user_id) + "' and shared = true")
    await conn.close()
    radios = []
    for entry in rows:
        radios.append(Radio(entry[0], entry[1], user_id, True))
    return radios


async def createRadio(name, user_id: int):
    conn = await asyncpg.connect(
        host=config.host,
        database=config.database,
        user=config.user,
        password=config.password,
        port=config.port
    )
    await conn.execute("INSERT INTO radios(name, owner) VALUES ($1, $2);", name, user_id)
    radio_id = await conn.fetch("SELECT id FROM radios WHERE name = $1 and owner = $2", name, user_id)
    radio_id = radio_id[::-1]
    radio_id = radio_id[0]
    await conn.close()
    return radio_id[0]


async def shareRadio(name: str, user_id: int):
    if name.isdigit():
        radio = await getRadioById(name)
        name = radio.name
    conn = await asyncpg.connect(
        host=config.host,
        database=config.database,
        user=config.user,
        password=config.password,
        port=config.port
    )
    radio = await conn.fetchrow("SELECT * FROM radios where name = $1 and owner = $2", name, user_id)
    if radio is None:
        return None
    status = not radio[3]
    await conn.execute("UPDATE radios SET shared = $1 where name = $2 and owner = $3", status, name, user_id)
    await conn.close()
    return status


async def getAllSharedRadios():
    conn = await asyncpg.connect(
        host=config.host,
        database=config.database,
        user=config.user,
        password=config.password,
        port=config.port
    )
    rows = await conn.fetch("SELECT * FROM radios where shared = true")
    await conn.close()
    radios = []
    for entry in rows:
        radios.append(Radio(entry[0], entry[1], entry[2], entry[3]))
    return radios


# pass radio_id as 0 if you need to create one new
async def importYouTubePlayList(user_id, link, radio_id):
    radio_id = int(radio_id)
    settings = {
        'match_filter': utils.match_filter_func("!is_live"),
        'nocheckcertificate': True,
        'format': 'bestaudio/best',
        'quiet': True,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/115.0.0.0 Safari/537.36',
        'no_warnings': True,
        'source_address': '0.0.0.0',
        'prefferedcodec': 'mp3',
        'live_from_start': False,
        'forceurl': True,
        'simulate': True,
        'ignoreerrors': True
    }
    with YoutubeDL(settings) as ydl:
        try:
            info = ydl.extract_info(link, download=False)
        except Exception as e:
            LogCog.logError(f'Exception during import of youtube playlist {e}')
            return e
        if radio_id == 0:
            radio_id = await createRadio(info['title'], user_id)
        entries = info['entries']
        conn = await asyncpg.connect(
            host=config.host,
            database=config.database,
            user=config.user,
            password=config.password,
            port=config.port
        )
        for entry in entries:
            LogCog.logDebug(str(entry))
            if entry is not None:
                await conn.execute("INSERT INTO tracks(name, list, link, duration) VALUES (%s, %s, %s, %s);",
                                  (entry["title"], radio_id, entry["webpage_url"], entry['duration']))
        await conn.close()
        return radio_id


async def createTrack(name, playlist_id: int, link, user_id: int, duration):
    playlist_id = int(playlist_id)
    radio = await getRadioById(playlist_id)
    if user_id == radio.owner or user_id in await radio.getEditors():
        conn = await asyncpg.connect(
            host=config.host,
            database=config.database,
            user=config.user,
            password=config.password,
            port=config.port
        )
        radioId = await conn.fetchrow("SELECT * FROM radios where id = $1", playlist_id)
        if radioId is None:
            return False
        check = await conn.fetchrow("SELECT * from tracks where link = $1 and list = $2", link, radioId[0])
        if check is not None:
            return None
        await conn.execute("INSERT INTO tracks(name, list, link, duration) VALUES ($1, $2, $3, $4);",
                    name, playlist_id, link, duration)
        await conn.close()
        return True


async def forceCreateTrack(name, playlist_id, link, user_id, duration):
    playlist_id = int(playlist_id)
    radio = await getRadioById(playlist_id)
    if user_id == radio.owner or user_id in await radio.getEditors():
        conn = await asyncpg.connect(
            host=config.host,
            database=config.database,
            user=config.user,
            password=config.password,
            port=config.port
        )
        radioId = await conn.fetchrow("SELECT * FROM radios where id = $1", playlist_id)
        if radioId is None:
            return False
        await conn.execute("INSERT INTO tracks(name, list, link, duration) VALUES ($1, $2, $3, $4);",
                           name, playlist_id, link, duration)
        await conn.close()
        return True


async def deleteTrack(track_id, userId):
    track_id = int(track_id)
    conn = await asyncpg.connect(
        host=config.host,
        database=config.database,
        user=config.user,
        password=config.password,
        port=config.port
    )
    track = await conn.fetchrow("SELECT * FROM tracks where id = $1", track_id)
    if track is None:
        return False
    radioId = track[3]
    radioId = await conn.fetchrow("SELECT * FROM radios where id = $1 and owner = $2", radioId, userId)
    if radioId is None:
        return False
    await conn.execute("DELETE FROM tracks WHERE id='" + str(track_id) + "'")
    await conn.close()
    return True


async def getTrackById(track_id):
    track_id = int(track_id)
    conn = await asyncpg.connect(
        host=config.host,
        database=config.database,
        user=config.user,
        password=config.password,
        port=config.port
    )
    track = await conn.fetchrow("SELECT * FROM tracks where id = $1", track_id)
    await conn.close()
    song = Song(track[2], False)
    song.name = track[1]
    song.duration = track[4]
    song.trackId = track[0]
    song.radioId = track[3]
    return song
