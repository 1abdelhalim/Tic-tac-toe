import sys
import copy
import pygame
import random
import numpy as np

from constants import *

# PyGame Setup:
pygame.init()
pygame.display.set_caption("Tic Tac Toe") # Window Title Bar
screen = pygame.display.set_mode( (WIDTH, HEIGHT) )

class Board:
    
    def __init__(self):
        self.squares = np.zeros( (ROWS, COLS) )
        self.empty_sqrs = self.squares
        self.marked_sqrs = 0

    def finalState(self, show=False):
        # return 0 if game not over & no winner
        # return 1 if player 1 won
        # return 2 if player 2 won
    

        # vertical:
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                if show: # Draw a line through the winner
                    color = CIRC_COLOR if self.squares[0][col] == 2 else X_COLOR
                    initPos = (col * SQSIZE + SQSIZE // 2, 20)
                    finPos = (col * SQSIZE + SQSIZE // 2, HEIGHT - 20)
                    pygame.draw.line(screen, color, initPos, finPos, LINE_WIDTH)
                return self.squares[0][col] # return which player won

        # horizontal wins:
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    color = CIRC_COLOR if self.squares[row][0] == 2 else X_COLOR
                    initPos = (20, row * SQSIZE + SQSIZE // 2)
                    finPos = (WIDTH - 20, row * SQSIZE + SQSIZE // 2)
                    pygame.draw.line(screen, color, initPos, finPos, LINE_WIDTH)
                return self.squares[row][0] # return player number of winner

        # descending diagonal win:

        """The show parameter is used to determine whether to draw a line on the Pygame screen
         to highlight the winning diagonal. If show is True, the code draws a line from the top-left corner
          (initPos) to the bottom-right corner (finPos) of the screen.
           The color of the line depends on the player who won (CIRC_COLOR for player 2
            and X_COLOR for player 1).
             The LINE_WIDTH constant is used to set the width of the line."""

        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show:
                    color = CIRC_COLOR if self.squares[row][0] == 2 else X_COLOR
                    initPos = (20, 20)
                    finPos = (WIDTH - 20, HEIGHT - 20)
                    pygame.draw.line(screen, color, initPos, finPos, LINE_WIDTH)
            return self.squares[1][1] # return player number who won

        # ascending diagonal win:
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            if show:
                    color = CIRC_COLOR if self.squares[row][0] == 2 else X_COLOR
                    initPos = (20, HEIGHT - 20)
                    finPos = (WIDTH - 20, 20)
                    pygame.draw.line(screen, color, initPos, finPos, LINE_WIDTH)
            return self.squares[1][1] # return player number who won

        # when there is no winner yet AND game not finished: return 0
        return 0

    def markSquare(self, row, col, player):
        self.squares[row][col] = player
        self.marked_sqrs += 1

    def emptySquare(self, row, col):
        return self.squares[row][col] == 0

    def getEmptySquares(self): # Returns a list of all unmarked squares
        unmarked = []
        for row in range(ROWS):
            for col in range(COLS):
                if (self.emptySquare(row, col)):
                    unmarked.append( (row, col) )
        return unmarked

    def isFull(self):
        return self.marked_sqrs == 9

    def isEmpty(self):
        return self.marked_sqrs == 0

class Game:
    def __init__(self):
        self.board = Board()
        self.ai = AI() # An instance of the AI class represents the AI player.
        self.player = 1 # Player 1: 'X', Player 2: 'O'
        self.gameMode = 'ai' #'pvp' = player vs player, 'ai' = AI player 2
        self.running = True
        self.showLines() # Pygame funciton to draw the game board lines

    def makeMove(self, row, col):
        self.board.markSquare(row, col, self.player)
        self.drawFigure(row, col)
        self.nextTurn()

    def showLines(self):
        screen.fill( BG_COLOR ) # Background Color Fill

        # Draw Vertical lines
        pygame.draw.line(screen, LINE_COLOR, (SQSIZE, 0), (SQSIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (WIDTH - SQSIZE, 0), (WIDTH - SQSIZE, HEIGHT), LINE_WIDTH)

        # Draw Horizontal lines
        pygame.draw.line(screen, LINE_COLOR, (0, SQSIZE), (WIDTH, SQSIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT - SQSIZE), (WIDTH, HEIGHT - SQSIZE), LINE_WIDTH)
    
    def drawFigure(self, row, col):
        if self.player == 1:
            # Draw X
            # Descending Line:
            start_desc = (col * SQSIZE + OFFSET, row * SQSIZE + OFFSET)
            end_desc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            pygame.draw.line(screen, X_COLOR, start_desc, end_desc, X_WIDTH)
            # Ascending Line:
            start_asc = (col * SQSIZE + OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            end_asc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + OFFSET)
            pygame.draw.line(screen, X_COLOR, start_asc, end_asc, X_WIDTH)

        elif self.player == 2:
            # Draw 'O'
            center = (col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2) # Create center position
            pygame.draw.circle(screen, CIRC_COLOR, center, RADIUS, CIRC_WIDTH)
        
    def nextTurn(self):
        self.player = self.player % 2 + 1 

    def changeGameMode(self):
        if self.gameMode == 'pvp':
            self.gameMode = 'ai'
        else:
            self.gameMode = 'pvp'
        print(f'Game Mode = {self.gameMode}')

    def isOver(self): # true if game is finished with a winner or a tie game
        return self.board.finalState(show=True) != 0 or self.board.isFull()

    def reset(self):
        self.__init__() # restart all attributes to default
        print('Game Reset Initiated')


class AI:
    def __init__(self, level=1, player=2):
        self.level = level # level 0 = random, level 1 = Minimax AI
        self.player = player # AI player is always player 2

    # Random Algo:
    def random(self, board):
        empty_squares = board.getEmptySquares()
        index = random.randrange(0, len(empty_squares))

        return empty_squares[index] # random (row, col)

    # Minimax AI Algo:
    def minimax(self, board, maximizing):
        # board = current board state
        # maximizing = boolean value to determine if AI is maximizing or minimizing
        # create  a temporary copy of the game board, marks the square with Player 1's symbol (X), and evaluates the next move using the minimax algorithm.
        # terminal case:
        case = board.finalState() # state is an integer 0 - 2

        # Player 1 Wins:
        if case == 1:
            return 1, None # return the evaluation & next move

        # Player 2 Wins (This is the AI player)
        if case == 2:
            return -1, None # (-1 value since AI is minimizing)

        # Board Full / Tie Game
        elif board.isFull():
            return 0, None

        if maximizing: # AI Player
            max_eval = -100
            best_move = None
            empty_squares = board.getEmptySquares() # Get list of (row, col) tuples
            for (row, col) in empty_squares:
                temp_board = copy.deepcopy(board) # copy current board for next move evaluation
                temp_board.markSquare(row, col, 1)
                eval = self.minimax(temp_board, False)[0] # [0] = only return 1st value (eval)
          
                if (eval > max_eval):
                    max_eval = eval
                    best_move = (row, col)
            return max_eval, best_move

        elif not maximizing: # Player 1
            min_eval = 100
            best_move = None
            empty_squares = board.getEmptySquares() # Get list of (row, col) tuples

            for (row, col) in empty_squares:
                temp_board = copy.deepcopy(board) # copy current board for next move evaluation
                temp_board.markSquare(row, col, self.player)
                eval = self.minimax(temp_board, True)[0] # [0] = only return 1st value (eval)
                if (eval < min_eval):
                    min_eval = eval
                    best_move = (row, col)

            return min_eval, best_move

    # Minimax Eval Function:
    def eval(self, main_board):
        if self.level == 0:
            # random choice
            eval = 'random'
            move = self.random(main_board)
        else:
            # minimax algo
            eval, move = self.minimax(main_board, False) # False: AI will minimize
        print(f'AI has chosen to mark square: {move} with eval of: {eval}')
        return move # (row, col)

def main():
    
    game = Game() #  an instance of the Game class
    board = game.board # for simplicity
    ai = game.ai


    # main loop until quit or reset
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Keyboard Events:
            if event.type == pygame.KEYDOWN:
                # 0 key: change to Random AI logic
                if event.key == pygame.K_0:
                    ai.level = 0
                    print('Random AI Opponent Selected')

                # 1 key: change to Minimaxs AI logic
                if event.key == pygame.K_1:
                    ai.level = 1
                    print('Smart AI Opponent Selected')
                
                # g key: change game mode: AI or 2 player human
                if event.key == pygame.K_g:
                    game.changeGameMode()
                
                # r key: reset game
                if event.key == pygame.K_r:
                    game.reset()
                    board = game.board
                    ai = game.ai
        
            if event.type == pygame.MOUSEBUTTONDOWN:
                position = event.pos
                row = position[1] // SQSIZE
                col = position[0] // SQSIZE

                if (board.emptySquare(row, col)) and game.running:
                    game.makeMove(row, col)

                    if game.isOver():
                        game.running = False

        if game.gameMode == 'ai' and game.player == ai.player and game.running:
            pygame.display.update()
            row, col = ai.eval(board)
            game.makeMove(row, col)
            print(board.squares) 

            if game.isOver():
                boardFull = board.isFull()
                if (boardFull):
                    print('TIE GAME')
                winner = board.finalState()
                if (winner == 1):
                    print('X (Player 1) WINS!')
                elif (winner == 2):
                    print('O (Player 2) WINS!')
                game.running = False
        
        pygame.display.update()

main()