class PossibleMoves:
    def __init__(self):
        # Used to see a current move is valid
        self.hasMoves = False
        # The column range that will be changed
        # If it's (-1, -1) it means that the current move doesn't attack horizontally
        self.columnRange = (-1, -1)
        # The row range that will be changed
        # If it's (-1, -1) it means that the current move doesn't attack vertically 
        self.rowRange = (-1, -1)
        # The diagonal (that goes from the lower left corner to the right upper corner) that will be changed
        # diagonal[0] are the coordinates of the left lower corner and [1] the coordinates of the right upper corner
        # If it's [(-1, -1), (-1, -1)] it means that the current move doesn't attack this diagonal
        self.leftGoingUp = [(-1, -1)] * 2
        # The diagonal (that goes from the upper left corner to the right lower corner) that will be changed
        # diagonal[0] are the coordinates of the left upper corner and [1] the coordinates of the right lower corner
        # If it's [(-1, -1), (-1, -1)] it means that the current move doesn't attack this diagonal
        self.leftGoingDown = [(-1, -1)] * 2
    
    # Update the horizontal move
    def addHorizontal(self, newColumnRange):
        # If we can attack horizontally
        if newColumnRange != -1:
            # We can make at least one move
            self.hasMoves = True
            self.columnRange = newColumnRange

    # Update the vertical move
    def addVertical(self, newRowRange):
        # If we can attack vertically
        if newRowRange != -1:
            # We can make at least one move
            self.hasMoves = True
            self.rowRange = newRowRange

    # Update the 2 diagonals
    def addDiagonals(self, diagonals):
        # diagonals[0] = left lower corner to right upper corner
        # diagonals[1] = left upper corner to right lower corner
        # If we can attack at least one diagonal we can make at least one move
        if diagonals[0] != -1 or diagonals[1] != -1:
            self.hasMoves = True 

        if diagonals[0] != -1: self.leftGoingUp = diagonals[0] 
        if diagonals[1] != -1: self.leftGoingDown = diagonals[1] 


