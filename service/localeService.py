import psycopg2

import config
from cogs import LogCog

langs = ['en', 'ua', 'ru']


def getLocale(locale, user_id):
    if user_id == 0:
        return locales[locale]['en']
    conn = psycopg2.connect(
        host=config.host,
        database=config.database,
        user=config.user,
        password=config.password,
        port=config.port
    )
    cur = conn.cursor()
    cur.execute("SELECT * FROM language WHERE user_id=%s", (user_id,))
    lang = cur.fetchone()
    lang = 'en' if lang is None else lang[1]
    try:
        return locales[locale][lang]
    except KeyError:  # if locale doesn't exist
        LogCog.logError(f'Can\'t find locale for {locale},lang {lang}, user {user_id}')
        return locales[locale]['en']


def setLang(user_id, lang):
    if lang in langs:
        conn = psycopg2.connect(
            host=config.host,
            database=config.database,
            user=config.user,
            password=config.password,
            port=config.port
        )
        cur = conn.cursor()
        cur.execute("SELECT * FROM language WHERE user_id=%s", (user_id,))
        locale = cur.fetchone()
        if locale is None:
            cur.execute("INSERT INTO language(user_id, language) VALUES (%s, %s);", (user_id, lang))
        else:
            cur.execute("UPDATE language SET language=(%s) WHERE user_id=(%s)", (lang, user_id))
        conn.commit()
        cur.close()
        conn.close()
        return locales['lang-changed'][lang]
    else:
        return "Can't find this language!"


