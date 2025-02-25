import random

class BlackjackGame:

    def __init__(self, players, players_nicknames):
        self.turn = 0
        # 2 decks from 2 to 11
        self.deck = [2,3,4,5,6,7,8,9,10,11,2,3,4,5,6,7,8,9,10,11]
        self.players = players
        self.playersNicknames = players_nicknames
        self.board = {}
        # Let's give all players 2 cards
        for player in players:
            self.board[player] = [self.pickRandomCard(), self.pickRandomCard()]



    def pickRandomCard(self):
        index = random.randint(0, len(self.deck)-1)
        value = self.deck[index]
        del self.deck[index]
        return value

    def get_description(self):
        res = ""
        for i in range(len(self.players)):
            line = f"{self.playersNicknames[i]}: ? "
            for j in range(1, len(self.board[self.players[i]])):
                line += f"{self.board[self.players[i]][j]} "
            res += line + "\n"
        return res


