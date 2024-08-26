import psycopg2

import config
from models.Song import Song


def getAllLikedSongs(user_id):
    conn = psycopg2.connect(
        host=config.host,
        database=config.database,
        user=config.user,
        password=config.password,
        port=config.port
    )
    cur = conn.cursor()
    cur.execute("SELECT * FROM liked_songs where user_id = '" + str(user_id) + "'")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    songs = []
    for entry in rows:
        song = Song(entry[3], False)
        song.name = entry[2]
        song.duration = entry[4]
        song.trackId = entry[0]
        songs.append(song)
    return songs


def likeSong(user_id, url):
    song = Song(url, True)
    if song.stream_url is None:
        return False
    conn = psycopg2.connect(
        host=config.host,
        database=config.database,
        user=config.user,
        password=config.password,
        port=config.port
    )
    cur = conn.cursor()
    cur.execute("SELECT * from liked_songs where link = %s and user_id = %s", (song.original_url, user_id))
    check = cur.fetchone()
    if check is not None:
        return False
    cur.execute("INSERT INTO liked_songs(user_id, name, link, duration) VALUES (%s, %s, %s, %s);",
                (user_id, song.name, song.original_url, song.duration))
    conn.commit()
    cur.close()
    conn.close()
    return True


def unlikeSong(user_id, song_id):
    conn = psycopg2.connect(
        host=config.host,
        database=config.database,
        user=config.user,
        password=config.password,
        port=config.port
    )
    cur = conn.cursor()
    cur.execute("DELETE FROM liked_songs WHERE id = %s and user_id = %s", (song_id, user_id))
    conn.commit()
    cur.close()
    conn.close()
    return True
