helpRU = {
    "Текстовые команды": [
        {
            "name": ">ball",
            "aliases": [],
            "description": "использовать волшебный \"шар 8\""
        },
        {
            "name": ">roll [?start] [?end] [?count]",
            "aliases": [],
            "description": "отправит случайное число от start до end. По умолчанию от 0 до 100" +
                           "count - Количество случайных чисел которые вы запросили. Убедитесь в указании первых двух параметров"
        },
        {
            "name": ">randp [mentions]",
            "aliases": [],
            "description": "выбрать случайного пользователя из упомянутых",
        },
        {
            "name": ">randw [text]",
            "aliases": [],
            "description": "выбрать случайное слово из заданного текста",
        },
        {
            "name": ">randm",
            "aliases": [],
            "description": "выбрать случайное сообщения в этом канале",
        },
        {
            "name": ">vote",
            "aliases": [],
            "description": "добавить на предыдущее сообщение реакции для голосования",
        },
        {
            "name": ">reply [?text]",
            "aliases": [],
            "description": "бот ответит настолько быстро насколько он может",
        },
        {
            "name": ">weather [city]",
            "aliases": [],
            "description": "прогноз погоды в вашем городе",
        },
        {
            "name": ">weatherd [city]",
            "aliases": [],
            "description": "более подробный прогноз погоды на 5 дней",
        },
        {
            "name": ">report [text]",
            "aliases": [],
            "description": "доложить о неполадках или проблемах",
        },
        {
            "name": ">clean [number]",
            "aliases": [">clear"],
            "description": "почистить сообщения в этом канале",
        },
        {
            "name": ">embed [text]",
            "aliases": [],
            "description": "отправить красивое встроенное сообщение. Текст должен быть написан следующим образом \n" +
                           "Заголовок | текст | цвет. Пример: >embed Привет | Приятное сообщение | #345678. Можна добавлять и картинки!",
        },
    ],
    "Редактирования картинок":
        [
            {
                "name": ">imgsearch [text]",
                "aliases": [],
                "description": "поиск изображения на платформе Pexel"
            },
            {
                "name": ">black [url]",
                "aliases": [],
                "description": "конвертирует картинку в чёрно-белый профиль"
            },
            {
                "name": ">red [url], >green [url], >blue [url], >alpha [url]",
                "aliases": [],
                "description": "получить каналы RGBA изображения"
            },
            {
                "name": ">cyan [url], >magenta [url], >yellow [url], >key [url]",
                "aliases": [],
                "description": "получить каналы CMYK изображения"
            },
            {
                "name": ">color, [red] [green] [blue] [url]",
                "aliases": [],
                "description": "добавить цвета к всему изображению"
            },
            {
                "name": ">swap [url] [mode]",
                "aliases": [],
                "description": " разрешает управлять каналами. Можна использовать: r,g,b,a,e (пустой), f (полный) каналы" +
                               "\nПример: rgea - получить картинку без синего канала; grba - поменять местами красный и зелёный канал"
            },
            {
                "name": ">mix [прозрачность] [url] [url]",
                "aliases": [],
                "description": "смешать два изображения. Прозрачность это число в пределах 0-100"
            },
            {
                "name": ">blur [url] [n]",
                "aliases": [],
                "description": "размывает картинку, n целое число, что указывает как сильно нужно размыть изображение"
            },
            {
                "name": ">spread [url] [n]",
                "aliases": [],
                "description": "случайно сдвигает пиксели"
            },
            {
                "name": ">contrast [url] [n]",
                "aliases": [],
                "description": "добавить контрасту картинке"
            },
            {
                "name": ">opacity [url] [n]",
                "aliases": [">no", ">test"],
                "description": "установить прозрачность от 0 до 100"
            },
            {
                "name": ">invers [url]",
                "aliases": [],
                "description": "инверсия изображения"
            },
            {
                "name": ">frameh [url]",
                "aliases": [],
                "description": "добавить рамки к горизонтальному изображению. Используйте >framev [url] для вертикальных"
            },
            {
                "name": ">crop [left] [top] [right] [bottom] [url]",
                "aliases": [],
                "description": "обрезать изображение. >crop 50 0 20 0 [url] - срежет 50% сверху и 20% снизу"
            },
            {
                "name": ">size [height] [width] [url]",
                "aliases": [],
                "description": "установить размер картинки в пикселях"
            },
            {
                "name": ">resize [height] [width] [url]",
                "aliases": [],
                "description": "сменить размер картинки. >resize 1 2 [url] растянет картинку в два раза"
            },
            {
                "name": ">sign [url] [text]",
                "aliases": [],
                "description": "добавить текст на изображении снизу полотна. >signtop [url] [text] сделает тоже самое," +
                               " но сверху картинки"
            },
            {
                "name": ">totext [url]",
                "aliases": [],
                "description": "нарисовать картину текстовыми символами"
            },
        ],
    "Команды шаблонов":
        [
            {
                "name": ">penguin [text]",
                "aliases": [],
                "description": "создаёт картинку с Ковальским. Используйте | что бы перейти к следующему ряду"
            },
            {
                "name": ">pat [url]",
                "aliases": [],
                "description": "создаёт GIF файл с вашей картиной. Можна добавлять картину к сообщению вместо URL"
            },
            {
                "name": ">vibe [url]",
                "aliases": [">viber"],
                "description": "создаёт GIF файл с вашей картиной. Можна добавлять картину к сообщению вместо URL. >viber разместит кота с правой стороны"
            },
            {
                "name": ">slap [url]",
                "aliases": [],
                "description": "создаёт GIF файл с вашей картиной. Можна добавлять картину к сообщению вместо URL"
            },
            {
                "name": ">work [url]",
                "aliases": [],
                "description": "создаёт GIF файл с вашей картиной. Можна добавлять картину к сообщению вместо URL"
            },
            {
                "name": ">poster [url] [color]",
                "aliases": [],
                "description": "превращает картину в постер. Переменная color указивает количество цветов в палитре.\n"
                               "Используйте большее значение для того что бы сделать картинку красочнее.\n"
                               "Советую начинать с 12."
            },
            {
                "name": ">oil [url], >pencil [url], >watercolor [url]",
                "aliases": [],
                "description": "пытается изобразить картину мол бы она нарисована художником"
            },
            {
                "name": ">rip [url или упоминание]",
                "aliases": [],
                "description": "Конвертирует картинку в чёрно-белый профиль и добавляет свечку"
            },
            {
                "name": ">vietnam [url или упоминание]",
                "aliases": [],
                "description": "Додает фото с Вьетнама на фон картинки"
            },
        ],
    "Музыкальные команды":
        [
            {
                "name": ">play [text]",
                "aliases": [],
                "description": "воспроизводит трек взятый из YouTube. Вы всегда можете использовать ссылку на видео"
            },
            {
                "name": ">search [text]",
                "aliases": [],
                "description": "находит 5 треков из YouTube и дает тебе выбрать один из них"
            },
            {
                "name": ">[n]",
                "aliases": [">c [n]"],
                "description": "используется после команды >search, используйте цифру, которая стоит рядом с" +
                               " понравившемся треком, чтобы выбрать её"
            },
            {
                "name": ">join",
                "aliases": [],
                "description": "бот присоединится к вашему каналу"
            },
            {
                "name": ">exit",
                "aliases": ["leave"],
                "description": "бот выйдет из вашего канала"
            },
            {
                "name": ">current",
                "aliases": [],
                "description": "показывает информацию о текущем треке"
            },
            {
                "name": ">skip [?n]",
                "aliases": [],
                "description": "пропускает трек в очереди, можно пропустить несколько треков если добавить цифру"
            },
            {
                "name": ">pause and >resume",
                "aliases": [],
                "description": "поставить трек на паузу или продолжить его"
            },
            {
                "name": ">list",
                "aliases": ['queue'],
                "description": "показывает лист с текущими треками"
            },
            {
                "name": ">shuffle",
                "aliases": [],
                "description": "меняет порядок воспроизведения треков"
            },
            {
                "name": ">remove [n] [?end]",
                "aliases": [],
                "description": "убрать трек из очереди. Можно пропустить несколько сразу, если ввести второе значение"
            },
            {
                "name": ">repeat",
                "aliases": [],
                "description": "запускает или отменяет повтор трека"
            },
            {
                "name": ">mclean",
                "aliases": [">mclean"],
                "description": "очищает очередь"
            },
            {
                "name": ">stop",
                "aliases": [],
                "description": "очищает очередь и останавливает текущий трек"
            },
            {
                "name": ">reset",
                "aliases": [],
                "description": "удалить плеер в случае поломки"
            },
            {
                "name": ">like [url]",
                "aliases": [],
                "description": "добавить песню в избранное"
            },
            {
                "name": ">liked",
                "aliases": ["likedsongs", "likedlist"],
                "description": "список избранных песен"
            },
            {
                "name": ">playliked",
                "aliases": ["pliked"],
                "description": "воспроизвести избранные песни"
            },
            {
                "name": ">unlike",
                "aliases": [],
                "description": "убрать песню из избранных"
            },
            {
                "name": ">linfo [id]",
                "aliases": [],
                "description": "информация об избранной песне"
            }
        ],
    "Команды плейлистов":
        [
            {
                "name": ">createradio [name]",
                "aliases": [],
                "description": "создает плейлист с заданным вами названием"
            },
            {
                "name": ">radios",
                "aliases": [],
                "description": "показывает созданные вами плейлисты"
            },
            {
                "name": ">radio [name or id]",
                "aliases": [],
                "description": "воспроизводит выбранный плейлист"
            },
            {
                "name": ">addradio [name or id]",
                "aliases": [],
                "description": "добавить плейлист в очередь"
            },
            {
                "name": ">radiolist [name or id]",
                "aliases": [">rlist", ">rl"],
                "description": "показывает все треки в плейлисте"
            },
            {
                "name": ">addtrack [id] [url]",
                "aliases": [">at"],
                "description": " добавить трек в плейлист. Используйте ID плейлиста"
            },
            {
                "name": ">tinfo [id]",
                "aliases": [],
                "description": "показывает информацию о треке. Используйте ID трека"
            },
            {
                "name": ">rinfo [id]",
                "aliases": [],
                "description": "показывает информацию о плейлисте. Используйте ID листа"
            },
            {
                "name": ">deltrack [id]",
                "aliases": [],
                "description": ">удаляет трек из плейлиста. Используйте ID трека"
            },
            {
                "name": ">delradio [id]",
                "aliases": [],
                "description": "удалить плейлист. Используйте ID плейлиста"
            },
            {
                "name": ">rename [id] [name] ",
                "aliases": [],
                "description": "переименовывает плейлист. Используйте ID плейлиста"
            },
            {
                "name": ">share [name]",
                "aliases": [],
                "description": "разрешает другим пользователям прослушивать ваши плейлисты"
            },
            {
                "name": ">allradios",
                "aliases": [],
                "description": "показывает все доступные вам плейлисты"
            },
            {
                "name": ">randradio",
                "aliases": ['>rradio', '>randomradio'],
                "description": "проиграть случайный плейлист со всех разрешенных"
            },
            {
                "name": ">randownradio",
                "aliases": ['>roradio', '>randomownradio'],
                "description": "проиграть случайный ваш плейлист"
            },
            {
                "name": ">importlist [link]",
                "aliases": ['>importlist', '>implist'],
                "description": "импорт плейлиста на основе плейлиста YouTube"
            },
            {
                "name": ">addlist [id] [link]",
                "aliases": ['>addplaylist'],
                "description": "импорт плейлиста на основе плейлиста YouTube в уже существующий плейлист"
            },
            {
                "name": ">allowedit [id] [mentions]",
                "aliases": ['>edit'],
                "description": "Разрешить пользователю редактировать ваш плейлист"
            },
            {
                "name": ">disallowedit [id] [mentions]",
                "aliases": ['>disedit'],
                "description": "Удалить пользователя с редакторов плейлиста"
            },
        ],
    "Игры":
        [
            {
                "name": ">fourinrow [mention]",
                "aliases": ['>4inrow', '>connect4'],
                "description": "Игра, в которой игроки пытаются собрать 4 шара подряд по вертикали, горизонтали или диагонали\n" +
                               "Шары обязательно падают вниз по полю или на другой шар, поэтому вам нужно только выбрать столбец для хода\n" +
                               ">4inrow [player] [?height] [?width] - создать новую игру\n" +
                               "Приглашенный игрок ходит первым\n" +
                               "Благодаря параметрам высоты и ширины вы можете создавать различные доски"
            },
            {
                "name": ">reversi [упоминание]",
                "aliases": ['>othello'],
                "description": "Реверси играют на доске 8х8 клеток. Игроки поочередно размещают свои фишки"
                                " (с одной стороны белые, с другой - черные) так чтобы между уже имеющейся своей фишкой и той"
                                " что только что положили на стол оказался непрерывный"
                                " ряд вражеских фишек. Все вражеские фишки в таких рядах переворачиваются.\n"
                                "Если не существует хода который перевернет хотя бы одну вражескую фишку – ход пропускается."
                                "Если оба игрока не могут походить - игра заканчивается\n"
                                "Выигрывает тот - чьих фишек на столе больше"
            },
            {
                "name": ">wordle [язык]",
                "aliases": [],
                "description": "Wordle - игра в которой нужно угадать слово с 5 букв за 6 попыток.\n"
                               "Зеленым цветом отмечены буквы что верно угаданы.\n"
                               "Желтый означает что буква есть в ответе, но находиться в другой позиции.\n"
                               "Что бы играть на русском, введите >wordle ru\n"
            },
        ],
    "Калькулятор":
        [
            {
                "name": ">calc [expression]",
                "aliases": [],
                "description": "Solves a mathematical expression\n" +
                               "Example: >calc 5 + 5 * 2 or >calc 8gcd12\n" +
                               "If you write an expression without extra text, the bot will solve it without a command\n" +
                               "Используйте следующие обозначения:\n" +
                               "+ сложение\n" +
                               "- вычитание\n" +
                               "* умножение\n" +
                               "\\ деление\n" +
                               "% остаток от деления\n" +
                               "^ степень\n" +
                               "n! - факториал числа n\n" +
                               "Також доступно несколько функций\n" +
                               "a gcd b это наибольший общий делитель чисел\n" +
                               "a lcd b является наименьшим общим кратным"
            },
            {
                "name": ">avg [example],[example]",
                "aliases": [],
                "description": "команда для поиска среднего значения из неограниченного количества примеров\n" +
                               "Пример: >avg 5, 4+6,10"
            }
        ],
    "Общение":
        [
            {
                "name": "Упомянув бота в начале сообщения, вы сможете с ним пообщаться",
                "aliases": [],
                "description": "Вы также можете использовать команду >chat для настроек"
            },
            {
                "name": ">chat clean",
                "aliases": [],
                "description": "Очищает вашу историю сообщений"
            },
            {
                "name": ">chat new [message]",
                "aliases": [],
                "description": "Создает новый чат с новым системным сообщением, определяющим поведение модели"
            },
            {
                "name": ">chat system",
                "aliases": [],
                "description": "Выводит системное сообщение\nСистемное сообщение сообщает боту, как себя вести"
            },
            {
                "name": ">chat history",
                "aliases": [],
                "description": "Возвращает всю историю чата"
            },
        ],
    "Настройки сервера":
        [
            {
                "name": ">setprefix [prefix] ",
                "aliases": [],
                "description": "установить новый префикс команд на вашем сервере"
            },
            {
                "name": ">defprefix",
                "aliases": ['defaultprefix', 'delprefix'],
                "description": "установить стандартный префикс"
            },
            {
                "name": ">ignore [?text channel]",
                "aliases": [],
                "description": "бот больше не будет отвечать в указанном канале"
            },
            {
                "name": ">autoreaction [reaction]",
                "aliases": [],
                "description": "бот будет отвечать на каждое сообщение с реакцией - [emoji]"
            },
            {
                "name": ">removereactions",
                "aliases": [],
                "description": "удалить все автоматические реакции в этом канале"
            },
            {
                "name": ">setcmd [канал]",
                "aliases": [],
                "description": "создать новую команду в указанном канале"
            },
            {
                "name": ">editcmd [channel] [id]",
                "aliases": [],
                "description": "редактируйте команду с [id] в указанном канале. ID можна найти с помощью >getcmds"
            },
            {
                "name": ">getcmds [channel]",
                "aliases": [],
                "description": "список всех команд в указанном канале"
            },
            {
                "name": ">delcmd [channe] [id]",
                "aliases": [],
                "description": "удаляет команду с укзаанным ID. Ищите ID с >getcmds"
            },
        ],
    "Настройка ролей сервера":
        [
            {
                "name": ">autorole [роль]",
                "aliases": [],
                "description": "автоматически выдаёт упомянутую роль всем новым пользователем этого сервера"
            },
            {
                "name": ">giveroletoall [роль]",
                "aliases": [">glall"],
                "description": "выдаёт роль всем участникам сервера"
            },
            {
                "name": ">giveroletousers [роль]",
                "aliases": [">gluser"],
                "description": "выдаёт роль всем пользователям, но не ботам"
            },
            {
                "name": ">giveroletobots [роль]",
                "aliases": [">glbot"],
                "description": "выдаёт роль всем ботам сервера"
            }
        ]
}
