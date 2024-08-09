import math
import random
from datetime import datetime

import aiohttp
import aiofiles
import os
from PIL import Image, ImageDraw, ImageFilter, ImageFont

import config


async def download_image(image_url, name_of_file):
    async with aiohttp.ClientSession() as session:
        async with session.get(image_url) as response:
            if response.status == 200:
                f = await aiofiles.open(name_of_file, mode='wb')
                await f.write(await response.read())
                await f.close()


async def totext(image_url, message_id, mode):
    brloop = 'Ñ@#W$861?!abc;:+=-,._ '
    name_of_file = f'temp/{message_id}.jpg'
    await download_image(image_url, name_of_file)
    img = Image.open(name_of_file)

    width, height, mx_sym = img.size[0], img.size[1], 1940
    k = math.sqrt((width * height) / mx_sym)
    width = int((width * 2) / k)
    height = int(height / k)
    while width * height >= mx_sym or width > 96:
        width -= 2
        height -= 1
    small_img = img.resize((width, height), Image.BILINEAR).convert('RGB')

    pixels = small_img.load()
    res = ''
    mx, mn = 0, 255
    for i in range(0, height):
        for g in range(0, width):
            r, g, b = pixels[g, i]
            if mode == 'r':
                bright = (r * 0.3 + g * 0.59 + b * 0.11) / 3
            else:
                bright = 255 - (r * 0.3 + g * 0.59 + b * 0.11) / 3
            mx, mn = max(bright, mx), min(bright, mn)
    price = (mx - mn) / len(brloop)
    for i in range(0, height):
        for g in range(0, width):
            r, g, b = pixels[g, i]
            if mode == 'r':
                bright = (r * 0.3 + g * 0.59 + b * 0.11) / 3
            else:
                bright = 255 - (r * 0.3 + g * 0.59 + b * 0.11) / 3
            br = int((bright - mn) / price)
            if br >= len(brloop):
                br = len(brloop) - 1
            res += brloop[br]
        res += "\n"
    os.remove(name_of_file)
    return "```" + res + "```"


async def black(image_url, message_id):
    name_of_file = f'temp/{message_id}.jpg'
    await download_image(image_url, name_of_file)
    img = Image.open(name_of_file).convert('L')
    img.save(name_of_file)
    return name_of_file


async def set_alpha(alpha, image_url, message_id):
    name_of_file = f'temp/{message_id}.png'
    real_alpha = int(int(alpha) * 255 / 100)
    await download_image(image_url, name_of_file)
    img = Image.open(name_of_file)
    img.putalpha(real_alpha)
    img.save(name_of_file)
    return name_of_file


async def get_channel(image_url, color, message_id):
    name_of_file = f'temp/{message_id}.png'
    await download_image(image_url, name_of_file)
    r, g, b, a = Image.open(name_of_file).convert('RGBA').split()
    empty = r.point(lambda _: 0)
    if color == 'r':
        merge = Image.merge("RGB", (r, empty, empty))
    elif color == 'g':
        merge = Image.merge("RGB", (empty, g, empty))
    elif color == 'b':
        merge = Image.merge("RGB", (empty, empty, b))
    else:
        merge = Image.merge("RGB", (a, a, a))
    os.remove(name_of_file)
    name_of_file = str(random.randint(100000000, 999999999)) + '.jpg'
    merge.save(name_of_file)
    return name_of_file


async def change_channel(image_url, mode, message_id):
    name_of_file = f'temp/{message_id}.png'
    await download_image(image_url, name_of_file)
    r, g, b, a = Image.open(name_of_file).convert('RGBA').split()
    e, f = r.point(lambda _: 0), r.point(lambda _: 255)
    c = [e, e, e, f]
    for i in range(len(mode)):
        if mode[i] == 'r':
            c[i] = r
        elif mode[i] == 'g':
            c[i] = g
        elif mode[i] == 'b':
            c[i] = b
        elif mode[i] == 'a':
            c[i] = a
        elif mode[i] == 'f':
            c[i] = f
    merge = Image.merge("RGBA", (c[0], c[1], c[2], c[3]))
    os.remove(name_of_file)
    name_of_file = str(random.randint(100000000, 999999999)) + '.png'
    merge.save(name_of_file)
    return name_of_file


