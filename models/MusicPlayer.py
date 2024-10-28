import random
from datetime import datetime, timedelta
from enum import Enum

from service.localeService import getLocale, getUserLang, getLocaleByLang

HISTORY_SIZE = 5


class RepeatType(Enum):
    NOT_REPEATING = 0
    REPEAT_ONE = 1
    REPEAT_ALL = 2


class ColorTheme(Enum):
    BLUE = 0
    GRAY = 1
    GREEN = 2
    RED = 3


class MusicPlayer:

    def __init__(self, guild_id, channel_id):
        self.guildId = guild_id
        self.songs = []
        self.history = []
        self.theme = ColorTheme.GRAY
        self.playing = None
        self.volume = 100
        self.repeating = RepeatType.NOT_REPEATING
        self.channelId = channel_id
        # musicPlayers means view-message in discord
        self.musicPlayerAuthorId = None
        self.musicPlayerMessageId = None
        self.musicPlayerChannelId = None
        self.isStopped = False
        self.playCooldown = datetime.now() - timedelta(seconds=10)

    def addSong(self, track):
        self.songs.append(track)

    def getNext(self):
        # if repeating is enabled and only one song in list is playing
        if len(self.songs) == 0:
            if self.repeating != RepeatType.NOT_REPEATING:
                if self.playing is not None:
                    return self.playing
            else:
                return None
        # manage repeating modes
        if self.repeating == RepeatType.REPEAT_ONE and self.playing is not None:
            t = self.playing
        else:
            t = self.songs[0]
            # skip None
            if t is None:
                self.songs.remove(t)
                return None
            if self.repeating != RepeatType.NOT_REPEATING and self.playing is not None:
                self.songs.append(self.playing)
            if self.playing is not None:
                self.history.append(self.playing)
                self.history = self.history[-HISTORY_SIZE:] \
                    if len(self.history) > HISTORY_SIZE else self.history
            self.playing = t
            self.songs.remove(t)
        # looks like one more validation
        if len(self.songs) > 0:
            if self.songs[0] is None:
                self.songs.remove(self.songs[0])
        return t

    # send 1 song from history to the start of query
    def toPrevious(self):
        if len(self.history) == 0:
            if self.playing is not None:
                self.songs = [self.playing] + self.songs
                self.playing = None
            return
        query = [self.history.pop(), self.playing] if self.playing is not None else [self.history.pop()]
        self.songs = query + self.songs
        if self.repeating != RepeatType.NOT_REPEATING:
            if query[0].original_url == self.songs[len(self.songs) - 1].original_url:
                self.songs.pop()
        self.playing = None

    def remove(self, n):
        if str(n).isnumeric():
            if int(n) < len(self.songs):
                t = self.songs[int(n)]
                self.songs.remove(t)
                t.delete()

    def removeLine(self, start, end):
        if str(start).isnumeric() and str(end).isnumeric():
            start, end = int(min(start, end)), int(max(start, end))
            if int(end) < len(self.songs) and start >= 0:
                for i in range(start, end):
                    t = self.songs[i]
                    self.songs.remove(t)
                    t.delete()

    def skip(self, saveIfRepeating=True):
        if self.repeating != RepeatType.NOT_REPEATING and saveIfRepeating:
            self.songs.append(self.playing)
        self.history.append(self.playing)
        self.history = self.history[-HISTORY_SIZE:] \
            if len(self.history) > HISTORY_SIZE else self.history
        self.playing = None

    def skipLine(self, n):
        n = max(min(n - 1, len(self.songs) - 1), 1)
        for i in range(0, n):
            if self.repeating:
                self.songs.append(self.songs[0])
            self.songs.remove(self.songs[0])

    def shuffle(self):
        random.shuffle(self.songs)
        return True

    def formatList(self, user_id):
        userLang = getUserLang(user_id)
        if len(self.songs) == 0 and self.playing is None:
            return getLocaleByLang("list-empty", userLang), ""

        if self.playing is not None:
            title = f'{getLocaleByLang("playing", userLang)} {self.playing.author}: {self.playing.name}'
            if self.playing.duration is not None and self.playing.duration != 0:
                title += f'({self.playing.getDurationToStr()})'
            title += "\n"
        else:
            title = f'{getLocaleByLang("nothing", userLang)}'

        description = ''
        for i in range(0, len(self.songs)):
            if self.songs[i] is not None:
                description += f'{i + 1}.{self.songs[i].author}: {self.songs[i].name}'
                if self.songs[i].duration is not None:
                    description += f'({self.songs[i].getDurationToStr()})'
                description += "\n"
        return title, description

    def formatHistory(self, user_id):
        if len(self.history) == 0 and self.playing is None:
            return getLocale("list-empty", user_id), ""

        description = ''
        for i in range(0, len(self.history)):
            if self.history[i] is not None:
                description += f'{i + 1}.{self.history[i].author}: {self.history[i].name}'
                if self.history[i].duration:
                    description += f'({self.history[i].getDurationToStr()})'
                description += "\n"
        return description
