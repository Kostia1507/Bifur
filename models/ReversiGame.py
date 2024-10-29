import copy
import random
from datetime import datetime
from enum import Enum

from PIL import ImageDraw, Image
from io import BytesIO

columnLetters = "abcdefgh"
BOARD_SIZE = 8

WHITE_MARK_COLOR = "#CCCCCC"
BLACK_MARK_COLOR = "#000000"

POINTS_FOR_CORNER = 10


class CellsValue(Enum):
    EMPTY = 0
    WHITE = 1
    BLACK = 2


# This method converts cords like "e4" to numbers
def convert_str_to_cords(loop: str):
    loop = loop.lower()
    first, last = loop[0], loop[1]
    if first.isnumeric():
        first, last = last, first
    return 8 - int(last), columnLetters.find(first)


def convert_cords_to_str(row, col):
    return f"{columnLetters[col]}{8 - row}"


# return True if there is no moves for all players
def is_terminal(board):
    possible = get_possible_moves(board, 0)
    if len(possible) > 0:
        return False
    possible = get_possible_moves(board, 1)
    if len(possible) > 0:
        return False
    return True


def eval_position(board, color):
    white, black = count_marks(board)
    res = white - black if color == CellsValue.WHITE.value else black - white
    res += 64
    if board[0][0] == color:
        res += POINTS_FOR_CORNER
    elif board[0][0] != CellsValue.EMPTY.value:
        res -= POINTS_FOR_CORNER
    if board[0][BOARD_SIZE - 1] == color:
        res += POINTS_FOR_CORNER
    elif board[0][BOARD_SIZE - 1] != CellsValue.EMPTY.value:
        res -= POINTS_FOR_CORNER
    if board[BOARD_SIZE - 1][0] == color:
        res += POINTS_FOR_CORNER
    elif board[BOARD_SIZE - 1][0] != CellsValue.EMPTY.value:
        res -= POINTS_FOR_CORNER
    if board[BOARD_SIZE - 1][BOARD_SIZE - 1] == color:
        res += POINTS_FOR_CORNER
    elif board[BOARD_SIZE - 1][BOARD_SIZE - 1] != CellsValue.EMPTY.value:
        res -= POINTS_FOR_CORNER
    return res


# returns two numbers. First is count of White. Second - Black
def count_marks(board):
    black = 0
    white = 0
    for row in board:
        for cell in row:
            if cell == CellsValue.WHITE.value:
                white += 1
            elif cell == CellsValue.BLACK.value:
                black += 1
    return white, black


def get_possible_moves(board, turn):
    value = CellsValue.BLACK.value if turn % 2 == 0 else CellsValue.WHITE.value
    enemy = CellsValue.WHITE.value if turn % 2 == 0 else CellsValue.BLACK.value
    ret = []
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            # skip if not empty
            if board[row][col] == CellsValue.EMPTY.value:
                found = False
                enemies = 0
                # left top
                for change in range(1, 9):
                    if row - change < 0 or col - change < 0:
                        break
                    if board[row - change][col - change] == CellsValue.EMPTY.value:
                        break
                    elif board[row - change][col - change] == enemy:
                        enemies += 1
                        continue
                    elif enemies > 0:
                        ret.append((row, col))
                        found = True
                        break
                    else:
                        break
                enemies = 0
                if found:
                    continue
                # left
                for change in range(1, 9):
                    if col - change < 0:
                        break
                    if board[row][col - change] == CellsValue.EMPTY.value:
                        break
                    elif board[row][col - change] == enemy:
                        enemies += 1
                        continue
                    elif enemies > 0:
                        ret.append((row, col))
                        found = True
                        break
                    else:
                        break
                enemies = 0
                if found:
                    continue
                # left bottom
                for change in range(1, 9):
                    if col - change < 0 or row + change >= BOARD_SIZE:
                        break
                    if board[row + change][col - change] == CellsValue.EMPTY.value:
                        break
                    elif board[row + change][col - change] == enemy:
                        enemies += 1
                        continue
                    elif enemies > 0:
                        ret.append((row, col))
                        found = True
                        break
                    else:
                        break
                enemies = 0
                if found:
                    continue
                # bottom
                for change in range(1, 9):
                    if row + change >= BOARD_SIZE:
                        break
                    if board[row + change][col] == CellsValue.EMPTY.value:
                        break
                    elif board[row + change][col] == enemy:
                        enemies += 1
                        continue
                    elif enemies > 0:
                        ret.append((row, col))
                        found = True
                        break
                    else:
                        break
                enemies = 0
                if found:
                    continue
                # bottom-right
                for change in range(1, 9):
                    if row + change >= BOARD_SIZE or col + change >= BOARD_SIZE:
                        break
                    if board[row + change][col + change] == CellsValue.EMPTY.value:
                        break
                    elif board[row + change][col + change] == enemy:
                        enemies += 1
                        continue
                    elif enemies > 0:
                        ret.append((row, col))
                        found = True
                        break
                    else:
                        break
                enemies = 0
                if found:
                    continue
                # right
                for change in range(1, 9):
                    if col + change >= BOARD_SIZE:
                        break
                    if board[row][col + change] == CellsValue.EMPTY.value:
                        break
                    elif board[row][col + change] == enemy:
                        enemies += 1
                        continue
                    elif enemies > 0:
                        ret.append((row, col))
                        found = True
                        break
                    else:
                        break
                enemies = 0
                if found:
                    continue
                # top-right
                for change in range(1, 9):
                    if row - change < 0 or col + change >= BOARD_SIZE:
                        break
                    if board[row - change][col + change] == CellsValue.EMPTY.value:
                        break
                    elif board[row - change][col + change] == enemy:
                        enemies += 1
                        continue
                    elif enemies > 0:
                        ret.append((row, col))
                        found = True
                        break
                    else:
                        break
                enemies = 0
                if found:
                    continue
                # top
                for change in range(1, 9):
                    if row - change < 0:
                        break
                    if board[row - change][col] == CellsValue.EMPTY.value:
                        break
                    elif board[row - change][col] == enemy:
                        enemies += 1
                        continue
                    elif enemies > 0:
                        ret.append((row, col))
                        found = True
                        break
                    else:
                        break
                if found:
                    continue
    return ret


