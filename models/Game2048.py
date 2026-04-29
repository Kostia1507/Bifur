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
            return True

    def generate_picture(self):
        FIELD_SIZE = 20
        SQUARE_SIZE = 100
        SQUARE_RADIUS = 20

        # Size calculated like 100x100px per square and 50px - fields
        img = Image.new("RGBA", (SQUARE_SIZE * 4 + FIELD_SIZE * 5, SQUARE_SIZE * 4 + FIELD_SIZE * 5), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)