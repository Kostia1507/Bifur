import random
from enum import Enum

with open("assets/wordle/valid-words.txt", "r") as file:
    words = [line.rstrip() for line in file]

with open("assets/wordle/possible-words.txt", "r") as file:
    possible_words = [line.rstrip() for line in file]

class ResultColor(Enum):
    GREEN = 0
    YELLOW = 1
    NONE = 2

class LetterStatus:

    def __init__(self, number, status, word):
        self.number = number
        self.status = status
        self.word = word

    def getLetter(self):
        return self.word[self.number]

class WordleGame:

    def __init__(self, user_id):
        self.user_id = user_id
        self.answer = random.choice(possible_words)
        self.history = []
        self.tries = 0
        self.possible_letters = ["q","w","e","r","t","y","u","i","o","p","a","s","d","f","g","h","j","k","l","z","x","c","v","b","n","m"]

    def makeMove(self, prompt: str):
        prompt = prompt.lower().strip()
        if prompt in words:
            ret = []
            yellowLoop = []
            counted = ""
            # let`s count green and red
            for i in range(0, 5):
                if prompt[i] == self.answer[i]:
                    ret.append((i, ResultColor.GREEN, prompt[i]))
                    counted += prompt[i]
                elif prompt[i] not in self.answer:
                    ret.append((i, ResultColor.NONE, prompt[i]))
                    counted += prompt[i]
                    if prompt[i] in self.possible_letters:
                        self.possible_letters.remove(prompt[i])
                else:
                    yellowLoop.append(i)
            # yellow now
            for i in yellowLoop:
                if self.answer.count(prompt[i]) > counted.count(prompt[i]):
                    ret.append((i, ResultColor.YELLOW, prompt[i]))
                else:
                    ret.append((i, ResultColor.NONE, prompt[i]))
                counted += prompt[i]
            ret.sort()
            self.tries += 1
            self.history.append(ret)
            return ret
        else:
            return None