class ReversiGame:

    def __init__(self, players, players_nicknames):
        self.board = [[CellsValue.EMPTY.value for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.board[3][4] = CellsValue.BLACK.value
        self.board[4][3] = CellsValue.BLACK.value
        self.board[3][3] = CellsValue.WHITE.value
        self.board[4][4] = CellsValue.WHITE.value
        self.turn = 0  # if turn is even - black turn, else white
        self.players = players
        self.playersNicknames = players_nicknames
        self.messageId = None
        self.channelId = None
        self.lastMove = None
        self.ai_game = False
        self.bot_id = False

    def make_move(self, row, col, player_id):
        if player_id == self.players[self.turn % 2]:
            value = CellsValue.BLACK.value if self.turn % 2 == 0 else CellsValue.WHITE.value
            enemy = CellsValue.WHITE.value if self.turn % 2 == 0 else CellsValue.BLACK.value
            cellsToChange = []
            enemies = []

            # left top
            for change in range(1, 9):
                if row - change < 0 or col - change < 0:
                    enemies = []
                    break
                if self.board[row - change][col - change] == CellsValue.EMPTY.value:
                    enemies = []
                    break
                elif self.board[row - change][col - change] == enemy:
                    enemies.append((row - change, col - change))
                    continue
                else:
                    break
            for element in enemies:
                cellsToChange.append(element)
            enemies = []
            # left
            for change in range(1, 9):
                if col - change < 0:
                    enemies = []
                    break
                if self.board[row][col - change] == CellsValue.EMPTY.value:
                    enemies = []
                    break
                elif self.board[row][col - change] == enemy:
                    enemies.append((row, col - change))
                    continue
                else:
                    break
            for element in enemies:
                cellsToChange.append(element)
            enemies = []
            # left bottom
            for change in range(1, 9):
                if col - change < 0 or row + change >= BOARD_SIZE:
                    enemies = []
                    break
                if self.board[row + change][col - change] == CellsValue.EMPTY.value:
                    enemies = []
                    break
                elif self.board[row + change][col - change] == enemy:
                    enemies.append((row + change, col - change))
                    continue
                else:
                    break
            for element in enemies:
                cellsToChange.append(element)
            enemies = []
            # bottom
            for change in range(1, 9):
                if row + change >= BOARD_SIZE:
                    enemies = []
                    break
                if self.board[row + change][col] == CellsValue.EMPTY.value:
                    enemies = []
                    break
                elif self.board[row + change][col] == enemy:
                    enemies.append((row + change, col))
                    continue
                else:
                    break
            for element in enemies:
                cellsToChange.append(element)
            enemies = []
            # bottom-right
            for change in range(1, 9):
                if row + change >= BOARD_SIZE or col + change >= BOARD_SIZE:
                    enemies = []
                    break
                if self.board[row + change][col + change] == CellsValue.EMPTY.value:
                    enemies = []
                    break
                elif self.board[row + change][col + change] == enemy:
                    enemies.append((row + change, col + change))
                    continue
                else:
                    break
            for element in enemies:
                cellsToChange.append(element)
            enemies = []
            # right
            for change in range(1, 9):
                if col + change >= BOARD_SIZE:
                    enemies = []
                    break
                if self.board[row][col + change] == CellsValue.EMPTY.value:
                    enemies = []
                    break
                elif self.board[row][col + change] == enemy:
                    enemies.append((row, col + change))
                    continue
                else:
                    break
            for element in enemies:
                cellsToChange.append(element)
            enemies = []
            # top-right
            for change in range(1, 9):
                if row - change < 0 or col + change >= BOARD_SIZE:
                    enemies = []
                    break
                if self.board[row - change][col + change] == CellsValue.EMPTY.value:
                    enemies = []
                    break
                elif self.board[row - change][col + change] == enemy:
                    enemies.append((row - change, col + change))
                    continue
                else:
                    break
            for element in enemies:
                cellsToChange.append(element)
            enemies = []
            # top
            for change in range(1, 9):
                if row - change < 0:
                    enemies = []
                    break
                if self.board[row - change][col] == CellsValue.EMPTY.value:
                    enemies = []
                    break
                elif self.board[row - change][col] == enemy:
                    enemies.append((row - change, col))
                    continue
                else:
                    break
            for element in enemies:
                cellsToChange.append(element)
            enemies = []
            # checks finished
            if len(cellsToChange) == 0:
                return False
            else:
                self.lastMove = f"⚫{convert_cords_to_str(row, col)}" if self.turn % 2 == 0 else \
                    f"⚪{convert_cords_to_str(row, col)}"
                for cords in cellsToChange:
                    self.board[cords[0]][cords[1]] = value
                self.board[row][col] = value
                self.turn += 1
                return True
        else:
            return False

    def generate_picture(self):
        board_img = Image.open("assets/chessboard.jpg").convert("RGB")
        draw = ImageDraw.Draw(board_img)
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.board[row][col] != CellsValue.EMPTY.value:
                    color = BLACK_MARK_COLOR if self.board[row][col] == CellsValue.BLACK.value else WHITE_MARK_COLOR
                    draw.ellipse(((55 + col * 100, 55 + row * 100), (145 + col * 100, 145 + row * 100)), fill=color)

        buffer = BytesIO()
        board_img.save(buffer, format="JPEG")
        buffer.seek(0)
        return buffer

    def get_text(self):
        white, black = count_marks(self.board)
        turn = f"Turn {self.turn}: ⚫\n" if self.turn % 2 == 0 else f"Turn {self.turn}: ⚪\n"
        if self.lastMove is not None:
            turn += "Previous: " + self.lastMove
        return f"{black}⚫ {self.playersNicknames[0]} -  {white}⚪ {self.playersNicknames[1]}\n\n{turn}"

    def handle_move(self, x, y, user_id):
        ret = self.make_move(x, y, user_id)
        if ret:
            possible = get_possible_moves(self.board, self.turn)
            # Player can't move. Next move
            if len(possible) == 0:
                self.turn += 1
                possible = get_possible_moves(self.board, self.turn)
                if len(possible) == 0:
                    # this is the end
                    return False
            # if game is AI, let's play
            elif self.ai_game and self.players[self.turn % 2] == self.bot_id:
                playing = True
                while playing:
                    # first moves bot will make for random
                    if self.turn < 4:
                        possible = get_possible_moves(self.board, self.turn)
                        x, y = random.choice(possible)
                        self.make_move(x, y, self.bot_id)
                    else:
                        val, best_cord = self.alpha_beta(copy.deepcopy(self.board), 6,
                                                         alpha=float('-inf'), beta=float('inf'), maximizing_player=True,
                                                         ai_color=(self.turn + 1) % 2 + 1, turn=self.turn)
                        if best_cord is not None:
                            self.make_move(best_cord[0], best_cord[1], self.players[self.turn % 2])
                        else:
                            possible = get_possible_moves(self.board, self.turn)
                            x, y = random.choice(possible)
                            self.make_move(x, y, self.players[self.turn % 2])
                    possible = get_possible_moves(self.board, self.turn)
                    if len(possible) == 0:
                        self.turn += 1
                        possible = get_possible_moves(self.board, self.turn)
                        if len(possible) == 0:
                            # this is the end
                            return False
                    else:
                        playing = False
        return True

    def get_child(self, board: list, player_ball: int, cord):
        child = copy.deepcopy(board)
        child[cord[0]][cord[1]] = player_ball
        return child

    def alpha_beta(self, board, depth, alpha, beta, maximizing_player, ai_color, turn):
        if depth == 0 or is_terminal(board):
            return eval_position(board, ai_color), -1

        if maximizing_player:
            max_eval = float('-inf')
            max_cord = None
            possible_moves = get_possible_moves(board, turn)
            if len(possible_moves) == 0:
                return self.alpha_beta(board, depth - 1, alpha, beta, False, ai_color, turn + 1)
            for cord in possible_moves:
                value = CellsValue.WHITE.value if ai_color == CellsValue.WHITE.value else CellsValue.BLACK.value
                child = self.get_child(board, value, cord)  # Отримуємо всі можливі ходи
                eval, _ = self.alpha_beta(child, depth - 1, alpha, beta, False, ai_color, turn + 1)
                if eval > max_eval:
                    max_eval = eval
                    max_cord = cord
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  # Відсікання
            return max_eval, max_cord
        else:
            min_eval = float('inf')
            min_cord = None
            possible_moves = get_possible_moves(board, turn)
            if len(possible_moves) == 0:
                return self.alpha_beta(board, depth - 1, alpha, beta, True, ai_color, turn + 1)
            for cord in possible_moves:
                value = CellsValue.WHITE.value if ai_color == CellsValue.BLACK.value else CellsValue.BLACK.value
                child = self.get_child(board, value, cord)
                eval, _ = self.alpha_beta(child, depth - 1, alpha, beta, True, ai_color, turn + 1)
                if eval < min_eval:
                    min_eval = eval
                    min_cord = cord
                beta = min(beta, eval)
                if beta <= alpha:
                    break  # Відсікання
            return min_eval, min_cord
