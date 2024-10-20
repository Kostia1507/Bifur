import random
import copy
from datetime import datetime
from io import BytesIO
from typing import Any, Union

BLUE_CIRCLE = "🔵"
RED_CROSS = "❌"

POINTS_FOR_CENTER = 5
POINTS_FOR_CENTER_DIAGONAL = 1
POINTS_FOR_ALL_ROW = 120
POINTS_FOR_3_IN_ROW = 30
POINTS_FOR_2_IN_ROW = 10
POINTS_FOR_2_ENEMY_IN_ROW = -10
POINTS_FOR_3_ENEMY_IN_ROW = -30
POINTS_FOR_4_ENEMY_IN_ROW = -115


def evaluate_row(row, player):
    score = 0
    opponent = 1 if player == 5 else 5
    empty_cells, player_cells, opponent_cells = 0, 0, 0
    for i in row:
        if i == player:
            player_cells += 1
        elif i == opponent:
            opponent_cells += 1
        else:
            empty_cells += 1

    if player_cells == 4:
        score += POINTS_FOR_ALL_ROW
    elif player_cells == 3 and empty_cells == 1:
        score += POINTS_FOR_3_IN_ROW
    elif player_cells == 2 and empty_cells == 2:
        score += POINTS_FOR_2_IN_ROW
    elif opponent_cells == 2 and empty_cells == 2:
        score += POINTS_FOR_2_ENEMY_IN_ROW
    elif opponent_cells == 3 and empty_cells == 1:
        score += POINTS_FOR_3_ENEMY_IN_ROW
    elif opponent_cells == 4:
        score += POINTS_FOR_4_ENEMY_IN_ROW

    return score


