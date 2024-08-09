from datetime import datetime

numbers = [":one:", ":two:", ":three:", ":four:", ":five:", ":six:", ":seven:", ":eight:", ":nine:"]


class FourInRowGame:

    # 0 - empty 1 - red 5 - blue
    # so if sum is 4 or 20 someone won

    def __init__(self, width, height, players):
        self.messageId = None
        self.channelId = None
        self.startText = None
        self.move = 1
        self.width = width
        self.height = height
        self.players = players
        self.board = [[0 for x in range(width)] for y in range(height)]
        self.lastIterated = datetime.utcnow().hour

    def printBoard(self):
        result = self.startText
        result += "Wave: :blue_circle:\n" if self.move%2 == 1 else "Wave: :red_circle:\n"
        for row in self.board:
            for value in row:
                if value == 0:
                    result += ":white_circle:"
                if value == 1:
                    result += ":red_circle:"
                if value == 5:
                    result += ":blue_circle:"
            result += '\n'
        for i in range(0, self.width):
            result += numbers[i]
        return result

    def makeMove(self, user_id, line):
        waveOf = self.players[self.move % 2]
        if waveOf == user_id:
            for i in range(0, self.height):
                if self.board[self.height - 1 - i][line] == 0:
                    self.lastIterated = datetime.utcnow().hour
                    self.move += 1
                    self.board[self.height - 1 - i][line] = 1 if self.move % 2 == 1 else 5
                    break

    # 1 - red won 2 - blue won 3 - draw 0 - not finished
    def isEnd(self):
        # check all rows
        for i in range(self.height):
            for g in range(self.width - 3):
                suma = self.board[i][g] + self.board[i][g + 1] + self.board[i][g + 2] + self.board[i][g + 3]
                if suma == 4:
                    return 1
                if suma == 20:
                    return 2
        # check all columns
        for i in range(self.height-3):
            for g in range(self.width):
                suma = self.board[i][g] + self.board[i + 1][g] + self.board[i + 2][g] + self.board[i + 3][g]
                if suma == 4:
                    return 1
                if suma == 20:
                    return 2
        # check all diagonals
        for i in range(self.height-3):
            for g in range(self.width-3):
                suma = self.board[i][g] + self.board[i + 1][g+1] + self.board[i + 2][g + 2] + self.board[i + 3][g + 3]
                if suma == 4:
                    return 1
                if suma == 20:
                    return 2
        # check all reversed diagonals
        for i in range(self.height - 3):
            for g in range(self.width - 3):
                suma = self.board[i][g + 3] + self.board[i + 1][g + 2] + self.board[i + 2][g + 1] + self.board[i + 3][g]
                if suma == 4:
                    return 1
                if suma == 20:
                    return 2
        # check is there any empty cells
        for i in range(self.height):
            for g in range(self.width):
                if self.board[i][g] == 0:
                    return 0
        return 3