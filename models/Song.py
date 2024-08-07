from yt_dlp import YoutubeDL, utils

from cogs import LogCog


class Song:

    def __init__(self, original_url):
        self.original_url = original_url
        self.name = ""
        self.is_live = False
        self.author = None
        self.icon_link = None
        self.duration = None
        self.stream_url = None
        options = {
            'match_filter': utils.match_filter_func("!is_live"),
            'nocheckcertificate': True,
            'format': 'bestaudio/best',
            'quiet': True,
            'no_warnings': True,
            'source_address': '0.0.0.0',
            'prefferedcodec': 'mp3',
            'live_from_start': False,
            'playlist_items': '1:20'
        }
        with YoutubeDL(options) as ydl:
            try:
                info = ydl.extract_info(self.original_url, download=False)
                self.is_live = info['is_live']
                self.name = info['title']
                self.duration = info['duration']
                self.icon_link = info['thumbnail']
                self.stream_url = info['url']
            except Exception as e:
                LogCog.logError(f'Помилка при спробі отримати інформацію {self.original_url}: {e}')

    # use this method if you need duration in format like 3:41
    def getDurationToStr(self):
        ret = f'{self.duration // 3600}:{self.duration % 3600 // 60}:{self.duration % 60 // 10}{self.duration % 60 % 10}'
        while ret.startswith('0') or ret.startswith(':'):
            ret = ret[1:len(ret)]
        return ret
