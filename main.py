from player import Player
from board import Board
import os
from datetime import datetime


class GameLogger:
    def __init__(self):
        directoryName = 'games'
        if not os.path.exists(directoryName): os.mkdir(directoryName)
        now = datetime.now()
        fileName = now.strftime('%d%m%Y_%H%M%S')
        self.file = open(directoryName + '/' + fileName + '.txt', 'w')
    
    def log(self, output):
        self.file.write(output)
    
    def closeFile(self):
        self.file.close()


def main():
    board = Board()
    boardStr = board.printBoard()
    logger = GameLogger()
    logger.log(boardStr)

    player_color = ['White', 'Black']
    checkers = [30, 30]
    playsFirst = 1 if input('Do you want to play first (yes/no): ').lower() == 'yes' else 0
    logger.log('Human plays first\n' if playsFirst == 1 else 'Computer plays first\n')

    turn = 1
    maxDepth = int(input("Max Depth: "))
    logger.log(f'Max Depth = {maxDepth}\n')
    
    weights = (0.08966120524022124, 0.025300321514067744, 0.12755162091380792, 0.7574868523319032)
    player = Player(maxDepth, 1 - playsFirst, weights)
    logger.log(f'Weights used: {weights}\n')

    while checkers[0] + checkers[1] > 0:
        
        if board.hasLegalMove(turn):
            print(f"{player_color[turn]} plays!")
            logger.log(f'{player_color[turn]} plays\n')

            if turn == playsFirst:
                while True:
                    
                    # Input validation required
                    r = int(input("Input row: "))
                    c = int(input("Input col: "))

                    logger.log(f'Human made the move, row: {r}, col: {c}\n')
                    if not board.makeMove(r, c, turn):
                        continue
                    
                    break
            else:
                moveCoords = player.miniMax(board)
                logger.log(f'Computer made the move, row: {moveCoords[0]}, col: {moveCoords[1]}\n')
                board.makeMove(moveCoords[0], moveCoords[1], 1 - playsFirst)
                
            if checkers[turn] == 0:
                checkers[1-turn] -= 1
                checkers[turn] += 1
                checkers[turn] -= 1
        else:
            print(f"{player_color[turn]} loses his turn since there isn't any legal move for him.")
            logger.log(f'{player_color[turn]} loses his turn since there isn\'t any legal move for him.\n')
        
        boardStr = board.printBoard()
        logger.log(boardStr)
        if board.isTerminal(): break

        turn = 1 - turn

    if board.colors[0] > board.colors[1]:
        print('White player wins!')
        logger.log('White player wins!\n')
    elif board.colors[0] < board.colors[1]:
        print('Black player wins!')
        logger.log('Black player wins!\n')
    else:
        print('Draw!')
        logger.log('Draw!\n')

    logger.closeFile()         


main()