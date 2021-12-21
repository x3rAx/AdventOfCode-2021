#%% Setup

from dataclasses import dataclass, field
from itertools import count
from icecream import ic


@dataclass()
class Player:
    id: int = field(default_factory=count().__next__, init=False)
    position: int
    score: int = 0


class DeterministicDie:
    _sides: int
    _counter = 0

    def __init__(self, sides):
        self._sides = sides
        pass

    def roll(self):
        self._counter = (self._counter % self._sides) + 1
        return self._counter

    def rolls(self, count):
        return [self.roll() for _ in range(count)]


def readPlayerPositions(inp: str):
    with open(inp, "r") as file:
        for line in file.read().splitlines():
            yield int(line.split(": ")[1])


players = [Player(pos) for pos in readPlayerPositions("input.txt")]


#%% Part 1

die = DeterministicDie(100)
rollCount = 0
winner = None

ic(players)

for iRound in range(1, 100000):
    for player in players:
        rolls = die.rolls(3)
        rollCount += len(rolls)
        move = sum(rolls)

        ic(iRound, player, rolls, move, rollCount)
        player.position = ((player.position + move - 1) % 10) + 1
        player.score += player.position
        ic(iRound, player)

        if player.score >= 1000:
            winner = player
            break
    else:
        continue
    break

loserScores = sum([player.score for player in players if player is not winner])

print()
print("Result 1:", loserScores * rollCount)