async def get_CMYKchannel(image_url, color, message_id):
    name_of_file = f'temp/{message_id}.jpg'
    await download_image(image_url, name_of_file)
    c, m, y, k = Image.open(name_of_file).convert('CMYK').split()
    empty = c.point(lambda _: 0)
    if color == 'c':
        merge = Image.merge("CMYK", (c, empty, empty, empty))
    elif color == 'm':
        merge = Image.merge("CMYK", (empty, m, empty, empty))
    elif color == 'y':
        merge = Image.merge("CMYK", (empty, empty, y, empty))
    else:
        merge = Image.merge("CMYK", (empty, empty, empty, k))
    merge.save(name_of_file)
    return name_of_file


async def blur(n, image_url, message_id):
    name_of_file = f'temp/{message_id}.png'
    await download_image(image_url, name_of_file)
    img = Image.open(name_of_file).convert('RGBA').filter(ImageFilter.BoxBlur(n))
    img.save(name_of_file)
    return name_of_file


async def spread(n, image_url, message_id):
    name_of_file = f'temp/{message_id}.png'
    await download_image(image_url, name_of_file)
    img = Image.open(name_of_file).convert('RGBA').effect_spread(n)
    img.save(name_of_file)
    return name_of_file


async def contrast(n, image_url, message_id):
    name_of_file = f'temp/{message_id}.jpg'
    await download_image(image_url, name_of_file)
    img = Image.open(name_of_file).convert('RGB')
    while img.size[0] > 1000 or img.size[1] > 1000:
        img = img.resize((int(img.size[0] / 2), int(img.size[1] / 2)), Image.BILINEAR)
    draw = ImageDraw.Draw(img)
    pix = img.load()
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            r, g, b = pix[x, y]
            draw.point((x, y), (int(r * n), int(g * n), int(b * n)))
    img.save(name_of_file)
    return name_of_file


async def inversion(image_url, message_id):
    name_of_file = f'temp/{message_id}.jpg'
    await download_image(image_url, name_of_file)
    img = Image.open(name_of_file).convert('RGB')
    while img.size[0] > 1000 or img.size[1] > 1000:
        img = img.resize((int(img.size[0] / 2), int(img.size[1] / 2)), Image.BILINEAR)
    draw = ImageDraw.Draw(img)
    pix = img.load()
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            r, g, b = pix[x, y]
            draw.point((x, y), (255 - r, 255 - g, 255 - b))
    img.save(name_of_file)
    return name_of_file


async def crop(left, top, right, bottom, image_url, message_id):
    name_of_file = f'temp/{message_id}.png'
    await download_image(image_url, name_of_file)
    img = Image.open(name_of_file).convert('RGBA')
    left = int(img.size[0] * int(left) / 100)
    top = int(img.size[1] * int(top) / 100)
    right = img.size[0] - int(img.size[0] * int(right) / 100)
    bottom = img.size[1] - int(img.size[1] * int(bottom) / 100)
    img.crop((left, top, right, bottom)).save(name_of_file)
    return name_of_file


async def vietnam(image_url, message_id):
    name_of_file = f'temp/{message_id}.png'
    await download_image(image_url, name_of_file)
    img = Image.open(name_of_file).convert('RGBA')
    vietnamBack = Image.open('assets/background/vietnam.jpg').convert('RGBA')
    vietnamBack = vietnamBack.resize((int(img.size[0]), int(img.size[1])), Image.BILINEAR)
    img = Image.blend(img, vietnamBack, 0.2).convert('RGB')
    img.save(name_of_file)
    return name_of_file


async def hans(image_url, message_id):
    name_of_file = f'temp/{message_id}.png'
    await download_image(image_url, name_of_file)
    img = Image.open(name_of_file).convert('RGBA')
    hansBack = Image.open('assets/background/hans.png').convert('RGBA')
    hansBack = hansBack.resize((int(img.size[0]), int(img.size[1])), Image.BILINEAR)
    img = Image.blend(img, hansBack, 0.2).convert('RGB')
    img.save(name_of_file)
    return name_of_file


async def triggered(image_url, message_id):
    name_of_file = f'temp/{message_id}.png'
    await download_image(image_url, name_of_file)
    img = Image.open(name_of_file).convert('RGB')
    trig = Image.open('assets/background/triggered.jpg').convert('RGB')
    trig = trig.resize((int(img.size[0]), int(trig.size[1])), Image.BILINEAR)
    dst = Image.new('RGB', (trig.width, img.height + trig.height))
    dst.paste(img, (0, 0))
    dst.paste(trig, (0, img.height))
    dst.save(name_of_file)
    return name_of_file


