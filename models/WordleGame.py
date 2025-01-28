import random
from enum import Enum
from io import BytesIO

from PIL import ImageDraw, Image, ImageFont

from service.chatGPTService import history

with open("assets/wordle/valid-words.txt", "r") as file:
    words = [line.rstrip() for line in file]

with open("assets/wordle/possible-words.txt", "r") as file:
    possible_words = [line.rstrip() for line in file]

def draw_rounded_rectangle(draw, xy, radius, fill, outline=None, width=1):
    x1, y1, x2, y2 = xy
    draw.rectangle([x1 + radius, y1, x2 - radius, y2], fill=fill)  # Top/bottom sides
    draw.rectangle([x1, y1 + radius, x2, y2 - radius], fill=fill)  # Left/right sides
    draw.pieslice([x1, y1, x1 + 2 * radius, y1 + 2 * radius], 180, 270, fill=fill)  # Top-left corner
    draw.pieslice([x2 - 2 * radius, y1, x2, y1 + 2 * radius], 270, 360, fill=fill)  # Top-right corner
    draw.pieslice([x1, y2 - 2 * radius, x1 + 2 * radius, y2], 90, 180, fill=fill)  # Bottom-left corner
    draw.pieslice([x2 - 2 * radius, y2 - 2 * radius, x2, y2], 0, 90, fill=fill)  # Bottom-right corner
    if outline:
        draw.arc([x1, y1, x1 + 2 * radius, y1 + 2 * radius], 180, 270, fill=outline, width=width)
        draw.arc([x2 - 2 * radius, y1, x2, y1 + 2 * radius], 270, 360, fill=outline, width=width)
        draw.arc([x1, y2 - 2 * radius, x1 + 2 * radius, y2], 90, 180, fill=outline, width=width)
        draw.arc([x2 - 2 * radius, y2 - 2 * radius, x2, y2], 0, 90, fill=outline, width=width)

def get_centered_text_position(draw, text, font, rect_x1, rect_y1, rect_x2, rect_y2):
    text_width, text_height = draw.textsize(text, font=font)
    x = rect_x1 + (rect_x2 - rect_x1 - text_width) // 2
    y = rect_y1 + (rect_y2 - rect_y1 - text_height) // 2
    return x, y

class ResultColor(Enum):
    GREEN = 0
    YELLOW = 1
    NONE = 2

class LetterStatus:

    def __init__(self, number, status, word):
        self.number = number
        self.status = status
        self.word = word

    def getLetter(self):
        return self.word[self.number]

class WordleGame:

    # Message id used to get unique name for picture file
    def __init__(self, user_id):
        self.user_id = user_id
        self.answer = random.choice(possible_words)
        self.history = []
        self.tries = 0
        self.finished = False
        self.possible_letters = ["q","w","e","r","t","y","u","i","o","p","a","s","d","f","g","h","j","k","l","z","x","c","v","b","n","m"]

    def makeMove(self, prompt: str):
        prompt = prompt.lower().strip()
        if prompt == self.answer:
            self.finished = True
        if prompt in words:
            ret = []
            yellowLoop = []
            counted = ""
            # let`s count green and red
            for i in range(0, 5):
                if prompt[i] == self.answer[i]:
                    ret.append(LetterStatus(i, ResultColor.GREEN, prompt))
                    counted += prompt[i]
                elif prompt[i] not in self.answer:
                    ret.append(LetterStatus(i, ResultColor.NONE, prompt))
                    counted += prompt[i]
                    if prompt[i] in self.possible_letters:
                        self.possible_letters.remove(prompt[i])
                else:
                    yellowLoop.append(i)
            # yellow now
            for i in yellowLoop:
                if self.answer.count(prompt[i]) > counted.count(prompt[i]):
                    ret.append(LetterStatus(i, ResultColor.YELLOW, prompt))
                else:
                    ret.append(LetterStatus(i, ResultColor.NONE, prompt))
                counted += prompt[i]
            ret.sort(key=lambda x: x.number)
            self.tries += 1
            if self.tries >= 6:
                self.finished = True
            self.history.append(ret)
            return ret
        else:
            return None

    def generetaPicture(self):
        FIELD_SIZE = 50
        SQUARE_SIZE = 100
        SQUARE_RADIUS = 20
        # Size calculated like 100x100px per square and 50px - fields
        img = Image.new("RGBA", (SQUARE_SIZE*5+FIELD_SIZE*2, SQUARE_SIZE*6+FIELD_SIZE*2), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        for y in range(0, 6):
            for x in range(0, 5):
                rect_x1 = x * SQUARE_SIZE + FIELD_SIZE
                rect_y1 = y * SQUARE_SIZE + FIELD_SIZE
                rect_x2 = rect_x1 + SQUARE_SIZE
                rect_y2 = rect_y1 + SQUARE_SIZE
                draw_rounded_rectangle(draw, (rect_x1, rect_y1, rect_x2, rect_y2), SQUARE_RADIUS, fill=(20, 20, 20, 255))
        font = ImageFont.truetype("assets/arial.ttf", 40)
        for y in range(0, len(self.history)):
            for x in range(0, 5):
                loopCell = self.history[y][x]
                rect_x1 = x * SQUARE_SIZE + FIELD_SIZE
                rect_y1 = y * SQUARE_SIZE + FIELD_SIZE
                rect_x2 = rect_x1 + SQUARE_SIZE
                rect_y2 = rect_y1 + SQUARE_SIZE
                if loopCell.status == ResultColor.GREEN:
                    draw_rounded_rectangle(draw, (rect_x1, rect_y1, rect_x2, rect_y2), SQUARE_RADIUS,
                                           fill=(110,186,87, 255))
                elif loopCell.status == ResultColor.YELLOW:
                    draw_rounded_rectangle(draw, (rect_x1, rect_y1, rect_x2, rect_y2), SQUARE_RADIUS,
                                           fill=(250,195,70, 255))
                letter = loopCell.getLetter()
                text_x, text_y = get_centered_text_position(draw, letter.upper(), font, rect_x1, rect_y1, rect_x2, rect_y2)
                draw.text((text_x, text_y), letter.upper(), font=font, fill="white")
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        return buffer

    def get_description(self):
        if not self.finished:
            return "Letters:\n"+" ".join(self.possible_letters)
        else:
            if self.tries >= 6 and self.history[-1][0].word != self.answer:
                return f"The word was {self.answer}"
            else:
                return "Congratulations!"