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
    "Template Commands":
        [
            {
                "name": ">penguin [text]",
                "aliases": [],
                "description": "generate a picture with Kowalski. Use | to start new line"
            },
            {
                "name": ">pat [url]",
                "aliases": [],
                "description": "create GIF file with your picture. You can attach file to message instead of a link."
            },
            {
                "name": ">vibe [url]",
                "aliases": [">viber"],
                "description": "create GIF file with your picture. You can attach file to message instead of a link. >viber will place a cat on a right side"
            },
            {
                "name": ">slap [url]",
                "aliases": [],
                "description": "create GIF file with your picture. You can attach file to message instead of a link."
            },
            {
                "name": ">work [url]",
                "aliases": [],
                "description": "create GIF file with your picture. You can attach file to message instead of a link."
            },
            {
                "name": ">poster [url] [color]",
                "aliases": [],
                "description": "Turns your picture into a poster. The color indicator controls the number of colors in the palette.\n"
                               "Use a larger color value to display more colors.\n"
                               "I recommend starting with indicator 12."
            },
            {
                "name": ">oil [url], >pencil [url], >watercolor [url]",
                "aliases": [],
                "description": "it tries to create the appearance of a painting painted with oil paints, pencils, or watercolors, respectively."
            },
            {
                "name": ">rip [url or mention]",
                "aliases": [],
                "description": "Convert Picture to Black and White mode and add candle to it"
            },
            {
                "name": ">vietnam [url or mention]",
                "aliases": [],
                "description": "Add photo from Vietnam War to your picture as background"
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
            },
            {
                "name": ">like [url]",
                "aliases": [],
                "description": "add song to favourite songs"
            },
            {
                "name": ">liked",
                "aliases": ["likedsongs", "likedlist"],
                "description": "list of your favourite songs"
            },
            {
                "name": ">playliked",
                "aliases": ["pliked"],
                "description": "play your favourite songs"
            },
            {
                "name": ">unlike",
                "aliases": [],
                "description": "remove song from favourites"
            },
            {
                "name": ">linfo [id]",
                "aliases": [],
                "description": "shows info about your favourite song"
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
                "description": "A game in which players try to collect 4 layers in a row, vertically, horizontally or diagonally" +
                               "Layers necessarily fall down the field, or on another layer, so you need to select only column" +
                               ">4inrow [player] [?height] [?width] - create a new game" +
                               "The player who was invited goes first" +
                               "Thanks to the height and width parameters, you can create a variety of boards"
            },
            {
                "name": ">reversi [mention]",
                "aliases": ['>othello'],
                "description": "Reversies are played on a board of 8x8 cells. Players take turns placing their pieces (disks)"
                               " (white on one side, black on the other) so that between your existing disk and that one"
                               "what was put on the table turned out to be continuous"
                               " a row of enemy disks. All enemy disks in such rows are turned over.\n"
                               "If there is no move that will flip at least one enemy disk, the move is skipped."
                               " If both players cannot move - the game ends\n"
                               "The one with more disks on the table wins"
            },
            {
                "name": ">wordle",
                "aliases": [],
                "description": "get 6 chances to guess a 5-letter word\n"
                               "green indicates that the letter is correct and in the correct position\n"
                               "yellow means it is in the answer but not in the right position\n"
            },
        ],
    "Calculator":
        [
            {
                "name": ">calc [expression]",
                "aliases": [],
                "description": "Solves a mathematical expression" +
                               "Example: >calc 5 + 5 * 2 or >calc 8gcd12" +
                               "If you write an expression without extra text, the bot will solve it without a command" +
                               "Use the following notations:" +
                               "+ adding" +
                               "- subtraction" +
                               "* multiplication" +
                               "\\ division" +
                               "% remainder from division" +
                               "^ degree" +
                               "n! - the factorial of the number n" +
                               "A few features are also available" +
                               "a gcd b is the greatest common divisor of numbers" +
                               "a lcd b is the least common multiple"
            },
            {
                "name": ">avg [expression],[expression]",
                "aliases": [],
                "description": "calculate average value. Use comma to seperate expressions." +
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
                "name": ">defprefix",
                "aliases": ['defaultprefix', 'delprefix'],
                "description": "set prefix to default"
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
                "name": ">setcmd [channel]",
                "aliases": [],
                "description": "add auto commands to mentioned channel"
            },
            {
                "name": ">editcmd [channel] [id]",
                "aliases": [],
                "description": "edit command with [id] in mentioned channel. You can found ID witn >getcmds"
            },
            {
                "name": ">getcmds [channel]",
                "aliases": [],
                "description": "list of all commands in mentioned channel"
            },
            {
                "name": ">delcmd [channe] [id]",
                "aliases": [],
                "description": "delete cmd by ID. Look for ID in >getcmds"
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
