import random
from enum import Enum

from service.localeService import getLocale

HISTORY_SIZE = 3


class RepeatType(Enum):
    NOT_REPEATING = 0
    REPEAT_ONE = 1
    REPEAT_ALL = 2


class MusicPlayer:

    def __init__(self, guild_id, channel_id):
        self.guildId = guild_id
        self.songs = []
        self.history = []
        self.playing = None
        # 0 don't repeat, 1 - repeat one, 2 - repeat all
        self.repeating = RepeatType.NOT_REPEATING
        self.channelId = channel_id
        # musicPlayers means view-message in discord
        self.musicPlayerAuthorId = None
        self.musicPlayerMessageId = None
        self.musicPlayerChannelId = None

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
                self.history = self.history[len(self.history)-3:]
            self.playing = t
            self.songs.remove(t)
        # looks like one more validation
        if len(self.songs) > 0:
            if self.songs[0] is None:
                self.songs.remove(self.songs[0])
        return t

    def getPrevious(self):
        pass

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

    def skip(self):
        if self.repeating:
            self.songs.append(self.playing)
        self.history.append(self.playing)
        self.history = self.history[len(self.history) - 3:]
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
        if len(self.songs) == 0 and self.playing is None:
            return getLocale("list-empty", user_id), ""

        if self.playing is not None:
            title = f'{getLocale("playing", user_id)} {self.playing.author}: {self.playing.name}'
            if self.playing.duration is not None and self.playing.duration != 0:
                title += f'({self.playing.getDurationToStr()})'
            title += "\n"
        else:
            title = f'{getLocale("nothing", user_id)}'

        description = ''
        for i in range(0, len(self.songs)):
            if self.songs[i] is not None:
                description += f'{i + 1}.{self.songs[i].author}: {self.songs[i].name}'
                if self.songs[i].duration is not None and self.playing.duration != 0:
                    description += f'({self.songs[i].getDurationToStr()})'
                description += "\n"
        return title, description
