import random

class BlackjackGame:

    def __init__(self, players, players_nicknames):
        self.turn = 0
        # 2 decks from 2 to 11
        if len(players) > 2:
            self.deck = [2,3,4,5,6,7,8,9,10,11,2,3,4,5,6,7,8,9,10,11]
        else:
            self.deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        self.players = players
        self.playersNicknames = players_nicknames
        self.board = {}
        self.passed = []
        # Let's give all players 2 cards
        for player in players:
            self.board[player] = [self.pickRandomCard(), self.pickRandomCard()]


    def pickRandomCard(self):
        index = random.randint(0, len(self.deck)-1)
        value = self.deck[index]
        del self.deck[index]
        return value

    def get_description(self):
        if len(self.passed) < len(self.players):
            res = f"Turn of {self.playersNicknames[self.turn%len(self.players)]}\n\n"
            for i in range(len(self.players)):
                line = f"{self.playersNicknames[i]}: ? "
                for j in range(1, len(self.board[self.players[i]])):
                    line += f"{self.board[self.players[i]][j]} "
                if self.players[i] in self.passed:
                    line += "PASS"
                res += line + "\n"
            return res
        else:
            maxCount = 0
            winners = []
            res = "Game finished\n\n"

            for i in range(len(self.players)):
                line = f"{self.playersNicknames[i]}: "
                for j in range(0, len(self.board[self.players[i]])):
                    line += f"{self.board[self.players[i]][j]} "
                res += line + "\n"
                points = sum(self.board[self.players[i]])
                if points == maxCount:
                    winners.append(self.playersNicknames[i])
                elif 21 >= points > maxCount:
                    winners = [self.playersNicknames[i]]
                    maxCount = points
            res += " ".join(winners) + " scored " + str(maxCount)
            return res

    def increase_turn(self):
        self.turn += 1
        if len(self.passed) == len(self.players):
            return
        while self.players[self.turn%len(self.players)] in self.passed:
            self.turn += 1