async def trava(image_url, message_id):
    name_of_file = f'temp/{message_id}.png'
    await download_image(image_url, name_of_file)
    img = Image.open(name_of_file).convert('L').convert('RGBA')
    travaImg = Image.open('assets/background/trava.png').convert('RGBA')
    travaImg = travaImg.resize((int(img.size[0]), int(img.size[1])), Image.BILINEAR)
    img = Image.alpha_composite(img, travaImg).convert('RGB')
    img.save(name_of_file)
    return name_of_file


async def frame(image_url, orientation, message_id):
    name_of_file = f'temp/{message_id}.png'
    await download_image(image_url, name_of_file)
    if orientation == 'h':
        img = Image.open(name_of_file).convert('RGBA').resize((845, 590), Image.BILINEAR)
        frameImg = Image.open('assets/background/frame.jpg').convert('RGBA')
        frameImg.paste(img, (99, 100))
    else:
        img = Image.open(name_of_file).convert('RGBA').resize((590, 845), Image.BILINEAR)
        frameImg = Image.open('assets/background/frame.jpg').convert('RGBA').rotate(90, expand=True)
        frameImg.paste(img, (100, 99))
    frameImg.save(name_of_file)
    return name_of_file


async def rip(image_url, message_id):
    name_of_file = f'temp/{message_id}.png'
    await download_image(image_url, name_of_file)
    img = Image.open(name_of_file).convert('L').convert('RGBA')
    ripImg = Image.open('assets/background/rip.png').convert('RGBA')
    ripImg = ripImg.resize((int(img.size[0]), int(img.size[1])), Image.BILINEAR)
    img = Image.alpha_composite(img, ripImg).convert('RGB')
    img.save(name_of_file)
    return name_of_file


async def yae(image_url, message_id):
    name_of_file = f'temp/{message_id}.png'
    await download_image(image_url, name_of_file)
    img = Image.open(name_of_file).convert('RGBA')
    yaeImg = Image.open('assets/background/yae.png').convert('RGBA')
    k = yaeImg.size[1] / img.size[1]
    yaeImg = yaeImg.resize((int(yaeImg.size[0] / k), int(yaeImg.size[1] / k)), Image.BILINEAR)
    img = img.resize((img.size[0], yaeImg.size[1]), Image.BILINEAR)
    yaeRes = Image.new('RGBA', (img.width, img.height), (0, 0, 0, 0))
    yaeRes.paste(yaeImg, (yaeRes.size[0] - yaeImg.size[0], 0))
    img = Image.alpha_composite(img, yaeRes).convert('RGB')
    img.save(name_of_file)
    return name_of_file


async def change_color(image_url, red, green, blue, message_id):
    name_of_file = f'temp/{message_id}.png'
    await download_image(image_url, name_of_file)
    img = Image.open(name_of_file).convert('RGBA')
    r, g, b, a = img.split()
    r = r.point(lambda _: _ + red)
    g = g.point(lambda _: _ + green)
    b = b.point(lambda _: _ + blue)
    img = Image.merge("RGBA", (r, g, b, a))
    img.save(name_of_file)
    return name_of_file


async def mix(image_url1, image_url2, alpha, message_id):
    name_of_file = f'temp/{message_id}.png'
    await download_image(image_url1, name_of_file)
    img1 = Image.open(name_of_file).convert('RGBA')
    await download_image(image_url2, name_of_file)
    img2 = Image.open(name_of_file).convert('RGBA')
    img2 = img2.resize((int(img1.size[0]), int(img1.size[1])), Image.BILINEAR)
    img = Image.blend(img1, img2, alpha / 100).convert('RGBA')
    img.save(name_of_file)
    return name_of_file


async def resize(image_url, height, width, mode, message_id):
    name_of_file = f'temp/{message_id}.png'
    await download_image(image_url, name_of_file)
    img = Image.open(name_of_file).convert('RGBA')
    if mode == "%":
        width, height = int(img.size[0] * width) % 10001, int(img.size[1] * height) % 10001
    img.resize((width, height), Image.BILINEAR).save(name_of_file)
    return name_of_file


