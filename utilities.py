from board import Board


def u(board, diskColor, weights):
    return weights[0] * u1(board, diskColor) + weights[1] * u2(board) + weights[2] * u3(board, diskColor) + weights[3] * u4(board) + u5(board, diskColor)


# How many more disks are in the terminal state from the initial state
def u1(board, diskColor):
    maxValue = 64 - 1 # E.g. starts from 1 black and x white and ends up with 64 black and 0 white
    return (board.colors[diskColor] - board.initialColors[diskColor])


# The sum of possible moves until the max depth
def u2(board):
    return board.legalMovesSum


# red_value = 100, green_val = 16, blue_val = 25, orange_val = 1
def u3(board, diskColor):
    values = [16, 25, 1, 100]

    # Board Position Values
    posValues = [[values[0] for _ in range(8)] for k in range(8)]

    for i in range(1, 4):
        for pos in getPosValues()[i]:
            posValues[pos[0]][pos[1]] = values[i] * (1 if i != 2 else board.colors[0] + board.colors[1])

    totalValue = 0
    for i in range(len(board.board)):
        for j in range(len(board.board[0])):
            if board.board[i][j] == diskColor:
                totalValue += posValues[i][j]
    
    return totalValue


# the amount of legal moves the opponent has
# 1 - normalized value
def u4(board):
    # 32 = max amount of legal moves
    return 32 * board.opponentTimesPlayed - board.opponentLegalMovesSum


def u5(board, diskColor):
    if not board.isTerminal() or board.colors[0] == board.colors[1]: return 0
    bigNumber = 10 ** 5

    return bigNumber if board.colors[diskColor] > board.colors[1-diskColor] else -bigNumber


def getPosValues():
    redPositions = [(0, 0), (0, 7), (7, 0), (7, 7)]
    orangePositions = [(0, 1), (1, 0), (1, 1), (0, 6), (1, 7), (1, 6), (6, 0), (6, 1), (7, 1), (7, 6), (6, 6), (6, 7)]
    bluePositions = [(0, i) for i in range(2, 6)] + [(i, 0) for i in range(2, 6)] + [(7, i) for i in range(2, 6)] + [(i, 7) for i in range(2, 6)]

    return [None, bluePositions, orangePositions, redPositions]