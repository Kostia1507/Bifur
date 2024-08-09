helpEN = {
    "Text Commands": [
        {
            "name": ">ball",
            "aliases": [],
            "description": "use magic 8ball"
        },
        {
            "name": ">roll [?start] [?end] [?count]",
            "aliases": [],
            "description": "send random number from start to end. By default, it's 0 and 100." +
                           "count - how many times you need to choose a random number."
                           " Be sure to specify the first two parameters"
        },
        {
            "name": ">randp [mentions]",
            "aliases": [],
            "description": "choose random user from all who was mentioned",
        },
        {
            "name": ">randw [text]",
            "aliases": [],
            "description": "choose random word from given text",
        },
        {
            "name": ">randm",
            "aliases": [],
            "description": "choose random message in this channel",
        },
        {
            "name": ">vote",
            "aliases": [],
            "description": "add reactions on previous message for voting",
        },
        {
            "name": ">reply [?text]",
            "aliases": [],
            "description": "bot will reply you as fast as he can",
        },
        {
            "name": ">weather [city]",
            "aliases": [],
            "description": "get forecast for your city",
        },
        {
            "name": ">weatherd [city]",
            "aliases": [],
            "description": "detailer forecast for 5 days",
        },
        {
            "name": ">report [text]",
            "aliases": [],
            "description": "report some bugs or other problems",
        },
        {
            "name": ">clean [number]",
            "aliases": [">clear"],
            "description": "clean messages in this channel",
        },
        {
            "name": ">embed [text]",
            "aliases": [],
            "description": "sending a custom message. The message should look like this: \n" +
                           "Title | text | color. Example: >embed Hello | Good message | #345678. Also, you can add a picture!",
        },
    ],
    "Picture Commands":
        [
            {
                "name": ">imgsearch [text]",
                "aliases": [],
                "description": "find a picture on Pexel"
            },
            {
                "name": ">black [url]",
                "aliases": [],
                "description": "convert picture to black"
            },
            {
                "name": ">red [url], >green [url], >blue [url], >alpha [url]",
                "aliases": [],
                "description": "get RGBA separations"
            },
            {
                "name": ">cyan [url], >magenta [url], >yellow [url], >key [url]",
                "aliases": [],
                "description": "get CMYK separations"
            },
            {
                "name": ">color, [red] [green] [blue] [url]",
                "aliases": [],
                "description": "add simple color to picture"
            },
            {
                "name": ">swap [url] [mode]",
                "aliases": [],
                "description": "allow to manipulate with separations. You can use: r,g,b,a,e (empty), f (full) channels" +
                               "\nExamples: rgea - get picture without blue channel; grba - swap red and green channels"
            },
            {
                "name": ">mix [transparency] [url] [url]",
                "aliases": [],
                "description": "mix two pictures. Transparency is a number in range 0-100"
            },
            {
                "name": ">blur [url] [n]",
                "aliases": [],
                "description": "blur picture, n is integer, which indicate power"
            },
            {
                "name": ">spread [url] [n]",
                "aliases": [],
                "description": "randomly move pixels"
            },
            {
                "name": ">contrast [url] [n]",
                "aliases": [],
                "description": "add contrast to picture"
            },
            {
                "name": ">opacity [url] [n]",
                "aliases": [">no", ">test"],
                "description": "set opacity from 0 to 100"
            },
            {
                "name": ">invers [url]",
                "aliases": [],
                "description": "inversion of picture"
            },
            {
                "name": ">frameh [url]",
                "aliases": [],
                "description": "add frame to horizontal picture. Use >framev [url] for vertical"
            },
            {
                "name": ">penguin [text]",
                "aliases": [],
                "description": "generate a picture with Kowalski. Use | to start new line"
            },
            {
                "name": ">crop [left] [top] [right] [bottom] [url]",
                "aliases": [],
                "description": "crop the picture. >crop 50 0 20 0 [url] - will crop 50% from top and 20% from bottom"
            },
            {
                "name": ">size [height] [width] [url]",
                "aliases": [],
                "description": "set size of picture in pixels"
            },
            {
                "name": ">resize [height] [width] [url]",
                "aliases": [],
                "description": "resize picture. >resize 1 2 [url] will double the width"
            },
            {
                "name": ">sign [url] [text]",
                "aliases": [],
                "description": "add text to picture at the bottom of picture. Use >signtop [url] [text]" +
                               " if you want to add text at top of picture"
            },
            {
                "name": ">totext [url]",
                "aliases": [],
                "description": "draw picture by characters."
            },
        ],
    "Music Commands":
        [
            {
                "name": ">play [text]",
                "aliases": [],
                "description": "play track from YouTube. Also, you can use link to the YouTube video"
            },
            {
                "name": ">search [text]",
                "aliases": [],
                "description": "search 5 tracks from YouTube and allow you to choose one"
            },
            {
                "name": ">[n]",
                "aliases": [">c [n]"],
                "description": "choose n song after search. >2 will choose second song"
            },
            {
                "name": ">join",
                "aliases": [],
                "description": "join to your voice channel"
            },
            {
                "name": ">exit",
                "aliases": ["leave"],
                "description": "leave from voice channel"
            },
            {
                "name": ">current",
                "aliases": [],
                "description": "shows info about current track"
            },
            {
                "name": ">skip [?n]",
                "aliases": [],
                "description": " skip n songs. By default, skips one song"
            },
            {
                "name": ">pause and >resume",
                "aliases": [],
                "description": "pause and resuming a song"
            },
            {
                "name": ">list",
                "aliases": ['queue'],
                "description": "list of all songs which will be played"
            },
            {
                "name": ">shuffle",
                "aliases": [],
                "description": "shuffle a list"
            },
            {
                "name": ">remove [n] [?end]",
                "aliases": [],
                "description": "remove track from the list. Use end if you want to remove songs in range from n to end"
            },
            {
                "name": ">repeat",
                "aliases": [],
                "description": "start or disable repeating of queue"
            },
            {
                "name": ">mclean",
                "aliases": [">mclean"],
                "description": "clean list"
            },
            {
                "name": ">stop",
                "aliases": [],
                "description": "clean list and stop current song"
            },
            {
                "name": ">reset",
                "aliases": [],
                "description": "deletes the music player, use in case of malfunction"
            }
        ],
    "Playlist Commands":
        [
            {
                "name": ">createradio [name]",
                "aliases": [],
                "description": "create playlist with given name"
            },
            {
                "name": ">radios",
                "aliases": [],
                "description": "shows all your playlists"
            },
            {
                "name": ">radio [name or id]",
                "aliases": [],
                "description": "play selected list"
            },
            {
                "name": ">addradio [name or id]",
                "aliases": [],
                "description": "add list to queue"
            },
            {
                "name": ">radiolist [name or id]",
                "aliases": [">rlist", ">rl"],
                "description": "shows all songs in playlist"
            },
            {
                "name": ">addtrack [id] [url]",
                "aliases": [">at"],
                "description": "add new track to playlist. ID - radio ID"
            },
            {
                "name": ">tinfo [id]",
                "aliases": [],
                "description": "track information. ID - track ID"
            },
            {
                "name": ">rinfo [id]",
                "aliases": [],
                "description": "playlist information. ID - playlist ID"
            },
            {
                "name": ">deltrack [id]",
                "aliases": [],
                "description": "delete track. ID - track ID"
            },
            {
                "name": ">delradio [id]",
                "aliases": [],
                "description": "delete radio. ID - radio ID"
            },
            {
                "name": ">rename [id] [name] ",
                "aliases": [],
                "description": "rename your playlist. ID - radio ID"
            },
            {
                "name": ">share [name]",
                "aliases": [],
                "description": "allows other users listen to your playlists"
            },
            {
                "name": ">allradios",
                "aliases": [],
                "description": "shows all shared playlists"
            },
            {
                "name": ">randradio",
                "aliases": ['>rradio', '>randomradio'],
                "description": "start random playlist from all shared"
            },
            {
                "name": ">randownradio",
                "aliases": ['>roradio', '>randomownradio'],
                "description": "start random own playlist"
            },
            {
                "name": ">importlist [link]",
                "aliases": ['>importlist', '>implist'],
                "description": "create new list with all songs in YouTube playlist"
            },
            {
                "name": ">addlist [id] [link]",
                "aliases": ['>addplaylist'],
                "description": "add songs from YouTube playlist to your list"
            },
            {
                "name": ">allowedit [id] [mentions]",
                "aliases": ['>edit'],
                "description": "allow users to edit your playlist. Use ID of playlist"
            },
            {
                "name": ">disallowedit [id] [mentions]",
                "aliases": ['>disedit'],
                "description": "disallow users to edit your playlist. Use ID of playlist"
            },
        ],
    "Games":
        [
            {
                "name": ">fourinrow [mention]",
                "aliases": ['>4inrow', '>connect4'],
                "description": "A game in which players try to collect 4 layers in a row, vertically, horizontally or diagonally<br>" +
                               "Layers necessarily fall down the field, or on another layer, so you need to select only column<br>" +
                               ">4inrow [player] [?height] [?width] - create a new game<br>" +
                               "The player who was invited goes first<br>" +
                               "Thanks to the height and width parameters, you can create a variety of boards"
            },
            {
                "name": ">puzzle15",
                "aliases": ['>15'],
                "description": "The player receives a 4x4 board randomly filled with numbers from 1 to 15. One cell remains empty<br>" +
                               "During a move, you can switch between an empty cell and any neighboring cell<br>" +
                               "The goal of the game: Put all the numbers in order from 1 to 15, and leave the bottom right corner empty" +
                               "All arrows point in the direction from an empty cell to a neighbor<br>" +
                               "So to swap an empty cell and the number above it, press the up arrow"
            },
            {
                "name": ">quiz",
                "aliases": [],
                "description": "Start a quiz with random images. Try to guess whats illustrated"
            },
            {
                "name": ">mquiz [points] [mention]",
                "aliases": [],
                "description": "Play the quiz together with your friends.<br>" +
                               "Play up to the specified number of points with everyone mentioned in the message<br>" +
                               "For an incorrect answer, the participant receives -2 points and can no longer answer this question<br>"
            }
        ],
    "Calculator":
        [
            {
                "name": ">calc [expression]",
                "aliases": [],
                "description": "Solves a mathematical expression<br>" +
                               "Example: >calc 5 + 5 * 2 or >calc 8gcd12<br>" +
                               "If you write an expression without extra text, the bot will solve it without a command<br>" +
                               "Use the following notations:<br>" +
                               "+ adding<br>" +
                               "- subtraction<br>" +
                               "* multiplication<br>" +
                               "\ division<br>" +
                               "% remainder from division<br>" +
                               "^ degree<br>" +
                               "n! - the factorial of the number n<br>" +
                               "A few features are also available<br>" +
                               "a gcd b is the greatest common divisor of numbers<br>" +
                               "a lcd b is the least common multiple"
            },
            {
                "name": ">avg [expression],[expression]",
                "aliases": [],
                "description": "calculate average value. Use comma to seperate expressions.<br>" +
                               "Example: >avg 5, 4+6,10"
            }
        ],
    "Communication":
        [
            {
                "name": "By mentioning the bot at the beginning of the message, you can chat with it",
                "aliases": [],
                "description": "It works thanks to the integration with ChatGPT"
            },
            {
                "name": ">chat clean",
                "aliases": [],
                "description": "clear your chat history"
            },
            {
                "name": ">chat new [message]",
                "aliases": [],
                "description": "creates a new chat with a new system message that specifies the behavior of model"
            },
            {
                "name": ">chat system",
                "aliases": [],
                "description": " find out the current system message"
            },
            {
                "name": ">chat history",
                "aliases": [],
                "description": "display the entire chat history"
            },
        ],
    "Server settings":
        [
            {
                "name": ">setprefix [prefix] ",
                "aliases": [],
                "description": "set new commands prefix for your guild"
            },
            {
                "name": ">ignore [?text channel]",
                "aliases": [],
                "description": "make bot ignore mentioned channel"
            },
            {
                "name": ">autoreaction [reaction]",
                "aliases": [],
                "description": "this makes bot react on every message at this channel with [emoji]"
            },
            {
                "name": ">removereactions",
                "aliases": [],
                "description": "remove all auto-reactions in this channel"
            },
            {
                "name": ">setcmd [interval] [cmd] [args]",
                "aliases": [],
                "description": "add auto commands to this channel. Set interval in hours, 24 if you need once at day"
            },
            {
                "name": ">setcmd [interval] weather [args]",
                "aliases": [],
                "description": "send weather with interval"
            },
            {
                "name": ">setcmd [interval] time",
                "aliases": [],
                "description": "send time"
            },
            {
                "name": ">setcmd [interval] say [args]",
                "aliases": [],
                "description": "send message"
            },
            {
                "name": ">setcmd [interval] currency [валюта1] [валюта2]",
                "aliases": [],
                "description": "sends the exchange rate of currency2 relative to currency1"
            },
            {
                "name": ">getcmds",
                "aliases": [],
                "description": "list of all commands in this channel"
            },
            {
                "name": ">delcmd [id]",
                "aliases": [],
                "description": "вdelete cmd by ID. Look for ID in >getcmds"
            },
        ],
    "Configuring server roles":
        [
            {
                "name": ">autorole [роль]",
                "aliases": [],
                "description": "automatically issue the mentioned role to all new users"
            },
            {
                "name": ">giveroletoall [роль]",
                "aliases": [">glall"],
                "description": "give role to all server users"
            },
            {
                "name": ">giveroletousers [роль]",
                "aliases": [">gluser"],
                "description": "give role to all server users, except bots"
            },
            {
                "name": ">giveroletobots [роль]",
                "aliases": [">glbot"],
                "description": "give role to all server bots"
            }
        ]
}
