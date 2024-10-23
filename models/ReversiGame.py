from datetime import datetime
from enum import Enum

columnLetters = "abcdefgh"
BOARD_SIZE = 8

class CellsValue(Enum):
    EMPTY = 0
    WHITE = 1
    BLACK = 2

# This method converts cords like "e4" to numbers
def convert_str_to_cords(loop: str):
    first,last = loop[0], loop[1]
    if first.isnumeric():
        first, last = last, first
    return 8-int(last), columnLetters.find(first)

# return True if there is no moves for all players
def is_terminal(board):
    possible = get_possible_moves(board, 0)
    if len(possible) > 0:
        return False
    possible = get_possible_moves(board, 1)
    if len(possible) > 0:
        return False
    return True

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
                for change in range(1, 8):
                    if row-change < 0 or col-change < 0:
                        break
                    if board[row-change][col-change] == CellsValue.EMPTY.value:
                        break
                    elif board[row-change][col-change] == enemy:
                        enemies += 1
                        continue
                    elif enemies > 0:
                        ret += (row, col)
                        found = True
                        break
                enemies = 0
                if found:
                    continue
                # left
                for change in range(1, 8):
                    if col - change < 0:
                        break
                    if board[row][col - change] == CellsValue.EMPTY.value:
                        break
                    elif board[row][col - change] == enemy:
                        enemies += 1
                        continue
                    elif enemies > 0:
                        ret += (row, col)
                        found = True
                        break
                enemies = 0
                if found:
                    continue
                # left bottom
                for change in range(1, 8):
                    if col - change < 0 or row + change >= BOARD_SIZE:
                        break
                    if board[row + change][col - change] == CellsValue.EMPTY.value:
                        break
                    elif board[row + change][col - change] == enemy:
                        enemies += 1
                        continue
                    elif enemies > 0:
                        ret += (row, col)
                        found = True
                        break
                enemies = 0
                if found:
                    continue
                # bottom
                for change in range(1, 8):
                    if row + change >= BOARD_SIZE:
                        break
                    if board[row + change][col] == CellsValue.EMPTY.value:
                        break
                    elif board[row + change][col] == enemy:
                        enemies += 1
                        continue
                    elif enemies > 0:
                        ret += (row, col)
                        found = True
                        break
                enemies = 0
                if found:
                    continue
                # bottom-right
                for change in range(1, 8):
                    if row + change >= BOARD_SIZE or col + change >= BOARD_SIZE:
                        break
                    if board[row + change][col + change] == CellsValue.EMPTY.value:
                        break
                    elif board[row + change][col + change] == enemy:
                        enemies += 1
                        continue
                    elif enemies > 0:
                        print(board[row + change][col + change])
                        ret += (row, col)
                        found = True
                        break
                enemies = 0
                if found:
                    continue
                # right
                for change in range(1, 8):
                    if col + change >= BOARD_SIZE:
                        break
                    if board[row][col + change] == CellsValue.EMPTY.value:
                        break
                    elif board[row][col + change] == enemy:
                        enemies += 1
                        continue
                    elif enemies > 0:
                        ret += (row, col)
                        found = True
                        break
                enemies = 0
                if found:
                    continue
                # top-right
                for change in range(1, 8):
                    if row - change < 0 or col + change >= BOARD_SIZE:
                        break
                    if board[row - change][col + change] == CellsValue.EMPTY.value:
                        break
                    elif board[row - change][col + change] == enemy:
                        enemies += 1
                        continue
                    elif enemies > 0:
                        ret += (row, col)
                        found = True
                        break
                enemies = 0
                if found:
                    continue
                # top
                for change in range(1, 8):
                    if row - change < 0:
                        break
                    if board[row - change][col] == CellsValue.EMPTY.value:
                        break
                    elif board[row - change][col] == enemy:
                        enemies += 1
                        continue
                    elif enemies > 0:
                        ret += (row, col)
                        found = True
                        break
                if found:
                    continue
    return ret


class ReversiGame:

    def __init__(self, players, players_nicknames):
        self.board = [[CellsValue.EMPTY.value for _ in range(BOARD_SIZE) ] for _ in range(BOARD_SIZE)]
        self.board[3][4] = CellsValue.BLACK.value
        self.board[4][3] = CellsValue.BLACK.value
        self.board[3][3] = CellsValue.WHITE.value
        self.board[4][4] = CellsValue.WHITE.value
        self.turn = 0 # if turn is even - black turn, else white
        self.players = players
        self.playersNicknames = players_nicknames
        self.messageId = None
        self.channelId = None
        self.startText = f"2⚫ {self.playersNicknames[0]} -  2⚪ {self.playersNicknames[1]}"
        self.lastIterated = datetime.utcnow().hour

    def make_move(self, row, col, player_id):
        if player_id == self.players[self.turn//2]:
            value = CellsValue.BLACK.value if self.turn % 2 == 0 else CellsValue.WHITE.value
            enemy = CellsValue.WHITE.value if self.turn % 2 == 0 else CellsValue.BLACK.value
            cellsToChange = []
            enemies = []

            # left top
            for change in range(1, 8):
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
            for change in range(1, 8):
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
            for change in range(1, 8):
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
            for change in range(1, 8):
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
            for change in range(1, 8):
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
            for change in range(1, 8):
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
            for change in range(1, 8):
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
            for change in range(1, 8):
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
            # checks finished
            if len(cellsToChange) == 0:
                return False
            else:
                for cords in cellsToChange:
                    self.board[cords[0]][cords[1]] = value
                self.board[row][col] = value
                self.turn += 1
                return True
        else:
            return False
