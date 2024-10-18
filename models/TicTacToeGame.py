import random
import copy
from datetime import datetime
from io import BytesIO
from typing import Any, Union

BLUE_CIRCLE = "🔵"
RED_CROSS = "❌"

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
            self.history.append((x,y))
            self.board[x][y] = 1 if self.move % 2 == 1 else 5
            if self.ai_game:
                pass
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

