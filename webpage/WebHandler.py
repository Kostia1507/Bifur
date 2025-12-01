import json
import os
import traceback

from jinja2 import Template

from aiohttp import web

import config
from cogs import LogCog
from service import premiumService, socialCreditsService


def html_response(document, **kwargs):
    with open(document, "r", encoding="utf-8") as file:
        template = Template(file.read())
    # Рендеримо шаблон із переданими змінними
    html_content = template.render(**kwargs)
    return web.Response(text=html_content, content_type='text/html')


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
    return html_response('webpage/index.html', guilds_count=len(bot.guilds))


async def handle_terms(request):
    return html_response('webpage/terms.html')


async def handle_vote(request):
    try:
        body = await request.json()
        user = body["user"]
        LogCog.logSystem(f"User voted for Bifur {user}")
        value = config.social_credits_for_vote * 2 if premiumService.is_premium(
            int(user)) else config.social_credits_for_vote
        await socialCreditsService.updateCounter(user, value)
        return web.Response(status=200, text="Success! Thanks for voting!")
    except json.decoder.JSONDecodeError as error:
        traceback.print_exception(type(error), error, error.__traceback__)
        LogCog.logError(f"Error in parsing VOTE top.gg JSON: {error}")
        return web.Response(status=400, text="JSON Parsing Error")


async def handle_patreon(request):
    action = request.match_info.get('action')
    try:
        body = await request.json()
        discord_id = None
        email = None
        full_name = None
        patreon_id = None
        for attr in body["included"]:
            if "discord_id" in attr["attributes"].keys():
                discord_id = attr["attributes"]["discord_id"]
                email = attr["attributes"]["email"]
                full_name = attr["attributes"]["full_name"]
                patreon_id = attr["id"]
        LogCog.logPatreon(
            f"DS: {discord_id}, Email: {email}, Name: {full_name}, patreon_id: {patreon_id}, action: {action}")
        if action == "create" and discord_id is not None:
            await premiumService.add_premium(discord_id)
        elif action == "delete":
            await premiumService.delete_premium(discord_id)
        return web.Response(status=200, text="Success!")
    except json.decoder.JSONDecodeError as error:
        traceback.print_exception(type(error), error, error.__traceback__)
        LogCog.logError(f"Error in parsing Patreon JSON: {error}")
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
    app.router.add_get('/terms', handle_terms)
    app.router.add_post('/patreon/{action}', handle_patreon)
    app.router.add_post('/voted', handle_vote)
    app.router.add_get('/webpage/{file_path:.*}', handle_static)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.getenv('PORT', 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"WEB-SERVER started on port: {port}")
    LogCog.logSystem(f"WEB-SERVER started on port: {port}")
