import os

from aiohttp import web

from cogs import LogCog

def html_response(text):
    return web.Response(text=text, content_type='text/html')

async def handle_main(request):
    bot = request.app["bifur_bot"]
    ret = f'<h1>Hello! I am Bifur with {len(bot.guilds)} guilds</h1>'
    for guild in bot.guilds:
        ret += f"<h2>{guild.name}</h2>"
    return html_response(ret)

async def start_aiohttp_server(bifur_bot):
    app = web.Application()
    app["bifur_bot"] = bifur_bot
    app.router.add_get('/', handle_main)
    app.router.add_get('/index', handle_main)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.getenv('PORT', 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    LogCog.logSystem(f"WEB-SERVER started on port: {port}")