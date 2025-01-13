import asyncio
from datetime import datetime
from urllib.parse import urlparse, parse_qs

from yt_dlp import YoutubeDL, utils

from cogs import LogCog

filesArr = {}

class DownloadedSong:

    def __init__(self, original_url):
        parsed_url = urlparse(original_url)
        query_params = parse_qs(parsed_url.query)
        video_id = query_params.get('v', [None])[0]

        self.filename = None
        self.download_time = None
        self.original_url = video_id

    async def download(self):
        filename = f'temp/url{self.original_url}.mp3'
        optionsDwnl = {
            'match_filter': utils.match_filter_func("!is_live"),
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
                return filename
            except Exception as e:
                LogCog.logError(f'Помилка при загрузці {filename}: {e}')
                return None

async def get_file_by_url(url):
    if url in filesArr.keys():
        # prevent from deleting this file
        filesArr[url].download_time = datetime.now()
        return filesArr[url]
    else:
        downloadedSong = DownloadedSong(url)
        filename = await asyncio.create_task(downloadedSong.download())
        if filename is not None:
            downloadedSong.filename = filename
            downloadedSong.download_time = datetime.now()
            filesArr[url] = downloadedSong
            return downloadedSong
        else:
            return None
