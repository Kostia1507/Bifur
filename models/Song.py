import asyncio
from datetime import datetime

import aiohttp
import psycopg2
from yt_dlp import YoutubeDL, utils

import config
from cogs import LogCog

options = {
    'match_filter': utils.match_filter_func("!is_live"),
    'nocheckcertificate': True,
    'format': 'bestaudio/best',
    'quiet': True,
    'no_warnings': True,
    'noplaylist': True,
    'retries': 5,
    'source_address': '0.0.0.0',
    'prefferedcodec': 'mp3',
    'live_from_start': False,
}


class Song:

    # it's rather better not to use initFromWeb and set it to False
    # Use updateFromWeb method which has validation
    def __init__(self, original_url, initFromWeb):
        self.original_url = original_url
        self.name = ""
        self.updated = datetime.now()
        self.is_live = False
        self.author = None
        self.icon_link = None
        self.duration = None
        self.stream_url = None
        # trackId is presented if song was loaded from radio
        self.trackId = None
        self.radioId = None
        if initFromWeb:
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

    async def updateFromWeb(self, count = 0):
        if count >= 5:
            return
        with YoutubeDL(options) as ydl:
            try:
                info = ydl.extract_info(self.original_url, download=False)
                self.is_live = info['is_live']
                self.name = info['title']
                self.duration = info['duration']
                self.icon_link = info['thumbnail']
                self.stream_url = info['url']
                self.updated = datetime.now()
                await asyncio.sleep(count)
                async with aiohttp.ClientSession() as session:
                    async with session.get(url=self.stream_url) as response:
                        # Try once again
                        if response.status != 200:
                            print("fuck 403")
                            await self.updateFromWeb(count + 1)
            except Exception as e:
                LogCog.logError(f'Помилка при спробі отримати інформацію {self.original_url}: {e}')
                return e

    def download(self, filename):
        if self.is_live:
            return "I will not play a live video"
        optionsDwnl = {
            'format': 'bestaudio/best',
            'keepvideo': False,
            'outtmpl': filename,
            'noplaylist': True,
            'source_address': '0.0.0.0',
            'nocheckcertificate': True
        }
        with YoutubeDL(optionsDwnl) as ydl:
            try:
                ydl.download([self.original_url])
            except Exception as e:
                LogCog.logError(f'Помилка при загрузці {filename}: {e}')
                return e

    def updateInDB(self):
        if self.trackId is not None:
            conn = psycopg2.connect(
                host=config.host,
                database=config.database,
                user=config.user,
                password=config.password,
                port=config.port
            )
            cur = conn.cursor()
            cur.execute("UPDATE tracks SET name = %s, duration = %s WHERE id = %s",
                        (self.name, self.duration, self.trackId))
            conn.commit()
            cur.close()
            conn.close()