# 0 - empty 1 - red 5 - blue
# so if sum is 4 or 20 someone won
class TicTacToeGame:

    def __init__(self, players):
        self.messageId = None
        self.channelId = None
        self.startText = None
        self.finished = False
        self.ai_game = False
        self.difficult = 4
        self.history = []
        self.move = 1
        self.size = 5
        self.players = players
        self.board = [[0 for x in range(self.size)] for y in range(self.size)]
        self.lastIterated = datetime.utcnow().hour

    def makeMove(self, user_id, x, y):
        waveOf = self.players[self.move % 2]
        if self.board[x][y] == 0 and waveOf == user_id and not self.finished:
            self.lastIterated = datetime.utcnow().hour
            self.move += 1
            self.history.append((x, y))
            self.board[x][y] = 1 if self.move % 2 == 1 else 5
            if self.ai_game and not self.is_terminal(self.board):
                best_score, best_move = self.alpha_beta(copy.deepcopy(self.board), depth=self.difficult,
                                                        alpha=float('-inf'), beta=float('inf'), maximizing_player=True)
                if best_move is None or self.board[best_move[0]][best_move[1]] != 0:
                    # better to define your logic here, idk
                    moved = False
                    for x in range(self.size):
                        for y in range(self.size):
                            if self.board[x][y] == 0 and not moved:
                                self.board[x][y] = 1
                                self.move += 1
                                moved = True
                                break
                else:
                    self.board[best_move[0]][best_move[1]] = 1
                    self.move += 1
            return True
        return False

    # 1 - red won 2 - blue won 3 - draw 0 - not finished
    def isEnd(self):
        # check all rows
        for i in range(self.size):
            for g in range(self.size - 3):
                suma = self.board[i][g] + self.board[i][g + 1] + self.board[i][g + 2] + self.board[i][g + 3]
                if suma == 4:
                    return 1
                if suma == 20:
                    return 2
        # check all columns
        for i in range(self.size - 3):
            for g in range(self.size):
                suma = self.board[i][g] + self.board[i + 1][g] + self.board[i + 2][g] + self.board[i + 3][g]
                if suma == 4:
                    return 1
                if suma == 20:
                    return 2
        # check all diagonals
        for i in range(self.size - 3):
            for g in range(self.size - 3):
                suma = self.board[i][g] + self.board[i + 1][g + 1] + self.board[i + 2][g + 2] + self.board[i + 3][g + 3]
                if suma == 4:
                    return 1
                if suma == 20:
                    return 2
        # check all reversed diagonals
        for i in range(self.size - 3):
            for g in range(self.size - 3):
                suma = self.board[i][g + 3] + self.board[i + 1][g + 2] + self.board[i + 2][g + 1] + self.board[i + 3][g]
                if suma == 4:
                    return 1
                if suma == 20:
                    return 2
        # check is there any empty cells
        for i in range(self.size):
            for g in range(self.size):
                if self.board[i][g] == 0:
                    return 0
        return 3

    # Return True if game was finished
    def is_terminal(self, board):
        for i in range(self.size):
            for g in range(self.size - 3):
                suma = board[i][g] + board[i][g + 1] + board[i][g + 2] + board[i][g + 3]
                if suma == 4 or suma == 20:
                    return True
            # check all columns
        for i in range(self.size - 3):
            for g in range(self.size):
                suma = board[i][g] + board[i + 1][g] + board[i + 2][g] + board[i + 3][g]
                if suma == 4 or suma == 20:
                    return True
            # check all diagonals
        for i in range(self.size - 3):
            for g in range(self.size - 3):
                suma = board[i][g] + board[i + 1][g + 1] + board[i + 2][g + 2] + board[i + 3][g + 3]
                if suma == 4 or suma == 20:
                    return True
            # check all reversed diagonals
        for i in range(self.size - 3):
            for g in range(self.size - 3):
                suma = board[i][g + 3] + board[i + 1][g + 2] + board[i + 2][g + 1] + board[i + 3][g]
                if suma == 4 or suma == 20:
                    return True
            # check is there any empty cells
        for i in range(self.size):
            for g in range(self.size):
                if self.board[i][g] == 0:
                    return False
        return True

    def get_empty_cells(self, board):
        for x in range(self.size):
            for y in range(self.size):
                if board[x][y] == 0:
                    yield x, y

    def get_child(self, board: list, player_ball: int, x, y):
        child = copy.deepcopy(board)
        if child[x][y] == 0:
            child[x][y] = player_ball
        return child

    def evaluate(self, board):
        # Cells were bot placed ball = 1
        player_mark = 1

        score = POINTS_FOR_CENTER + 4*POINTS_FOR_CENTER_DIAGONAL
        score += POINTS_FOR_CENTER if board[2][2] == player_mark else - POINTS_FOR_CENTER
        score += POINTS_FOR_CENTER_DIAGONAL if board[0][0] == player_mark else - POINTS_FOR_CENTER_DIAGONAL
        score += POINTS_FOR_CENTER_DIAGONAL if board[1][1] == player_mark else - POINTS_FOR_CENTER_DIAGONAL
        score += POINTS_FOR_CENTER_DIAGONAL if board[3][3] == player_mark else - POINTS_FOR_CENTER_DIAGONAL
        score += POINTS_FOR_CENTER_DIAGONAL if board[4][4] == player_mark else - POINTS_FOR_CENTER_DIAGONAL
        score += POINTS_FOR_CENTER_DIAGONAL if board[4][0] == player_mark else - POINTS_FOR_CENTER_DIAGONAL
        score += POINTS_FOR_CENTER_DIAGONAL if board[3][1] == player_mark else - POINTS_FOR_CENTER_DIAGONAL
        score += POINTS_FOR_CENTER_DIAGONAL if board[1][3] == player_mark else - POINTS_FOR_CENTER_DIAGONAL
        score += POINTS_FOR_CENTER_DIAGONAL if board[0][4] == player_mark else - POINTS_FOR_CENTER_DIAGONAL

        # Оцінка рядків
        # check all rows
        for i in range(self.size):
            for g in range(self.size - 3):
                row = [board[i][g], board[i][g + 1], board[i][g + 2], board[i][g + 3]]
                score += evaluate_row(row, player_mark)
        # check all columns
        for i in range(self.size - 3):
            for g in range(self.size):
                row = [board[i][g], board[i + 1][g], board[i + 2][g], board[i + 3][g]]
                score += evaluate_row(row, player_mark)
        # check all diagonals
        for i in range(self.size - 3):
            for g in range(self.size - 3):
                row = [board[i][g], board[i + 1][g + 1], board[i + 2][g + 2], board[i + 3][g + 3]]
                score += evaluate_row(row, player_mark)
        # check all reversed diagonals
        for i in range(self.size - 3):
            for g in range(self.size - 3):
                row = [board[i][g + 3], board[i + 1][g + 2], board[i + 2][g + 1], board[i + 3][g]]
                score += evaluate_row(row, player_mark)
        return score

    def alpha_beta(self, board, depth, alpha, beta, maximizing_player):
        if depth == 0 or self.is_terminal(board):
            return self.evaluate(board), -1

        if maximizing_player:
            max_eval = float('-inf')
            max_cord = None
            possible_moves = self.get_empty_cells(board)
            for cord in possible_moves:
                child = self.get_child(board, 1, cord[0], cord[1])
                eval, _ = self.alpha_beta(child, depth - 1, alpha, beta, False)
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
            possible_moves = self.get_empty_cells(board)
            for cord in possible_moves:
                child = self.get_child(board, 5, cord[0], cord[1])
                eval, _ = self.alpha_beta(child, depth - 1, alpha, beta, True)
                if eval < min_eval:
                    min_eval = eval
                    min_cord = cord
                beta = min(beta, eval)
                if beta <= alpha:
                    break  # Відсікання
            return min_eval, min_cord
