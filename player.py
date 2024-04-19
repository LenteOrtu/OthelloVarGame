from numpy import random 
from utilities import *
from board import Board


class Player: 
    def __init__(self, maxDepth, diskColor, weights):
        self.maxDepth = maxDepth
        self.optCoords = (-1, -1)
        self.diskColor = diskColor
        # Weights for the heuristic functions.
        self.weights = weights
    
    def miniMax(self, board):
        # Keep track of board's initial colors, needed for heuristic u1.
        board.initialColors[0] = board.colors[0]
        board.initialColors[1] = board.colors[1]

        self.maxValue(board, 0, float('-inf'), float('inf')) 
        return self.optCoords

    def maxValue(self, board, depth, a, b):
        if board.isTerminal() or depth == self.maxDepth:
            return u(board, self.diskColor, self.weights)

        currMax = float('-inf')
        maxCoords = (-1, -1)

        legalMoves = board.getLegalMoves(self.diskColor)
        if len(legalMoves) == 0:
            legalMoves.append([-1, -1])

        board.legalMovesSum += len(legalMoves) # used for heuristics u2, u4
        for child in legalMoves:
            newBoard = board.getCopy()
            newBoard.makeMove(child[0], child[1], self.diskColor)
            currValue = self.minValue(newBoard, depth + 1, a, b)

            #  b-Pruning
            if currValue >= b: 
                self.optCoords = maxCoords
                return currValue

            if currValue >= currMax:
                if currValue == currMax and random.uniform() <= 0.5:
                    continue
                maxCoords = child
                currMax = currValue
            a = max(a, currValue)
        
        self.optCoords = maxCoords
        return currMax

    def minValue(self, board, depth, a, b):
        if board.isTerminal() or depth == self.maxDepth:
            return u(board, self.diskColor, self.weights)

        currMin = float('inf')
        minCoords = (-1, -1)

        legalMoves = board.getLegalMoves(1 - self.diskColor)
        if len(legalMoves) == 0:
            legalMoves.append([-1, -1])

        board.opponentLegalMovesSum += len(legalMoves)  # used for heuristics u2, u4
        board.opponentTimesPlayed += 1  # used for heuristic u4 to derive upper bound for total legal moves.

        for child in legalMoves:
            newBoard = board.getCopy()
            newBoard.makeMove(child[0], child[1], 1 - self.diskColor)
            currValue = self.maxValue(newBoard, depth + 1, a, b)

            # a-Pruning
            if currValue <= a: 
                self.optCoords = minCoords 
                return currValue

            if currValue <= currMin:
                if currValue == currMin and random.uniform() <= 0.5:
                    continue
                minCoords = child
                currMin = currValue
            b = min(b, currValue)

        self.optCoords = minCoords
        return currMin