helpUA = {
    "Текстові команди": [
        {
            "name": ">ball",
            "aliases": [],
            "description": "скористатись магічним \"Шар 8\""
        },
        {
            "name": ">roll [?start] [?end] [?count]",
            "aliases": [],
            "description": "відправляє випадкове число від start до end. За замовчанням це 0 і 100." +
                           "Якщо потрібно згенерувати декілька чисел, вкажіть count"
        },
        {
            "name": ">randp [згадування]",
            "aliases": [],
            "description": "вибирає випадкового користувача зі списку згаданих",
        },
        {
            "name": ">randw [text]",
            "aliases": [],
            "description": "вибирає випадкове слово зі всього заданого тексту",
        },
        {
            "name": ">randm",
            "aliases": [],
            "description": "вибирає випадкове повідомлення в цьому каналі",
        },
        {
            "name": ">vote",
            "aliases": [],
            "description": "додати реакції на попереднє повідомлення для голосування",
        },
        {
            "name": ">reply [?text]",
            "aliases": [],
            "description": "бот відповість на ваше повідомлення як можна швидше",
        },
        {
            "name": ">weather [city]",
            "aliases": [],
            "description": "прогноз погоди для вашого міста на 3 дні вперед",
        },
        {
            "name": ">weatherd [city]",
            "aliases": [],
            "description": "більш детальний прогноз погоди на 5 днів",
        },
        {
            "name": ">report [text]",
            "aliases": [],
            "description": "повідомити розробнику про помилку",
        },
        {
            "name": ">clean [number]",
            "aliases": [">clear"],
            "description": "видалення повідомлень в цьому каналі",
        },
        {
            "name": ">embed [text]",
            "aliases": [],
            "description": "відправка гарного повідомлення. Повідомлення має виглядати наступним чином: \n" +
                           "Заголовок | текст | колір. Приклад: >embed Привіт | Гарне повідомлення | #345678. Також можна додати картину",
        },
    ],
    "Команди для картин":
        [
            {
                "name": ">imgsearch [text]",
                "aliases": [],
                "description": "Пошук картин на платформі Pexel"
            },
            {
                "name": ">black [url]",
                "aliases": [],
                "description": "переводить картинку в чорно-білий профіль"
            },
            {
                "name": ">red [url], >green [url], >blue [url], >alpha [url]",
                "aliases": [],
                "description": "отримати сепарації RGB"
            },
            {
                "name": ">cyan [url], >magenta [url], >yellow [url], >key [url]",
                "aliases": [],
                "description": "отримати сепарації CMYK"
            },
            {
                "name": ">color, [red] [green] [blue] [url]",
                "aliases": [],
                "description": "додатки колір до картини по сепараціях"
            },
            {
                "name": ">swap [url] [mode]",
                "aliases": [],
                "description": "дозволяє керувати каналами RGBA. Доступні значення: r,g,b,a,e (пусто), f (повно) канали" +
                               "\nНаприклад: rgea - вернути картину без синього; grba - поміняти червоний з зеленим канали"
            },
            {
                "name": ">mix [прозорість] [url] [url]",
                "aliases": [],
                "description": "змішати дві картинки. Прозорість число в межах 0-100"
            },
            {
                "name": ">blur [url] [n]",
                "aliases": [],
                "description": "розмити картинку, n ціле число що вказує силу"
            },
            {
                "name": ">spread [url] [n]",
                "aliases": [],
                "description": "випадково зміщує пікселі зображення на відстань n"
            },
            {
                "name": ">contrast [url] [n]",
                "aliases": [],
                "description": "добавляє контраст"
            },
            {
                "name": ">opacity [url] [n]",
                "aliases": [">no", ">test"],
                "description": "переводить картинку в чорно-білий профіль"
            },
            {
                "name": ">invers [url]",
                "aliases": [],
                "description": "отримати інверсію картини"
            },
            {
                "name": ">frameh [url]",
                "aliases": [],
                "description": "добавити рамки для горизонтальної картини. Використовуйте >framev [url] для вертикальних"
            },
            {
                "name": ">penguin [text]",
                "aliases": [],
                "description": "створює картинку з Ковальским. Використовуйте | щоб поставити абзац"
            },
            {
                "name": ">crop [left] [top] [right] [bottom] [url]",
                "aliases": [],
                "description": "обрізати картину. >crop 50 0 20 0 [url] - обріже 50% зверху зображення та 20 знизу"
            },
            {
                "name": ">size [height] [width] [url]",
                "aliases": [],
                "description": "встановити розмір картини в пікселях"
            },
            {
                "name": ">resize [height] [width] [url]",
                "aliases": [],
                "description": "змінити розмір картини по відношенню до оригіналу. >resize 1 2 [url] розтяне зображення в 2 рази"
            },
            {
                "name": ">sign [url] [text]",
                "aliases": [],
                "description": "добавити текст до картини знизу. Використовуйте >signtop [url] [text] щоб добавити текст зверху"
            },
            {
                "name": ">totext [url]",
                "aliases": [],
                "description": "передає зображення текстовими символами"
            },
        ],
    "Команди музичного плеєра":
        [
            {
                "name": ">play [text]",
                "aliases": [],
                "description": "програти пісню з YouTube. Також, це може бути посилання"
            },
            {
                "name": ">search [text]",
                "aliases": [],
                "description": "шукає 5 пісень і повертає вам список для вибору однієї"
            },
            {
                "name": ">[n]",
                "aliases": [">c [n]"],
                "description": "вибрати n-у пісню після пошуку. Наприклад >2 вибере другу пісню"
            },
            {
                "name": ">join",
                "aliases": [],
                "description": "приєднатися до голосового каналу"
            },
            {
                "name": ">exit",
                "aliases": ["leave"],
                "description": "вийти з голосового каналу"
            },
            {
                "name": ">current",
                "aliases": [],
                "description": "показує інформацію про поточну пісню"
            },
            {
                "name": ">skip [?n]",
                "aliases": [],
                "description": "пропусти n пісень. За замовчанням, пропускає 1 пісню"
            },
            {
                "name": ">pause і >resume",
                "aliases": [],
                "description": "зупинити й продовжити програвати пісні"
            },
            {
                "name": ">list",
                "aliases": ['queue'],
                "description": "список всіх пісень в черзі"
            },
            {
                "name": ">shuffle",
                "aliases": [],
                "description": "перемішати список"
            },
            {
                "name": ">remove [n] [?end]",
                "aliases": [],
                "description": "прибрати пісню з черги. Якщо вказана друга змінна, то буде прибрано всі пісні від n до end"
            },
            {
                "name": ">repeat",
                "aliases": [],
                "description": "включити/виключити повтор списку"
            },
            {
                "name": ">mclean",
                "aliases": [">mclean"],
                "description": "очистити список"
            },
            {
                "name": ">stop",
                "aliases": [],
                "description": "очистити список і зупинити поточну пісню"
            },
            {
                "name": ">reset",
                "aliases": [],
                "description": "видаляє музичний плеєр, використовувати в випадку несправності"
            },
            {
                "name": ">like [url]",
                "aliases": [],
                "description": "добавити пісню в список улюблених"
            },
            {
                "name": ">liked",
                "aliases": ["likedsongs", "likedlist"],
                "description": "список ваших улюблених пісень"
            },
            {
                "name": ">playliked",
                "aliases": ["pliked"],
                "description": "програти всі ваші улюблені пісні"
            },
            {
                "name": ">unlike",
                "aliases": [],
                "description": "прибрати пісню з улюблених"
            },
            {
                "name": ">linfo [id]",
                "aliases": [],
                "description": "інформація про вподобану пісню"
            }
        ],
    "Команди плейлистів":
        [
            {
                "name": ">createradio [name]",
                "aliases": [],
                "description": "створити плейлист з вибраним ім'ям"
            },
            {
                "name": ">radios",
                "aliases": [],
                "description": "показує всі ваші плейлисти"
            },
            {
                "name": ">radio [name or id]",
                "aliases": [],
                "description": "програти вибраний плейлист"
            },
            {
                "name": ">addradio [name or id]",
                "aliases": [],
                "description": "добавити плейлист в чергу, не видаляючи інші пісні"
            },
            {
                "name": ">radiolist [name or id]",
                "aliases": [">rlist", ">rl"],
                "description": "показує всі пісні в вибраному плейлисти"
            },
            {
                "name": ">addtrack [id] [url]",
                "aliases": [">at"],
                "description": "добавити нову пісню до плейлиста. ID - ID плейлиста"
            },
            {
                "name": ">tinfo [id]",
                "aliases": [],
                "description": "інформація про пісню. ID - ID пісні"
            },
            {
                "name": ">rinfo [id]",
                "aliases": [],
                "description": "інформація про плейлист. ID - ID плейлиста"
            },
            {
                "name": ">deltrack [id]",
                "aliases": [],
                "description": "видалити пісню. ID - ID пісні"
            },
            {
                "name": ">delradio [id]",
                "aliases": [],
                "description": "видалити плейлист. ID - ID плейлиста"
            },
            {
                "name": ">rename [id] [name] ",
                "aliases": [],
                "description": "перейменувати плейлист. ID - ID плейлиста"
            },
            {
                "name": ">share [name]",
                "aliases": [],
                "description": "дозволити іншим користувачам прослуховувати ваш плейлист"
            },
            {
                "name": ">allradios",
                "aliases": [],
                "description": "показати всі поширенні плейлисти"
            },
            {
                "name": ">randradio",
                "aliases": ['>rradio', '>randomradio'],
                "description": "запустити випадковий плейлист зі всіх поширених"
            },
            {
                "name": ">randownradio",
                "aliases": ['>roradio', '>randomownradio'],
                "description": "запустити випадковий плейлист зі своїх"
            },
            {
                "name": ">importlist [link]",
                "aliases": ['>importlist', '>implist'],
                "description": "створити новий плейлист на основі плейлиста YouTube"
            },
            {
                "name": ">addlist [id] [link]",
                "aliases": ['>addplaylist'],
                "description": "добавити пісні з плейлиста YouTube у плейлист з вказаним ID"
            },
            {
                "name": ">allowedit [id] [згадування]",
                "aliases": ['>edit'],
                "description": "дозволити згаданим користувачам редагувати ваш плейлист з вказаним ID"
            },
            {
                "name": ">disallowedit [id] [згадування]",
                "aliases": ['>disedit'],
                "description": "заборонити згаданим користувачам редагувати ваш плейлист з вказаним ID"
            },
        ],
    "Ігри":
        [
            {
                "name": ">fourinrow [згадування]",
                "aliases": ['>4inrow', '>connect4'],
                "description": "Гра в якій гравці намагаються зібрати 4 шари в ряд, по вертикалі, горизонталі чи діагоналі\n" +
                               "Шари обов'язково ппадають вниз поля, чи на інший шар, тому для ходу потрібно вибрати тільки стовпець\n" +
                               ">4inrow [гравець] [?висота] [?ширина] - створити нову гру\n" +
                               "Гравець якого запросили, ходить першим\n" +
                               "Завдяки параметрам висоти та ширини можна створити різноманітні дошки"
            },
            {
                "name": ">reversi [згадування]",
                "aliases": ['>othello'],
                "description": "Реверсі граються на дошці 8х8 клітин. Гравці почергово розміщають свої фішки"
                               " (з однієї сторони білі, з другої - чорні) так щоб між уже наявною  своєю фішкою та тою"
                               " що щено поклали на стіл опинився безперервний"
                               " ряд ворожих фішок. Всі ворожі фішки в таких рядах перевертаються.\n"
                               "Якщо не існує ходу який переверне хоча б одну ворожу фішку - хід пропускається."
                               " Якщо обидва гравці не можуть походити - гра закінчується\n"
                               "Виграє той - чиїх фішок на столі більше"
            },
        ],
    "Калькулятор":
        [
            {
                "name": ">calc [вираз]",
                "aliases": [],
                "description": "Вирішує математичний вираз\n" +
                               "Приклад: >calc 5 + 5 * 2 чи >calc 8gcd12\n" +
                               "Якщо писати вираз без зайвого тексту, то бот буде вирішувати його без команди\n" +
                               "Використовуйте наступні позначення:\n" +
                               "+ додавання\n" +
                               "- віднімання\n" +
                               "* множення\n" +
                               "\\ ділення\n" +
                               "% остача від ділення\n" +
                               "^ степінь\n" +
                               "n! - факторіал числа n\n" +
                               "Також доступно декілька функцій\n" +
                               "a gcd b - найбільший спільний дільник чисел\n" +
                               "a lcd b - найменше спільне кратне"
            },
            {
                "name": ">avg [вираз],[вираз]",
                "aliases": [],
                "description": "команда для пошуку середнього значення між довільною кількістю значень\n" +
                               "Приклад: >avg 5, 4+6,10"
            }
        ],
    "Спілкування":
        [
            {
                "name": "Згадуйте бота, на початку повідомлення",
                "aliases": [],
                "description": "Також комадою >chat можна налаштувати бота"
            },
            {
                "name": ">chat clean",
                "aliases": [],
                "description": "очистити вашу історію чату"
            },
            {
                "name": ">chat new [message]",
                "aliases": [],
                "description": "створює новий чат з новим системним повідомленням, що задає модель поведінки"
            },
            {
                "name": ">chat system",
                "aliases": [],
                "description": "дізнатися поточне системне повідомлення"
            },
            {
                "name": ">chat history",
                "aliases": [],
                "description": "вивести всю історію чату"
            },
        ],
    "Налаштування серверу":
        [
            {
                "name": ">setprefix [prefix] ",
                "aliases": [],
                "description": "встановити новий префікс команд для вашого серверу"
            },
            {
                "name": ">ignore [?текстовий канал]",
                "aliases": [],
                "description": "заборонити боту відповідати в згаданому каналі"
            },
            {
                "name": ">autoreaction [реакція]",
                "aliases": [],
                "description": "бот буде реагувати на всі повідомлення в цьому каналі з вибраною реакцією"
            },
            {
                "name": ">removereactions",
                "aliases": [],
                "description": "прибрати всі автоматичні реакції"
            },
            {
                "name": ">setcmd [interval] [cmd] [args]",
                "aliases": [],
                "description": "добавити авто-команду до цього каналу. Встановіть інтервал в годинах, 24 якщо треба "
                               "раз в день"
            },
            {
                "name": ">setcmd [interval] weather [args]",
                "aliases": [],
                "description": "відправляти прогноз погоди раз в день"
            },
            {
                "name": ">setcmd [interval] time",
                "aliases": [],
                "description": "відправляти час"
            },
            {
                "name": ">setcmd [interval] say [args]",
                "aliases": [],
                "description": "відправляти вказане повідомлення"
            },
            {
                "name": ">setcmd [interval] currency [валюта1] [валюта2]",
                "aliases": [],
                "description": "відправляє курс валюти2 відносно валюти1"
            },
            {
                "name": ">getcmds",
                "aliases": [],
                "description": "список всіх команд в цьому каналі"
            },
            {
                "name": ">initcmd [id]",
                "aliases": [],
                "description": "скидує значення лічильника до нуля.\n"
                               "Бот виконає команду коли цей лічильник буде рівним вказаному інтервалу"
            },
            {
                "name": ">delcmd [id]",
                "aliases": [],
                "description": "видалити автоматичну команду за її ID. ID можна глянути в >getcmds"
            },
        ],
    "Налаштування ролей серверу":
        [
            {
                "name": ">autorole [роль]",
                "aliases": [],
                "description": "автоматично видавати всім новим користувачам згадану роль"
            },
            {
                "name": ">giveroletoall [роль]",
                "aliases": [">glall"],
                "description": "видати роль всім користувачам сервера"
            },
            {
                "name": ">giveroletousers [роль]",
                "aliases": [">gluser"],
                "description": "видати роль всім користувачам сервера, окрім ботів"
            },
            {
                "name": ">giveroletobots [роль]",
                "aliases": [">glbot"],
                "description": "видати роль всім ботам серверу"
            }
        ]
}
