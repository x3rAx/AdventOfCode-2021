#%% Setup

from dataclasses import dataclass, replace
from icecream import ic
import numpy as np
import time


@dataclass()
class Player:
    id: int
    position: int
    score: int = 0

    def copy(self):
        return replace(self)


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


class RecLogger:
    _counter = 0
    _lastTime = None
    _logEvery: int

    def __init__(self, logEvery=1):
        self._logEvery = logEvery

    def log(self, callback):
        self._counter += 1
        if self._counter < self._logEvery:
            return

        if self._lastTime is None:
            self._lastTime = time.time()
        else:
            timeDelta = time.time() - self._lastTime
            ic(timeDelta)
            self._lastTime = time.time()

        self._counter = 0
        callback()

        return


class QuantumDie:
    _sides: int

    def __init__(self, sides: int):
        self._sides = sides

    def roll(self):
        return range(1, self._sides + 1)

    def rolls(self, count):
        return product(self.roll(), repeat=count)


def copyPlayers(players: list[Player]):
    return [player.copy() for player in players]


def readPlayerPositions(inp: str):
    with open(inp, "r") as file:
        for line in file.read().splitlines():
            yield int(line.split(": ")[1])


def getPlayers(inp):
    return [Player(i, pos) for i, pos in enumerate(readPlayerPositions(inp))]


#%% Part 1

ic.disable()

players = getPlayers("input.txt")

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


#%% Part 2 - Too much copy

ic.disable()

from itertools import product


players = getPlayers("test-input.txt")

die = QuantumDie(3)
winCounter = {}

parallelWorlds = [players]

ic(players)

# NOTE: Running more than one step like this kills my PC
for iRound in range(1, 2):
    ic(iRound)
    newParallelWorld = []
    for players in parallelWorlds:
        playerOutcomes = []

        for player in players:
            outcomes = []

            possibleRolls = die.rolls(3)
            for rolls in possibleRolls:
                newPlayer = player.copy()

                move = sum(rolls)

                newPlayer.position = ((newPlayer.position + move - 1) % 10) + 1
                newPlayer.score += newPlayer.position

                if newPlayer.score >= 21:
                    ic(player)
                    winCount = winCounter.get(player.id, 0)
                    winCounter[player.id] = winCount + 1
                    break

                outcomes.append(newPlayer)

            playerOutcomes.append(outcomes)

        newParallelWorld += product(*playerOutcomes)

    parallelWorlds = newParallelWorld
    ic(len(parallelWorlds))


# %% Part 2 - Works but takes a lot of time (ca. 15:50 for input.txt, ca. 24:10 for test-input.txt)

ic.disable()

ic("-----")


def gameTurn(
    players: list[Player],
    playerAtTurn,
    turn=1,
    samePathCount=1,
    winCounter=None,
    recLogger=None,
):
    if winCounter is None:
        winCounter = {}

    possibleRolls = die.rolls(3)
    possibleMoves = [sum(x) for x in possibleRolls]
    uniqueMoves, counts = np.unique(np.array(possibleMoves), return_counts=True)

    for move, count in zip(uniqueMoves, counts):
        newPlayers = copyPlayers(players)
        player = newPlayers[playerAtTurn]

        player.position = ((player.position + move - 1) % 10) + 1
        player.score += player.position

        if player.score >= 21:
            winCount = winCounter.get(player.id, 0)
            winCounter[player.id] = winCount + samePathCount * count
            continue

        gameTurn(
            newPlayers,
            (playerAtTurn + 1) % len(newPlayers),
            turn + 1,
            samePathCount * count,
            winCounter,
            recLogger,
        )

    if recLogger is not None:
        recLogger.log(lambda: ic(winCounter))


players = getPlayers("input.txt")

die = QuantumDie(3)
winCounter = {}

# NOTE: Uncomment below to run this block
# gameTurn(players, 0, recLogger=RecLogger(1000), winCounter=winCounter)
# print(winCounter)
# print()
# print("Result 2:", max(winCounter.values()))


# %% Part 2 - More optimized (estimated speedup about 1.8x) - ca. 8:40 for input.txt

ic.enable()

ic("-----")


def gameTurn(
    players: list[Player],
    playerAtTurn,
    turn=1,
    samePathCount=1,
    winCounter=None,
    recLogger=None,
):
    if winCounter is None:
        winCounter = {}

    possibleRolls = die.rolls(3)
    possibleMoves = [sum(x) for x in possibleRolls]
    uniqueMoves, counts = np.unique(np.array(possibleMoves), return_counts=True)

    for move, count in zip(uniqueMoves, counts):
        player = players[playerAtTurn]
        origPos = player.position
        origScore = player.score

        player.position = ((player.position + move - 1) % 10) + 1
        player.score += player.position

        if player.score >= 21:
            # ic(player)
            winCount = winCounter.get(player.id, 0)
            winCounter[player.id] = winCount + samePathCount * count
        else:
            gameTurn(
                players,
                (playerAtTurn + 1) % len(players),
                turn + 1,
                samePathCount * count,
                winCounter,
                recLogger,
            )

        player.position = origPos
        player.score = origScore

    if recLogger is not None:
        recLogger.log(lambda: ic(winCounter))


players = getPlayers("input.txt")

die = QuantumDie(3)
winCounter = {}

gameTurn(players, 0, recLogger=RecLogger(10000), winCounter=winCounter)

print(winCounter)
print()
print("Result 2:", max(winCounter.values()))
