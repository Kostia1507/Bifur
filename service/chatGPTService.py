import aiohttp
import config
from cogs import LogCog
from service.localeService import getLocale

systemMessage = {"role": "system", "content": "You are a helpful assistant"}

history = {}


async def ask(message, userId):
    headers = {'Authorization': f'Bearer {config.chatGPTKey}'}
    body = {'model': 'gpt-3.5-turbo'}
    for i in badWords:
        if message.find(i) >= 0:
            return await getLocale("not-pass-filter", userId)
    if userId not in history.keys():
        history[userId] = [systemMessage]
    messages = history[userId]
    messages.append({"role": "user", "content": message})
    body['messages'] = messages

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(url='https://api.openai.com/v1/chat/completions', json=body) as response:
            if response.status == 200:
                body = await response.json()
                answer = body["choices"][0]["message"]
                messages.append(answer)
                history[userId] = messages
                return answer['content']
            else:
                return await getLocale('no-answer', userId)


def clean(userId):
    history[userId] = [systemMessage]


def createChatWithSystemMessage(userId, message):
    newSystemMessage = {"role": "system", 'content': message}
    history[userId] = [newSystemMessage]


async def getSystemMessage(userId):
    if userId not in history.keys():
        return await getLocale('chat-does-not-exist', userId)
    else:
        return history[userId][0]['content']


async def getHistory(userId):
    if userId not in history.keys():
        return [await getLocale('chat-does-not-exist', userId)]
    else:
        return history[userId]


badWords = ['блядь', 'блядиада', 'блядина', 'блядинос', 'блядистость',
            'блядословник', 'блядство', 'выблядок', 'выебон', 'голоёбица',
            'греблядь', 'дерьмохеропиздократ', 'ебало', 'ёбкость',
            'жидоёб', 'козлоёб', 'козлоёбина', 'козлоёбище', 'многопиздная',
            'оверблядь', 'объебательство', 'пидор', 'пизда', 'пиздабол', 'пиздец',
            'пиздоблошка', 'пиздобрат', 'пиздовладелец', 'пиздомания',
            'пиздрик', 'подъёбка', 'поебень', 'скотоёб', 'скотоёбина',
            'сосихуйский', 'страхоёбище', 'трепездон', 'уёбище', 'хуелес',
            'хуеман', 'хуеглот', 'хуйня', 'хуеблядь']


async def generate(message, userId):
    headers = {'Authorization': f'Bearer {config.chatGPTKey}',
               "Content-Type": "application/json"}
    body = {'model': 'dall-e-3',
            'n': 1,
            'size': "1024x1024",
            'prompt': message
            }
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(url='https://api.openai.com/v1/chat/completions', json=body) as response:
            if response.status == 200:
                body = await response.json()
                return body['data'][0]
            else:
                return await getLocale('no-answer', userId)