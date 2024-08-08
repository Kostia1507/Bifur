import psycopg2
from yt_dlp import YoutubeDL, utils

import config
from cogs import LogCog
from models.Radio import Radio


def getRadioById(radio_id):
    conn = psycopg2.connect(
        host=config.host,
        database=config.database,
        user=config.user,
        password=config.password,
        port=config.port
    )
    cur = conn.cursor()
    cur.execute("SELECT * FROM radios where id = '" + str(radio_id) + "'")
    radio = cur.fetchone()
    cur.close()
    conn.close()
    return Radio(radio[0], radio[1], radio[2], radio[3])


def getRadioByName(playlist, owner_id):
    conn = psycopg2.connect(
        host=config.host,
        database=config.database,
        user=config.user,
        password=config.password,
        port=config.port
    )
    cur = conn.cursor()
    cur.execute("SELECT * FROM radios where name = %s and owner = %s", (playlist, owner_id))
    radio = cur.fetchone()
    cur.close()
    conn.close()
    return Radio(radio[0], radio[1], radio[2], radio[3])


def getPlayLists(user_id):
    conn = psycopg2.connect(
        host=config.host,
        database=config.database,
        user=config.user,
        password=config.password,
        port=config.port
    )
    cur = conn.cursor()
    cur.execute("SELECT id,name,shared FROM radios WHERE owner = '" + str(user_id) + "'")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    radios = []
    for entry in rows:
        radios.append(Radio(entry[0], entry[1], user_id, entry[2]))
    return radios


def getSharedPlayLists(user_id):
    conn = psycopg2.connect(
        host=config.host,
        database=config.database,
        user=config.user,
        password=config.password,
        port=config.port
    )
    cur = conn.cursor()
    cur.execute("SELECT id,name FROM radios WHERE owner = '" + str(user_id) + "' and shared = true")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    radios = []
    for entry in rows:
        radios.append(Radio(entry[0], entry[1], user_id, True))
    return radios


def createRadio(name, user_id):
    conn = psycopg2.connect(
        host=config.host,
        database=config.database,
        user=config.user,
        password=config.password,
        port=config.port
    )
    cur = conn.cursor()
    cur.execute("INSERT INTO radios(name, owner) VALUES (%s, %s);", (name, user_id))
    cur.execute("SELECT id FROM radios WHERE name = %s and owner = %s", (name, user_id))
    conn.commit()
    radio_id = cur.fetchall()
    radio_id = radio_id[::-1]
    radio_id = radio_id[0]
    cur.close()
    conn.close()
    return radio_id[0]


def shareRadio(name, user_id):
    if name.isdigit():
        radio = getRadioById(name)
        name = radio.name
    conn = psycopg2.connect(
        host=config.host,
        database=config.database,
        user=config.user,
        password=config.password,
        port=config.port
    )
    cur = conn.cursor()
    cur.execute("SELECT * FROM radios where name = %s and owner = %s", (name, user_id))
    radio = cur.fetchone()
    if radio is None:
        return None
    status = not radio[3]
    cur.execute("UPDATE radios SET shared = %s where name = %s and owner = %s", (status, name, user_id))
    conn.commit()
    cur.close()
    conn.close()
    return status


def getAllSharedRadios():
    conn = psycopg2.connect(
        host=config.host,
        database=config.database,
        user=config.user,
        password=config.password,
        port=config.port
    )
    cur = conn.cursor()
    cur.execute("SELECT * FROM radios where shared = true")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    radios = []
    for entry in rows:
        radios.append(Radio(entry[0], entry[1], entry[2], entry[3]))
    return radios


# pass radio_id as 0 if you need to create one new
def importYouTubePlayList(user_id, link, radio_id):
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
            radio_id = createRadio(info['title'], user_id)
        entries = info['entries']
        conn = psycopg2.connect(
            host=config.host,
            database=config.database,
            user=config.user,
            password=config.password,
            port=config.port
        )
        cur = conn.cursor()
        for entry in entries:
            LogCog.logDebug(str(entry))
            if entry is not None:
                cur.execute("INSERT INTO tracks(name, list, link, duration) VALUES (%s, %s, %s, %s);",
                            (entry["title"], radio_id, entry["webpage_url"], entry['duration']))
        conn.commit()
        cur.close()
        conn.close()
        return radio_id
