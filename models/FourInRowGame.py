import random
import copy
from datetime import datetime
from io import BytesIO
from typing import Any, Union

from PIL import ImageDraw, Image
from PIL.Image import Image as IMG

from service.TransparertAnimatedGifConverter import TransparentAnimatedGifConverter

numbers = [":one:", ":two:", ":three:", ":four:", ":five:", ":six:", ":seven:", ":eight:", ":nine:"]
POINTS_FOR_CENTER = 3
POINTS_FOR_ALL_ROW = 100
POINTS_FOR_3_IN_ROW = 5
POINTS_FOR_2_IN_ROW = 2
POINTS_FOR_2_ENEMY_IN_ROW = -1
POINTS_FOR_3_ENEMY_IN_ROW = -4
POINTS_FOR_4_ENEMY_IN_ROW = -99


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


class FourInRowGame:

    # 0 - empty 1 - red 5 - blue
    # so if sum is 4 or 20 someone won

    def __init__(self, width, height, players):
        self.messageId = None
        self.channelId = None
        self.startText = None
        self.history = []
        self.move = 1
        self.width = width
        self.height = height
        self.players = players
        self.board = [[0 for x in range(width)] for y in range(height)]
        self.lastIterated = datetime.utcnow().hour

    def printBoard(self):
        result = self.startText
        result += "Wave: :blue_circle:\n" if self.move % 2 == 1 else "Wave: :red_circle:\n"
        lookForLast = False
        lastLine = -1
        if len(self.history) > 3:
            lookForLast = True
            lastLine = self.history[-1]
        for row in self.board:
            for lineNumber in range(len(row)):
                value = row[lineNumber]
                if value == 0:
                    result += ":white_circle:"
                if value == 1:
                    if lookForLast and lastLine == lineNumber:
                        result += ":orange_circle:"
                        lookForLast = False
                    else:
                        result += ":red_circle:"
                if value == 5:
                    if lookForLast and lastLine == lineNumber:
                        result += ":purple_circle:"
                        lookForLast = False
                    else:
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
                    self.history.append(line)
                    self.board[self.height - 1 - i][line] = 1 if self.move % 2 == 1 else 5
                    break

    def makeBotMove(self, bot_id):
        waveOf = self.players[self.move % 2]
        if waveOf == bot_id:
            # First move bot will make by random. It will create unique games against him
            if self.move == 2:
                line = random.choice(self.get_empty_columns(self.board))
            else:
                best_score, best_move = self.alpha_beta(copy.deepcopy(self.board), depth=4, alpha=float('-inf'), beta=float('inf'), maximizing_player=True)
                line = best_move
            for i in range(0, self.height):
                if self.board[self.height - 1 - i][line] == 0:
                    self.move += 1
                    self.history.append(line)
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
        for i in range(self.height - 3):
            for g in range(self.width):
                suma = self.board[i][g] + self.board[i + 1][g] + self.board[i + 2][g] + self.board[i + 3][g]
                if suma == 4:
                    return 1
                if suma == 20:
                    return 2
        # check all diagonals
        for i in range(self.height - 3):
            for g in range(self.width - 3):
                suma = self.board[i][g] + self.board[i + 1][g + 1] + self.board[i + 2][g + 2] + self.board[i + 3][g + 3]
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

    def get_empty_columns(self, board):
        ret = []
        for rows in range(self.width):
            if board[0][rows] == 0:
                ret.append(rows)
        return ret

    def get_child(self, board: list, player_ball: int, line):
        child = copy.deepcopy(board)
        for i in range(0, self.height):
            if child[self.height - 1 - i][line] == 0:
                child[self.height - 1 - i][line] = player_ball
                break
        return child

    # Return True if game was finished
    def is_terminal(self, board):
        for i in range(self.height):
            for g in range(self.width - 3):
                suma = board[i][g] + board[i][g + 1] + board[i][g + 2] + board[i][g + 3]
                if suma == 4 or suma == 20:
                    return True
            # check all columns
        for i in range(self.height - 3):
            for g in range(self.width):
                suma = board[i][g] + board[i + 1][g] + board[i + 2][g] + board[i + 3][g]
                if suma == 4 or suma == 20:
                    return True
            # check all diagonals
        for i in range(self.height - 3):
            for g in range(self.width - 3):
                suma = board[i][g] + board[i + 1][g + 1] + board[i + 2][g + 2] + board[i + 3][g + 3]
                if suma == 4 or suma == 20:
                    return True
            # check all reversed diagonals
        for i in range(self.height - 3):
            for g in range(self.width - 3):
                suma = board[i][g + 3] + board[i + 1][g + 2] + board[i + 2][g + 1] + board[i + 3][g]
                if suma == 4 or suma == 20:
                    return True
            # check is there any empty cells
        for i in range(self.height):
            for g in range(self.width):
                if self.board[i][g] == 0:
                    return False
        return True

    def evaluate(self, board):
        # Cells were bot placed ball = 1
        player_ball = 1

        score = 0
        # Центр дошки
        center_columns = []
        if self.width % 2 == 1:
            center_columns.append(board[(self.width - 1) // 2])
        else:
            center_columns.append(board[self.width // 2])
            center_columns.append(board[self.width // 2 - 1])
        for row in center_columns:
            for cell in row:
                if cell == player_ball:
                    score += POINTS_FOR_CENTER

        # Оцінка рядків
        # check all rows
        for i in range(self.height):
            for g in range(self.width - 3):
                row = [board[i][g], board[i][g + 1], board[i][g + 2], board[i][g + 3]]
                score += evaluate_row(row, player_ball)
        # check all columns
        for i in range(self.height - 3):
            for g in range(self.width):
                row = [board[i][g], board[i + 1][g], board[i + 2][g], board[i + 3][g]]
                score += evaluate_row(row, player_ball)
        # check all diagonals
        for i in range(self.height - 3):
            for g in range(self.width - 3):
                row = [board[i][g], board[i + 1][g + 1], board[i + 2][g + 2], board[i + 3][g + 3]]
                score += evaluate_row(row, player_ball)
        # check all reversed diagonals
        for i in range(self.height - 3):
            for g in range(self.width - 3):
                row = [board[i][g + 3], board[i + 1][g + 2], board[i + 2][g + 1], board[i + 3][g]]
                score += evaluate_row(row, player_ball)
        return score

    def alpha_beta(self, board, depth, alpha, beta, maximizing_player):
        if depth == 0 or self.is_terminal(board):
            return self.evaluate(board), -1

        if maximizing_player:
            max_eval = float('-inf')
            max_line = self.width//2
            possible_moves = self.get_empty_columns(board)
            for line in possible_moves:
                child = self.get_child(board, 1, line)  # Отримуємо всі можливі ходи
                eval, _ = self.alpha_beta(child, depth - 1, alpha, beta, False)
                if eval > max_eval:
                    max_eval = eval
                    max_line = line
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  # Відсікання
            return max_eval, max_line
        else:
            min_eval = float('inf')
            min_line = self.width//2
            possible_moves = self.get_empty_columns(board)
            for line in possible_moves:
                child = self.get_child(board, 5, line)
                eval, _ = self.alpha_beta(child, depth - 1, alpha, beta, True)
                if eval < min_eval:
                    min_eval = eval
                    min_line = line
                beta = min(beta, eval)
                if beta <= alpha:
                    break  # Відсікання
            return min_eval, min_line

    async def animate_history(self):
        SIZE = 40
        GRAY_COLOR = "#ef1346"
        BLUE_COLOR = "#16b1ea"
        RED_COLOR = "#ef1346"

        width, height = self.width * SIZE, self.height * SIZE

        frames = [Image.new('RGBA', size=(width, height), color=(0, 0, 0, 0))]
        current_height = []
        for i in range(0, self.width):
            current_height.append(0)

        for move in range(0, len(self.history)):
            canvas = frames[-1].copy()
            draw = ImageDraw.Draw(canvas)
            current_color = BLUE_COLOR if move % 2 == 0 else RED_COLOR
            draw.ellipse(((self.history[move]*SIZE, height-(current_height[self.history[move]]+1)*SIZE),
                          ((self.history[move]+1)*SIZE, height-current_height[self.history[move]]*SIZE)),
                         fill=current_color)
            frames.append(canvas)
            current_height[self.history[move]] = current_height[self.history[move]] + 1

        frames.append(frames[-1].copy())
        frames.append(frames[-1].copy())

        gif_image, save_kwargs = await self.__animate_gif(frames)

        buffer = BytesIO()
        gif_image.save(buffer, **save_kwargs)
        buffer.seek(0)

        return buffer

    async def __animate_gif(self, images: list[IMG], durations: Union[int, list[int]] = 100) -> tuple[
        IMG, dict[str, Any]]:
        save_kwargs: dict[str, Any] = {}
        new_images: list[IMG] = []

        for frame in images:
            thumbnail = frame.copy()
            thumbnail_rgba = thumbnail.convert(mode='RGBA')
            thumbnail_rgba.thumbnail(size=frame.size, reducing_gap=3.0)
            converter = TransparentAnimatedGifConverter(img_rgba=thumbnail_rgba)
            thumbnail_p = converter.process()
            new_images.append(thumbnail_p)

        output_image = new_images[0]
        save_kwargs.update(
            format='GIF',
            save_all=True,
            optimize=False,
            append_images=new_images[1:],
            duration=durations,
            disposal=2,  # Other disposals don't work
            loop=0)

        return output_image, save_kwargs
