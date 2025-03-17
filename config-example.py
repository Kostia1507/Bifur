# KEYS for API
token = "Discord bot token"
weatherKey = 'key from WeatherAPI'
pexelsKey = 'API key from Pexels'
chatGPTKey = 'API key from openai'
fixerKey = 'API key from fixer'
GOOGLE_API_KEY = "API key from Google"
GOOGLE_CX = "Maybe don't used"

# DB CONNECTION
host = "db-host"
database = "bifurdb"
user = "admin"
password = "password"
port = "15432"


# SETTINGS
prefix = '>'
owners = [418040057019236353]
# channel for all logs
log_channel = 1146417855450066965
# channel where bot will send messages with RAM usage
status_channel = 1200814696564019231
release = True

# OPTIMIZATION SETTINGS
delete_songs_after_hours = 1
social_credits_for_vote = 1

if not release:
    prefix = "="
    token = "your can erase this part of code but keep release=True"
    log_channel = 1222457916867743795

# OTHER INFO for commands
invite = "https://discord.com/api/oauth2/authorize?client_id=802546295906107423&permissions=1644372164209&scope=bot"
patreon = "https://www.patreon.com/Bifur"
topgg = "https://top.gg/bot/802546295906107423"

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

previousPageEmoji = "<:previous_page:1325153589961949195>"
nextPageEmoji = "<:next_page:1325153617090707518>"
saveEmoji = "<:save:1325153661755850835>"
