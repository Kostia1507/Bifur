import random
from copy import deepcopy
from enum import Enum
from io import BytesIO

from PIL import ImageDraw, Image, ImageFont


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


class MoveDirection(Enum):
    TOP = 0
    RIGHT = 1
    BOTTOM = 2
    LEFT = 3


def slide_and_merge(line: list):
    new_line = [i for i in line if i != 0]

    merged_line = []
    skip = False
    for i in range(len(new_line)):
        if skip:
            skip = False
            continue

        if i + 1 < len(new_line) and new_line[i] == new_line[i + 1]:
            merged_line.append(new_line[i] * 2)
            skip = True
        else:
            merged_line.append(new_line[i])

    while len(merged_line) < len(line):
        merged_line.append(0)

    return merged_line


class Game2048:

    def __init__(self, user_id):
        self.user_id = user_id
        self.moves = 0
        self.board = [[0 for x in range(4)] for y in range(4)]
        self.add_new_value()

    def get_empty_cells(self):
        empty_cells = [(r, c) for r in range(4) for c in range(4) if self.board[r][c] == 0]
        return empty_cells

    def is_game_over(self):
        for row in self.board:
            if 0 in row:
                return False

        # check rows
        for row in range(4):
            for cell in range(3):
                if self.board[row][cell] == self.board[row][cell + 1]:
                    return False

        # check columns
        for row in range(3):
            for cell in range(4):
                if self.board[row][cell] == self.board[row + 1][cell]:
                    return False

        return True

    def add_new_value(self):
        empty_cells = self.get_empty_cells()
        if len(empty_cells) > 0:
            r, c = random.choice(empty_cells)
            self.board[r][c] = 4 if random.random() < 0.1 else 2
            return True
        return False

    def move(self, direction):
        current_board = deepcopy(self.board)

        if direction == MoveDirection.TOP:
            self.board = [list(row) for row in zip(*self.board)]
            for i in range(len(self.board)):
                self.board[i] = slide_and_merge(self.board[i])
            self.board = [list(row) for row in zip(*self.board)]
        elif direction == MoveDirection.RIGHT:
            for i in range(len(self.board)):
                self.board[i].reverse()
                self.board[i] = slide_and_merge(self.board[i])
                self.board[i].reverse()
        elif direction == MoveDirection.BOTTOM:
            self.board = [list(row) for row in zip(*self.board)]
            for i in range(len(self.board)):
                self.board[i].reverse()
                self.board[i] = slide_and_merge(self.board[i])
                self.board[i].reverse()
            self.board = [list(row) for row in zip(*self.board)]
        elif direction == MoveDirection.LEFT:
            for i in range(len(self.board)):
                self.board[i] = slide_and_merge(self.board[i])

        if self.board != current_board:
            self.moves += 1
            # return is there empty cells
            return self.add_new_value()
        else:
            return False

    def generate_picture(self):
        valueToColorMap = {
            0: (247, 239, 237),
            2: (240, 224, 219),
            4: (232, 208, 202),
            8: (223, 193, 184),
            16: (215, 178, 167),
            32: (206, 163, 151),
            64: (198, 149, 134),
            128: (188, 134, 118),
            256: (179, 120, 102),
            512: (170, 105, 87),
            1024: (165, 98, 79),
            2048: (160, 91, 72),
            4096: (155, 86, 68),
        }
        MARGIN_SIZE = 5
        SQUARE_SIZE = 100
        SQUARE_RADIUS = 20

        # Size calculated like 100x100px per square and 20px - margins
        img = Image.new("RGBA", (SQUARE_SIZE * 4 + MARGIN_SIZE * 5, SQUARE_SIZE * 4 + MARGIN_SIZE * 5), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("assets/arial.ttf", 40)
        # font = ImageFont.load_default()

        for x in range(len(self.board)):
            for y in range(len(self.board)):
                rect_x1 = x * SQUARE_SIZE + MARGIN_SIZE * (x + 1)
                rect_y1 = y * SQUARE_SIZE + MARGIN_SIZE * (y + 1)
                rect_x2 = rect_x1 + SQUARE_SIZE
                rect_y2 = rect_y1 + SQUARE_SIZE
                draw_rounded_rectangle(draw, (rect_x1, rect_y1, rect_x2, rect_y2), SQUARE_RADIUS,
                                       fill=valueToColorMap[self.board[y][x]])

                if self.board[y][x] != 0:
                    text_x, text_y = get_centered_text_position(draw, str(self.board[y][x]), font, rect_x1, rect_y1,
                                                                rect_x2,
                                                                rect_y2)
                    draw.text((text_x, text_y), str(self.board[y][x]), font=font, fill="white")

        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        return buffer
