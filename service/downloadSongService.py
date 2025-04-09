import asyncio
from datetime import datetime
from urllib.parse import urlparse, parse_qs

from yt_dlp import YoutubeDL, utils

from cogs import LogCog

filesArr = {}


def extract_video_id(url: str) -> str:
    parsed_url = urlparse(url)

    # Якщо стандартний формат URL (з параметром 'v')
    if 'youtube.com' in parsed_url.netloc and parsed_url.path == '/watch':
        query_params = parse_qs(parsed_url.query)
        return query_params.get('v', [None])[0]

    # Якщо скорочений формат URL (youtu.be)
    if 'youtu.be' in parsed_url.netloc:
        return parsed_url.path.lstrip('/')

    return None


class DownloadedSong:

    def __init__(self, original_url):
        parsed_url = urlparse(original_url)
        query_params = parse_qs(parsed_url.query)
        video_id = extract_video_id(original_url)

        self.filename = None
        self.download_time = None
        self.original_url = video_id

    async def download(self):
        if self.original_url is None:
            return
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

        def download_file():
            with YoutubeDL(optionsDwnl) as ydl:
                try:
                    ydl.download([self.original_url])
                    return filename
                except Exception as e:
                    LogCog.logError(f'Помилка при загрузці {filename}: {e}')
                    return None

        res = await asyncio.to_thread(download_file)
        return res


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
