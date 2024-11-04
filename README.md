## Bifur is the discord bot, based on discord.py

Invite bot to your guild - https://discord.com/api/oauth2/authorize?client_id=802546295906107423&permissions=1644372164209&scope=bot

My discord: comradekostia

[![Discord](https://discord.com/api/guilds/336642139381301249/embed.png)](https://discord.gg/2EGkGzDTK5 "Discord")

### Current features:
- Music
- Playlists
- Weather Forecast
- Picture Editor (some simple commands like convert to black and white profile)
- Translator
- Connect 4
- Reversi
- TicTacToe (5x5 field)
- ChatGPT Integration
- Calculator
- Currency rates
- Commands with fixed intervals

If you want to create your own command:
1. All views and modals create in discordModels package
2. If you want to output a lot of information, consider to use PagedMessage from pagedMessagesService
3. Use locales and add your own in localeService
4. Consider to write all functions in services

Don't forgive to create your own config.py with keys and tokens

Example:
```python
# KEYS for API
token = "DISCORD_BOT_TOKEN"
weatherKey = 'WEATHER_API'
pexelsKey = 'PEXELS_API'
chatGPTKey = 'OPENAI_KEY'
fixerKey = 'FIXERS_KEY'
GOOGLE_API_KEY = "GOOGLE_API_KEY"
GOOGLE_CX = "GOOGLE_CX"

# DB CONNECTION
host = "host"
database = "dbname"
user = "postgres"
password = "password"
port = "5432"


# SETTINGS
prefix = '>'
owners = [418040057019236353]
# channel for all logs
log_channel = 1146417855450066965
# channel where bot will send messages with RAM usage
status_channel = 1200814696564019231

# OTHER INFO for commands
invite = "https://discord.com/api/oauth2/authorize?client_id=802546295906107423&permissions=1644372164209&scope=bot"

# EMOJIS
cubesEmojis = ["<:cube1:1143593710471360522>", "<:cube2:1143593711951954001>", "<:cube3:1143593714229461154>",
               "<:cube4:1143593715668111462>", "<:cube5:1143593718121762836>", "<:cube6:1143593719094853865>"]

playEmoji = "<:play:1279134976180228219>"
pauseEmoji = "<:pause:1279134985282125905>"
previousEmoji = "<:previous:1279134988159422576>"
skipEmoji = "<:skip:1279134979829268604>"
stopEmoji = "<:stop:1279142161173971056>"
repeatEmoji = "<:repeat:1279134989568573473>"
shuffleEmoji = "<:shuffle:1279134977946292344>"
volumeUpEmoji = "<:volume_up:1279134992705785918>"
volumeDownEmoji = "<:volume_down:1279134972703277116>"
likeEmoji = "<:like:1279134974628597924>"
```
