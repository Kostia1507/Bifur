from enum import Enum


class SignValue(Enum):
    ROCK = 0
    PAPER = 1
    SCISSORS = 2


sign_text = ["Rock 🪨", "Paper 📰", "Scissors ✂️"]


class RPSGame:

    def __init__(self, players, players_nicknames):
        self.players = players
        self.playersNicknames = players_nicknames
        self.playersMoves = [None, None]
        # self.playersMoves = [SignValue.SCISSORS, SignValue.SCISSORS]
        self.messageId = None
        self.channelId = None

    def make_move(self, move, player_id):
        if player_id in self.players:
            player_index = 0 if self.players[0] == player_id else 1
            if self.playersMoves[player_index] is None:
                self.playersMoves[player_index] = move
                return True
        return False

    def is_game_ready_for_result(self):
        if self.playersMoves[0] is not None and self.playersMoves[1] is not None:
            return True
        return False

    def get_text(self):
        res = (f"{self.playersNicknames[0]}: {sign_text[self.playersMoves[0].value]}\n"
               f"{self.playersNicknames[1]}: {sign_text[self.playersMoves[1].value]}\n")
        if self.playersMoves[0] == self.playersMoves[1]:
            return res + "Draw!"
        else:
            if (self.playersMoves[0] == SignValue.SCISSORS and self.playersMoves[1] == SignValue.PAPER or
                    self.playersMoves[0] == SignValue.PAPER and self.playersMoves[1] == SignValue.ROCK or
                    self.playersMoves[0] == SignValue.ROCK and self.playersMoves[1] == SignValue.SCISSORS):
                return res + self.playersNicknames[0] + " won this game!"
            else:
                return res + self.playersNicknames[1] + " won this game!"