class Board:
    def __init__(self):
        # -1 = Empty spot, 0 = white, 1 = black
        self.board = [[-1 for _ in range(8)] for k in range(8)]
        # update the board to always be in its initial state
        self.board[3][3] = 0
        self.board[3][4] = 1
        self.board[4][3] = 1
        self.board[4][4] = 0
        # Used for the utility function to compare the colors of the root board state
        # with the colors of the max depth board state
        self.initialColors = [2, 2]

        # initialColors[0]([1]) = the number of white (black) disks
        self.colors = [2, 2]

        # total legal moves
        self.legalMovesSum = 0

        # total legal moves of the opponent
        self.opponentLegalMovesSum = 0
        self.opponentTimesPlayed = 0

    # Returns true if the whole board is filled
    def full(self):
        return self.colors[0] + self.colors[1] == 64

    def printBoard(self):
        resString = '  '
        symbols = {-1: "   ", 1: ' B ', 0: ' W '}
        print("  ",end='')
        for i in range(8):
            print(f"  {i} ", end='')
            resString += f'  {i} '
        resString += '\n'
        print()
        t = "―" * 35

        for i in range(len(self.board)):
            print(t)
            resString += f'{t}\n'
            s = ''
            for c in self.board[i]:
                s += '|' + symbols[c]
            resString += str(i) + ' ' + s + '|\n'
            print(str(i) + " " + s + '|')
        resString += f'{t}\n'
        resString += f'{self.colors}\n\n\n'
        print(t)
        print(self.colors)
        return resString

    # Returns true if a player can make at least one move
    def hasLegalMove(self, player):
        # Get all the coords that are empty
        emptySquares = self.getChildren()
        for square in emptySquares:
            # Get all possible moves if we place a disk at the current square
            possibleMoves = self.findMoves(square[0], square[1], player)
            if possibleMoves.hasMoves: return True

        return False
        
    # Check the moves that can be done if we place a disk at row, col 
    def findMoves(self, row, col, diskColor):
        possibleMoves = PossibleMoves()
        # The coords are either out of bounds or placed in a non empty spot
        if row >= 8 or col >= 8 or row < 0 or col < 0 or self.board[row][col] != -1: return possibleMoves

        # Check if we can attack horizontally
        possibleMoves.addHorizontal(self.outflankHorizontally(row, col, diskColor))
        # Check if we can attack vertically
        possibleMoves.addVertical(self.outflankVertically(row, col, diskColor))
        # Check if we can attack either of the two diagonals
        possibleMoves.addDiagonals(self.outflankDiagonally(row, col, diskColor))

        return possibleMoves
    
    # Update the board if we place a disk at row, col
    def makeMove(self, row, col, diskColor):
        possibleMoves = self.findMoves(row, col, diskColor)
        # If the current player doesn't have any moves then continue
        if not possibleMoves.hasMoves:
            return False

        columnRange = possibleMoves.columnRange
        rowRange = possibleMoves.rowRange
        leftGoingUp = possibleMoves.leftGoingUp
        leftGoingDown = possibleMoves.leftGoingDown
        
        # Place the disk
        self.board[row][col] = diskColor
        self.colors[diskColor] += 1

        # If we can attack horizontally then we will enter the for
        for currCol in range(columnRange[0] + 1, columnRange[1]):
            # reverse the color
            self.board[row][currCol] = diskColor
            # update the number of the disks on the board
            self.colors[diskColor] += 1
            self.colors[1-diskColor] -= 1
        
        # If we can attack vertically then we will enter the for
        for currRow in range(rowRange[0] + 1, rowRange[1]):
            # reverse the color
            self.board[currRow][col] = diskColor
            # update the number of the disks on the board
            self.colors[diskColor] += 1
            self.colors[1-diskColor] -= 1
            

        # If we can attack this diagonal then we will enter the for
        i = 0
        while leftGoingUp[0][1] + i < leftGoingUp[1][1]:
            # We go from left to right so the col number increases
            # We go from down to up so the row number decreases
            self.board[leftGoingUp[0][0] - i][leftGoingUp[0][1] + i] = diskColor
            if i > 0: 
                self.colors[diskColor] += 1
                self.colors[1-diskColor] -= 1
            i += 1

        # If we can attack this diagonal then we will enter the for
        i = 0
        while leftGoingDown[0][1] + i < leftGoingDown[1][1]:
            # We go from left to right so the col number increases
            # We go from up to down so the row number increases
            self.board[leftGoingDown[0][0] + i][leftGoingDown[0][1] + i] = diskColor
            if i > 0: 
                self.colors[diskColor] += 1
                self.colors[1-diskColor] -= 1
            i += 1

        return True

    def outflankHorizontally(self, row, col, diskColor):
        _, leftCol = self.move(row, col, 0, -1, diskColor)
        _, rightCol = self.move(row, col, 0, 1, diskColor)

        if leftCol == rightCol == -1: return -1

        if leftCol == -1: leftCol = col
        
        if rightCol == -1: rightCol = col
        
        return (leftCol, rightCol)

    def outflankVertically(self, row, col, diskColor):
        upRow, _ = self.move(row, col, -1, 0, diskColor)
        downRow, _ = self.move(row, col, 1, 0, diskColor)

        if upRow == downRow == -1: return -1

        if upRow == -1: upRow = row

        if downRow == -1: downRow = row

        return (upRow, downRow)

    def outflankDiagonally(self, row, col, diskColor):
        leftUp = self.move(row, col, -1, -1, diskColor)
        leftDown = self.move(row, col, 1, -1, diskColor)
        rightUp = self.move(row, col, -1, 1, diskColor)
        rightDown = self.move(row, col, 1, 1, diskColor)
 
        leftGoingUp = self.makeDiagonal(row, col, leftDown, rightUp)
        leftGoingDown = self.makeDiagonal(row, col, leftUp, rightDown)
        return leftGoingUp, leftGoingDown

    def makeDiagonal(self, row, col, leftCorner, rightCorner):
        if leftCorner == [-1, -1] and rightCorner == [-1, -1]: return -1

        if leftCorner != [-1, -1]:
            if rightCorner != [-1, -1]:
                return [leftCorner, rightCorner]
            return [leftCorner, (row, col)]
        else:
            return [(row, col), rightCorner]

    def move(self, startRow, startCol, stepRow, stepCol, diskColor):
        currCol = startCol + stepCol
        currRow = startRow + stepRow

        if currCol < 0 or currRow < 0: return [-1, -1]

        while 0 <= currCol < 8 and 0 <= currRow < 8:
            if self.board[currRow][currCol] == diskColor:
                break

            if self.board[currRow][currCol] == -1: return [-1, -1]
            currCol += stepCol
            currRow += stepRow

        if (currCol < 0 or currCol > 7 or currRow < 0 or currRow > 7) or (currCol == startCol + stepCol and currRow == startRow + stepRow):
            return [-1, -1]

        return [currRow, currCol]

    def isTerminal(self):
        return (not self.hasLegalMove(0) and not self.hasLegalMove(1)) or self.colors[0] == 0 or self.colors[1] == 0 or sum(self.colors) == 64

    def getChildren(self):
        children = []
        for r in range(len(self.board)):
            for c in range(len(self.board[0])):
                if self.board[r][c] == -1:
                    children.append([r, c])
        return children

    def getCopy(self):
        newBoard = Board()
        newBoard.board = [[value for value in row] for row in self.board] 
        newBoard.colors = [color for color in self.colors]
        newBoard.initialColors = [color for color in self.initialColors]
        newBoard.legalMovesSum = self.legalMovesSum
        newBoard.opponentLegalMovesSum = self.opponentLegalMovesSum

        return newBoard

    def getLegalMoves(self, diskColor):
        legalMoves = []
        for ch in self.getChildren():
            if self.findMoves(ch[0], ch[1], diskColor).hasMoves:
                legalMoves.append(ch)

        return legalMoves