locales = {
    'lang':
        {
            'en': 'en',
            'ua': 'ua',
            'ru': 'ru',
        },
    'lang-changed':
        {
            'en': 'English language is selected!',
            'ua': 'Вибрано українську мову!',
            'ru': 'Выбран русский язык!',
        },
    'result':
        {
            'en': 'Result:',
            'ua': 'Результат:',
            'ru': 'Результат:',
        },
    'owner':
        {
            'en': 'Owner:',
            'ua': 'Власник:',
            'ru': 'Владелец:'
        },
    'count':
        {
            'en': 'Count:',
            'ua': 'Кількість:',
            'ru': 'Количество:'
        },
    'chatGPT-file':
        {
            'en': 'answer is too long, here is your file',
            'ua': 'відповідь надто довга для Discord(у), ось ваш файл',
            'ru': 'ответ слишком длинный для Discord, вот ваш файл'
        },
    'repeat-on':
        {
            'en': 'Repeat enabled',
            'ua': 'Включено повтор списку',
            'ru': 'Включен повтор очереди',
        },
    'repeat-off':
        {
            'en': 'Repeat disabled',
            'ua': 'Виключено повтор списку',
            'ru': 'Выключен повтор очереди',
        },
    'repeat-one':
        {
            'en': 'Enabled repeat of one song',
            'ua': 'Включено повтор одного треку',
            'ru': 'Включено проигривание одной песни',
        },
    'no-playlists':
        {
            'en': 'You don`t have any playlists',
            'ua': 'Ви немаєте готових плейлистів',
            'ru': 'У вас нету плейлистов'
        },
    'playlists-list':
        {
            'en': 'Your playlists:',
            'ua': 'Список ваших плейлистів:',
            'ru': 'Список ваших плейлистов'
        },
    'user-playlists':
        {
            'en': '%p\'s playlists:',
            'ua': 'Доступні плейлисти %p:',
            'ru': 'Доступные плейлисти %p:',
        },
    'shared-list':
        {
            'en': 'All shared playlists:',
            'ua': 'Список поширених плейлистів:',
            'ru': 'Список доступных плейлистов'
        },
    'list-not-found':
        {
            'en': 'List not found',
            'ua': 'Лист не знайдено',
            'ru': 'Список не найдено',
        },
    'user-not-found':
        {
            'en': 'User not found',
            'ua': 'Користувача не знайдено',
            'ru': 'Пользователя не найдено',
        },
    'no-playlist':
        {
            'en': 'Create a radio to get started',
            'ua': 'Створіть радіо для початку',
            'ru': 'Сначала создайте плейлист',
        },
    'new-playlist':
        {
            'en': 'New playlist created. ID:',
            'ua': 'Створено новий плейлист з ID:',
            'ru': 'Создано новый плейлист с ID:',
        },
    'from-list':
        {
            'en': 'from list',
            'ua': 'з плейлиста',
            'ru': 'с плейлиста',
        },
    'playing':
        {
            'en': 'Playing:',
            'ua': 'Зараз граю:',
            'ru': 'Сейчас проигрываю:',
        },
    'duration':
        {
            'en': 'Duration:',
            'ua': 'Тривалість:',
            'ru': 'Продолжительность:',
        },
    'volume':
        {
            'en': 'Volume:',
            'ua': 'Гучність:',
            'ru': 'Громкость:'
        },
    'not-connected-to-voice':
        {
            'en': 'You are not connected to voice channel',
            'ua': 'Ви не приєднанні до голосового каналу',
            'ru': 'Вы не подключены к голосовому каналу',
        },
    'url-exist':
        {
            'en': 'This song has already been found in list. \n'
                  'Use >forceaddtrack [radioId] [url] if you want to add track again.',
            'ua': 'Такий трек вже найдено в листі! \n'
                  'Використайте >forceaddtrack [radioId] [url] якщо бажаєте добавити трек повторно.',
            'ru': 'Такой трек уже существует! \n'
                  'Используйте >forceaddtrack [radioId] [url] если желаете добавить ещё раз.',
        },
    'nothing':
        {
            'en': 'Nothing',
            'ua': 'Нічого',
            'ru': 'Ничего',
        },
    'nothing-found':
        {
            'en': 'Nothing found',
            'ua': 'Нічого не знайдено',
            'ru': 'Ничего не найдено',
        },
    'shared':
        {
            'en': 'Radio shared:',
            'ua': 'Радіо доступне іншим:',
            'ru': 'Радио доступно другим:'
        },
    'ordered':
        {
            'en': 'Ordered by',
            'ua': 'Замовив',
            'ru': 'Заказал',
        },
    'list-empty':
        {
            'en': 'List is empty',
            'ua': 'Лист пустий',
            'ru': 'Лист пустой',
        },
    'first-not-number':
        {
            'en': 'First character can\'t be a number',
            'ua': 'Перший символ не може бути цифрою',
            'ru': 'Первый символ не может быть цифрой'
        },
    'clouds':
        {
            'en': 'Clouds',
            'ua': 'Хмарно',
            'ru': 'Облачно',
        },
    'clear':
        {
            'en': 'Sunny',
            'ua': 'Сонячно',
            'ru': 'Солнечно',
        },
    'snow':
        {
            'en': 'Snow',
            'ua': 'Сніг',
            'ru': 'Снег',
        },
    'rain':
        {
            'en': 'Rain',
            'ua': 'Дощ',
            'ru': 'Дождь',
        },
    'monday':
        {
            'en': 'Monday',
            'ua': 'Понеділок',
            'ru': 'Понедельник',
        },
    'tuesday':
        {
            'en': 'Tuesday',
            'ua': 'Вівторок',
            'ru': 'Вторник',
        },
    'wednesday':
        {
            'en': 'Wednesday',
            'ua': 'Середа',
            'ru': 'Среда',
        },
    'thursday':
        {
            'en': 'Thursday',
            'ua': 'Четвер',
            'ru': 'Четверг',
        },
    'friday':
        {
            'en': 'Friday',
            'ua': "П'ятниця",
            'ru': 'Пятниці',
        },
    'saturday':
        {
            'en': 'Saturday',
            'ua': 'Субота',
            'ru': 'Субота',
        },
    'sunday':
        {
            'en': 'Sunday',
            'ua': 'Неділя',
            'ru': 'Воскресенье',
        },
    'now':
        {
            'en': 'Now:',
            'ua': 'Зараз:',
            'ru': 'Сейчас',
        },
    'weather-in':
        {
            'en': 'Weather in',
            'ua': 'Погода в',
            'ru': 'Погода в',
        },
    'quote':
        {
            'en': 'Quote:',
            'ua': 'Цитата:',
            'ru': 'Цитата:',
        },
    'chose':
        {
            'en': 'I chose',
            'ua': 'Я вибрав',
            'ru': 'Я выбрал',
        },
    'random-number':
        {
            'en': 'Random number from %1 to %2: %3',
            'ua': 'Випадкове число від %1 до %2: %3',
            'ru': 'Случайное число от %1 до %2: %3',
        },
    'animals':
        {
            'en': ['capybara', 'parrot', 'wolf', 'dog', 'cat', 'hamster', 'seal', 'pig',
                   'orca', 'goat', 'tiger', 'lion', 'jaguar animal', 'leopard', 'zebra',
                   'bear', 'walrus', 'penguin',  'donkey', 'pheasant', 'toucan', 'mouse', 'spider',
                   'crab', 'shrimp', 'stingray', 'mantis', 'flamingo', 'horse', 'jellyfish',
                   'jackal', 'hyena', 'orangutan', 'chimpanzee', 'baboon', 'pigeon',
                   'turtle', 'eagle', 'falcon', 'dove', 'sparrow', 'monkey', 'goose', 'swan',
                   'duck', 'chicken', 'deer', 'moose', 'peacock', 'bull', 'buffalo', 'cow', 'dodo',
                   'llama', 'camel', 'crocodile', 'clown fish',
                   'gazelle', 'shark', 'octopus', 'fox', 'rabbit', 'hare', 'snake', 'anaconda',
                   'lizard', 'boar', 'ant', 'cockroach', 'bee', 'wasp',
                   'hornet', 'worm', 'caterpillar', 'humpback whale', 'squirrel',
                   'beaver', 'viper snake', 'scorpion', 'hedgehog'
                   'butterfly', 'python', 'boa', 'locust', 'ladybug',
                   'iguana', 'elephant', 'mosquito', 'tapir',
                   'dolphin', 'panda', 'cougar', 'giraffe', 'owl', 'hawk', 'crow',
                   'antelope', 'stork', 'raccoon', 'lemur', 'sloth',
                   'snail', 'gopher', 'mongoose',  'gecko', 'hummingbird', 'monitor lizard',
                   'sheep', 'starfish', 'meerkat', 'porcupine'],
        },
    'fruits':
        {
            'en': ['banana', 'mango', 'watermelon', 'coconut (fruit)', 'grape', 'lemon',
                   'pomegranate', 'pineapple', 'dragon fruit', 'kiwi', 'avocado', 'canistel',
                   'apple', 'cherry', 'peach', 'strawberry', 'blackberry', 'pumpkin', 'kiwano', 'pepper', 'brocoli',
                   'tomato', 'raspberry', 'cucumber', 'corn', 'carrot', 'garlic', 'cabbage',
                   'artichoke'],
        },
    'landmarks':
        {
            'en': ['Big Ben', 'Eiffel tower', 'London eye', 'Colosseum', 'Tower of Pisa', 'The Great Wall',
                   'Golden Gate bridge', 'Statue of Liberty', 'Sphinx', 'The Taj Mahal', 'Sydney Opera House',
                   'Stonehenge', 'Burj Khalifa', 'Machu Picchu', 'Mount Rushmore', 'Mont Saint-Michel', 'The Acropolis',
                   'The Brandenburg Gate', 'Neuschwanstein Castle', 'Christ the Redeemer', 'Tower Bridge', 'Reichstag',
                   'Berlin cathedral', 'Louvre', 'Empire State Building', 'Saint Sophia Cathedral', 'Palanok Castle',
                   'Buckingham Palace', 'St Paul\'s Cathedral', 'Drottningholm Palace', 'Uspenski Cathedral',
                   'Malbork Castle', 'Karlštejn', 'Powder Tower, Prague', 'Pražský hrad', 'Blue Mosque, Istanbul',
                   'Dolmabahce Palace'],
        },
    'random-animal':
        {
            'en': 'Random animal:',
            'ua': 'Випадкова тварина:',
            'ru': 'Случайное животное:',
        },
    '8ball':
        {
            'en':
                ['It is certain.', 'It is decidedly so.', 'Without a doubt', 'Yes definitely.',
                 'You may rely on it.',
                 'As I see it, yes.', 'Most likely.', 'Outlook good.', 'Yes.', 'Signs point to yes.',
                 'Reply hazy, try again.', 'Ask again later.', 'Better not tell you now.', 'Cannot predict now.',
                 'Concentrate and ask again',
                 'Don\'t count on it.', 'My reply is no.', 'My sources say no.', 'Outlook not so good.',
                 'Very doubtful.'],
            'ua':
                ['Звісно', 'Точно так', 'Можеж бути впевненим в цьому', 'Безперечно', 'Без сумнівів',
                 'Мені здається, так', 'Скоріш за все', 'Знаки говорять - так', 'Так', 'Гарні перспективи',
                 'Спитай ще раз', 'Не можу передбачити', 'Поки не зрозуміло, спитай пізніше',
                 'Краще тобі не говорити',
                 'Сформулюй питання інакше',
                 'Навіть не думай', 'Моя відповідь - ні', 'Дуже сумнівно', 'По моїм даним - ні', 'Однозначно ні'],
        },
    '8ball-answer':
        {
            'en': '8ball response:',
            'ua': 'Відповідь шара:',
            'ru': 'Ответ шара:'
        },
    'large-image':
        {
            'en': 'Too large image, I can\'t handle it',
            'ua': 'Зображення завелике, я не буду з цим працювати',
            'ru': 'Изображение велико, я не буду с этим работать',
        },
    'ignore-on':
        {
            'en': 'I will not reply in this channel',
            'ua': 'Тепер я не буду відповідати в цьому каналі',
            'ru': 'Теперь я не буду отвечать в этом канале',
        },
    'ignore-off':
        {
            'en': 'Now, I can reply in this channel',
            'ua': 'Тепер я знову спілкуюсь в цьому каналі',
            'ru': 'Снова общаюсь в єтом канале'
        },
    'won':
        {
            'en': 'Won',
            'ua': 'Виграв',
            'ru': 'Выиграл'
        },
    'set-prefix':
        {
            'en': 'Set prefix to',
            'ua': 'Встановлено новий префікс',
            'ru': 'Установлен новый префикс'
        },
    'chat-does-not-exist':
        {
            'en': 'Chat doesn`t exist',
            'ua': 'Вашого чату не існує',
            'ru': 'Вашего чата не существует'
        },
    'no-answer':
        {
            'en': 'Couldn\'t get a response. Try clearing your history with >chat clean',
            'ua': 'Не вдалось отримати відповідь. Спробуйте очистити вашу історію з >chat clean',
            'ru': 'Не удалось получить ответ. Спробуйте очистить вашу историю с помощью >chat clean'
        },
    'not-pass-filter':
        {
            'en': "The message did not pass the filter",
            'ua': "Повідомлення не пройшло фільтр",
            'ru': "Сообщение не прошло фильтр"
        },
    'your-history':
        {
            'en': "Your history",
            'ua': "Ваша історія",
            'ru': "Ваша история"
        },
    'wrong':
        {
            'en': "Wrong",
            'ua': "Неправильно",
            'ru': "Неверно"
        },
    'editors':
        {
            'en': "Can edit:",
            'ua': "Мають право добавляти:",
            'ru': "Могут добавлять:"
        },
    'file-not-found':
        {
            'en': "File not found",
            'ua': "Файл не знайдено",
            'ru': "Файл не найден",
        },
    'not-in-voice':
        {
            'en': "You should be in voice channel with me",
            'ua': "Ви не в голосовому каналі зі мною",
            'ru': "Вы не в голосовом канале со мной",
        },
    'ready':
        {
            'en': "Ready!",
            'ua': "Готово!",
            'ru': "Готово!",
        },

}
