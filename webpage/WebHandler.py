import json
import os
from multiprocessing.resource_tracker import register

from aiohttp import web

from cogs import LogCog

def html_response(document):
    s = open(document, "r")
    return web.Response(text=s.read(), content_type='text/html')

def file_response(file_path):
    """
    Повертає статичний файл (CSS, PNG, JPG тощо).
    """
    if not os.path.exists(file_path):
        return web.Response(status=404, text="File not found")

    # Визначаємо MIME-тип на основі розширення файлу
    mime_types = {
        ".css": "text/css",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
    }
    ext = os.path.splitext(file_path)[1]
    content_type = mime_types.get(ext, "application/octet-stream")

    with open(file_path, "rb") as f:
        return web.Response(body=f.read(), content_type=content_type)

async def handle_main(request):
    bot = request.app["bifur_bot"]
    ret = f'<h1>Hello! I am Bifur with {len(bot.guilds)} guilds</h1>'
    for guild in bot.guilds:
        ret += f"<h2>{guild.name}</h2>"
    return html_response('webpage/index.html')

async def handle_patreon(request):
    try:
        body = await request.json()
        LogCog.logDebug(str(body))
        return web.Response(status=200, text="Success!")
    except json.decoder.JSONDecodeError:
        return web.Response(status=400, text="JSON Parsing Error")

async def handle_static(request):
    """
    Обробник для статичних файлів.
    URL-адреса визначає шлях до файлу.
    """
    file_path = request.match_info.get("file_path", "")
    full_path = os.path.join("webpage", file_path)
    return file_response(full_path)

async def start_aiohttp_server(bifur_bot):
    app = web.Application()
    app["bifur_bot"] = bifur_bot
    app.router.add_get('/', handle_main)
    app.router.add_get('/index', handle_main)
    app.router.add_post('/patreon', handle_patreon)
    app.router.add_get('/webpage/{file_path:.*}', handle_static)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.getenv('PORT', 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    LogCog.logSystem(f"WEB-SERVER started on port: {port}")