async def sign(text, image_url, mode, message_id):
    name_of_file = f'temp/{message_id}.png'
    await download_image(image_url, name_of_file)
    img = Image.open(name_of_file).convert('RGBA')
    draw = ImageDraw.Draw(img)
    size = int(img.size[0] / (len(text) + 2)) * 2
    size = min(size, int(img.size[0] / 4))
    font = ImageFont.truetype("assets/arial.ttf", size)
    if mode == "bottom":
        x = (img.size[0] - font.getsize(text)[0] + 10) / 2
        y = (img.size[1] - font.getsize(text)[1] - 10)
    else:
        x = (img.size[0] - font.getsize(text)[0] + 10) / 2
        y = 5
    draw.text((x - 2, y - 2), text, fill='black', font=font, align="left")
    draw.text((x - 2, y + 2), text, fill='black', font=font, align="left")
    draw.text((x + 2, y - 2), text, fill='black', font=font, align="left")
    draw.text((x + 2, y + 2), text, fill='black', font=font, align="left")
    draw.text((x, y), text, font=font, align="left")
    img.save(name_of_file)

    file_stat = os.stat(name_of_file)
    if file_stat.st_size > 8388608:
        os.remove(name_of_file)
        name_of_file = name_of_file[:-3] + "jpg"
        img.convert('RGB').save(name_of_file)
    return name_of_file


async def card(image_url, message_id):
    name_of_file = f'temp/{message_id}.jpg'
    await download_image(image_url, name_of_file)
    img = Image.open(name_of_file).convert('RGB').resize((600, 300), Image.BILINEAR)
    cardType = random.randint(4, 5)
    number = str(cardType) + str(random.randint(10000000000000, 99999999999999))
    number += str(luhn(number))
    font = ImageFont.truetype("assets/arial.ttf", 50)
    number = number[0:4] + " " + number[4:8] + " " + number[8:12] + " " + number[12:16]
    typeImage = Image.open("assets/background/mastercard.png").resize((100, 60), Image.BILINEAR) if cardType == 5 else \
        Image.open("assets/background/visa.png").resize((100, 60), Image.BILINEAR)
    img.paste(typeImage, (480, 220))
    draw = ImageDraw.Draw(img)
    draw.text((59, 109), number, fill='black', font=font, align="center")
    draw.text((59, 111), number, fill='black', font=font, align="center")
    draw.text((61, 109), number, fill='black', font=font, align="center")
    draw.text((61, 111), number, fill='black', font=font, align="center")
    draw.text((60, 110), number, font=font, align="center")
    date = getDate()
    font = ImageFont.truetype("arial.ttf", 40)
    draw.text((79, 229), date, fill='black', font=font, align="center")
    draw.text((79, 231), date, fill='black', font=font, align="center")
    draw.text((81, 229), date, fill='black', font=font, align="center")
    draw.text((81, 231), date, fill='black', font=font, align="center")
    draw.text((80, 230), date, font=font, align="center")
    img.save(name_of_file)
    return name_of_file


async def searchPhoto(query):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                             'Chrome/68.0.3440.106 Safari/537.36', "Authorization": config.pexelsKey}
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(f'https://api.pexels.com/v1/search?query='
                               f'{query.replace(" ", "+")}&per_page={15}&page={1}') as response:
            if response.status == 200:
                res = await response.json()
                if len(res['photos']) > 0:
                    return random.choice(res['photos'])
                else:
                    return None


def luhn(number):
    number = str(number)
    sum = 0
    for i in range(0, 15):
        if i % 2 == 1:
            sum += int(number[i])
        else:
            add = int(number[i]) * 2
            if add > 9:
                add = add % 10 + 1
            sum += add
    return (sum * 9) % 10


def getDate():
    today = datetime.now()
    return str(today.month) + "/" + str(today.year + 4)[2:4]


def penguin(message_id, text):
    name_of_file = "temp/" + str(message_id) + '.jpg'
    img = Image.open('assets/background/penguin.png').convert('RGB')
    textArr = text.split('|')
    size = 100
    while True:
        font = ImageFont.truetype("assets/arial.ttf", size)
        if size == 20:
            break
        found = True
        for i in textArr:
            if font.getsize(i)[0] >= 430:
                found = False
                size -= 5
                break
        if found:
            break
    startY = 227 - (len(textArr)*size)/2 + size
    for i in range(len(textArr)):
        draw = ImageDraw.Draw(img)
        draw.text((930-font.getsize(textArr[i])[0]/2+10, startY+i*size), textArr[i], fill='black', font=font, align="center")
    img.save(name_of_file)
    return name_of_file