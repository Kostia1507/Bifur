import asyncio
import random
import traceback

from yt_dlp import utils, YoutubeDL

from cogs import LogCog
from models.MusicPlayer import MusicPlayer, RepeatType
from models.Song import Song
from service import radioService, likedSongsService

settings = {
    'match_filter': utils.match_filter_func("!is_live"),
    'nocheckcertificate': True,
    'format': 'bestaudio/best',
    'retries: 5'
    'quiet': True,
    'no_warnings': True,
    'source_address': '0.0.0.0',
    'prefferedcodec': 'mp3',
    'live_from_start': False,
    'playlist_items': '1:20',
    'ignoreerrors': True,
}
players = {}


# this function will create new player if it doesn't exist
def getMusicPlayer(guild_id, channel_id):
    if guild_id not in players.keys():
        players[guild_id] = MusicPlayer(guild_id, channel_id)
    return players[guild_id]


# this function can't create new music player, so be careful and check for None
def findMusicPlayerByGuildId(guild_id):
    return players[guild_id] if guild_id in players.keys() else None


async def addTrack(name, guild_id, author, channel_id):
    if str(name).startswith('http'):
        ret = await asyncio.create_task(searchByLink(name))
    else:
        ret = await searchOne(name)
    if ret is not None:
        for song in ret:
            song.author = author
            mp = getMusicPlayer(guild_id, channel_id)
            mp.addSong(song)
        return True
    else:
        return False


def addSong(song, guild_id, author, channel_id):
    song.author = author
    mp = getMusicPlayer(guild_id, channel_id)
    mp.addSong(song)


def startRadio(radioName, guildId, author, channelId, userId, isClearPlaylist):
    if radioName[0].isdigit():
        radio = radioService.getRadioById(radioName)
    else:
        radio = radioService.getRadioByName(radioName, userId)
    if radio is None:
        return False
    tracks = radio.getTracks(userId)
    if tracks is None or len(tracks) == 0:
        return False
    # clear all songs
    if isClearPlaylist and guildId in players.keys():
        players[guildId].songs = []
        players[guildId].playing = None
    mp = getMusicPlayer(guildId, channelId)
    mp.repeating = RepeatType.REPEAT_ALL
    random.shuffle(tracks)
    for song in tracks:
        song.author = author
        mp.addSong(song)
    players[guildId] = mp
    return True


def startLiked(guildId, author, channelId, userId, isClearPlaylist):
    tracks = likedSongsService.getAllLikedSongs(userId)
    if tracks is None or len(tracks) == 0:
        return False
    # clear all songs
    if isClearPlaylist and guildId in players.keys():
        players[guildId].songs = []
        players[guildId].playing = None
    mp = getMusicPlayer(guildId, channelId)
    mp.repeating = RepeatType.REPEAT_ALL
    random.shuffle(tracks)
    for song in tracks:
        song.author = author
        mp.addSong(song)
    players[guildId] = mp
    return True


async def searchByLink(name):
    new_settings = settings.copy()
    new_settings["forceurl"] = True
    new_settings["simulate"] = True
    new_settings["quiet"] = True
    with YoutubeDL(new_settings) as ydl:
        try:
            info = ydl.extract_info(name, download=False)
            if "entries" in info:
                entries = info['entries']
                ret = []
                count = 0
                for entry in entries:
                    count += 1
                    song = Song(entry["webpage_url"], False)
                    if count < 5:
                        await song.updateFromWeb()
                    ret.append(song)
                return ret
            else:
                if info['is_live']:
                    return None
                song = Song(info['webpage_url'], False)
                await asyncio.create_task(song.updateFromWeb())
                return [song]
        except Exception as e:
            LogCog.logError(f'Помилка при пошуку за посиланням {name}: {e}')
            traceback.print_exception(type(e), e, e.__traceback__)


async def searchOne(name):
    with YoutubeDL(settings) as ydl:
        try:
            info = ydl.extract_info("ytsearch:%s" % name, download=False)['entries'][0]
            if info['is_live']:
                return None
            song = Song(info['webpage_url'], False)
            await asyncio.create_task(song.updateFromWeb())
            return [song]
        except Exception as e:
            LogCog.logError(f'Помилка при пошуку {name}: {e}')
            traceback.print_exception(type(e), e, e.__traceback__)


async def searchFive(name):
    with YoutubeDL(settings) as ydl:
        try:
            info = ydl.extract_info(f"ytsearch5:{name}", download=False)['entries'][0:5]
            ret = []
            for e in info:
                if e['is_live']:
                    continue
                t = Song(e['webpage_url'], False)
                await asyncio.create_task(t.updateFromWeb())
                ret.append(t)
            return ret
        except Exception as e:
            LogCog.logError(f'Помилка при пошуку 5 відео {name}: {e}')
            traceback.print_exception(type(e), e, e.__traceback__)


def delete(guild_id):
    if guild_id in players.keys():
        del players[guild_id]


async def downloadVideo(url):
    t = (await searchByLink(url))[0]
    await t.updateFromWeb()
    filename = f'temp/{t.name}.mp3'
    t.download(filename)
    return filename
