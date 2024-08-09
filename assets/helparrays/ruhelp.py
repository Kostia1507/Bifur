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
                "name": ">penguin [text]",
                "aliases": [],
                "description": "создаёт картинку с Ковальским. Используйте | что бы перейти к следующему ряду"
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
                "name": ">puzzle15",
                "aliases": ['>15'],
                "description": "Игрок получает доску 4х4 случайно заполненную цифрами от 1 до 15. Одна ячейка остается пустой\n" +
                               "Таким образом за ход можно поменять местами пустую ячейку и любую соседнюю\n" +
                               "Цель игры: Поставить все цифры в порядке от 1 до 15, и в правом нижнем углу оставить пустую\n" +
                               "Все стрелки указывают направление от пустой клетки к соседу\n" +
                               "Поэтому для изменения пустой клетки и цифры над ней нажмите стрелку вверх\n"
            },
            {
                "name": ">quiz",
                "aliases": [],
                "description": "Start a quiz with random images. Try to guess whats illustrated"
            },
            {
                "name": ">mquiz [points] [mention]",
                "aliases": [],
                "description": "Play the quiz together with your friends.\n" +
                               "Play up to the specified number of points with everyone mentioned in the message\n" +
                               "For an incorrect answer, the participant receives -2 points and can no longer answer this question"
            }
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
                "name": ">setcmd [interval] [cmd] [args]",
                "aliases": [],
                "description": "добавляет автоматические команды в данном канале. Интервал указывается в часах"
            },
            {
                "name": ">setcmd [interval] weather [args]",
                "aliases": [],
                "description": "отправляет прогноз погоды с указанным интервалом"
            },
            {
                "name": ">setcmd [interval] time",
                "aliases": [],
                "description": "отправляет текущее время"
            },
            {
                "name": ">setcmd [interval] say [args]",
                "aliases": [],
                "description": "отправляет сообщение с указанным текстом"
            },
            {
                "name": ">setcmd [interval] currency [валюта1] [валюта2]",
                "aliases": [],
                "description": "отправляет курс валюта2 относительно валюта1"
            },
            {
                "name": ">getcmds",
                "aliases": [],
                "description": "список всех команд в этом канале"
            },
            {
                "name": ">delcmd [id]",
                "aliases": [],
                "description": "удалить команду за её ID. Узнать ID можна с помощью >getcmds"
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
