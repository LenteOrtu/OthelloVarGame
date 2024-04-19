from player import Player
from board import Board
from numpy import random
import random as rand


# Conducts a 1 v 1 Knockout Elimination Style Tournament and returns the winner's weights.
def tournament(weights):
    while len(weights) > 1:
        newWeights = []
        for j in range(1, len(weights), 2):
            # Randomly determine color of each 'player'.
            if random.uniform() <= 0.5:
                newWeights.append(battle(weights[j-1], weights[j])[0])
            else:
                newWeights.append(battle(weights[j], weights[j-1])[0])
        weights = newWeights

    return weights[0]


# Plays game between two bots with specified weights, returns tuple with  winner's weights and 1 if black wins, 0 if white wins or -1 if it's a tie.
def battle(blackWeights, whiteWeights, maxDepth = 2):
    board = Board()
    checkers = [30, 30]
    turn = 1

    blackPlayer = Player(maxDepth, 1, blackWeights)
    whitePlayer = Player(maxDepth, 0, whiteWeights)
    players = [whitePlayer, blackPlayer]
    i = 0
    while checkers[0] + checkers[1] > 0:
        #print(f"turn {i}")
        if board.hasLegalMove(turn):

            moveCoords = players[turn].miniMax(board)
            board.makeMove(moveCoords[0], moveCoords[1], turn)

            # A player must give a checker to the other player if he doesn't have one to play.
            if checkers[turn] == 0:
                checkers[1 - turn] -= 1
                checkers[turn] += 1
                checkers[turn] -= 1

        if board.isTerminal(): break

        turn = 1 - turn
        i += 1

    if board.colors[0] > board.colors[1]:
        return whiteWeights, 0
    elif board.colors[0] < board.colors[1]:
        return blackWeights, 1
    else:
        if random.uniform() <= 0.5:
            return whiteWeights, -1
        else:
            return blackWeights, -1


# Using Modified Kraemer Algorithm to generate uniformly distributed pi s.t sum(pi) = 1,Note: every pi <> 0
def generateStartingWeights(numOfTuples, numOfWeights):
    startingWeightsSet = set([])
    startingWeights = []

    i = 0
    while i < numOfTuples:
        tuple = generateTuple(numOfWeights, 1)
        if str(tuple) not in startingWeightsSet:
            startingWeightsSet.add(str(tuple))
            startingWeights.append(tuple)
            i += 1
    
    return startingWeights


# Modified Kraemer Algorithm to generate uniformly distributed pi's s.t sum(pi) = sm,Note: every pi <> 0
def generateTuple(numOfWeights, sm):
    M = 1000000
    t = rand.sample(range(M+1), numOfWeights - 1)
    t.append(0)
    t.append(M)
    t.sort()
    y = []
    for i in range(1, len(t)):
        y.append((t[i]-t[i-1])/M*sm)

    return tuple(y)


# Conducts numOfTuples tournaments with numOfContestants number of contestants per tournament,
# then conducts final tournament with winners of the tournaments and prints the
# winner's weights.
def determine(numOfTuples, numOfContestants, numOfWeights):
    finale = []
    for i in range(numOfTuples):
        finale.append(tournament(generateStartingWeights(numOfContestants, numOfWeights)))

    print(tournament(finale))


numOfTuples = int(input("Number of tournaments: "))
numOfContestants = int(input("Number of contestants: "))
numOfWeights = int(input("Number of weights: "))
determine(numOfTuples, numOfContestants, numOfWeights)