import pygame
from math import *

class board:

    def __init__(self, size):
        self.board =   [['', '', '', '', '', '', '', ''],
                        ['', '', '', '', '', '', '', ''],
                        ['', '', '', '', '', '', '', ''],
                        ['', '', '', 'white', 'black', '', '', ''],
                        ['', '', '', 'black', 'white', '', '', ''],
                        ['', '', '', '', '', '', '', ''],
                        ['', '', '', '', '', '', '', ''],
                        ['', '', '', '', '', '', '', '']]
        self.size = size

    #displays the board
    def display(self, screen, width, height, turn):

        if turn == 'black':
            colour = (12, 3, 11) #black lines
        elif turn == 'white':
            colour = (232, 233, 235) # white lines

        colour = (68, 112, 82) # light green

        THICKNESS = 2
        BUFFER = 10
        RADIUS = floor(width/(2*self.size) - BUFFER)
        white = (248, 247, 255)
        black = (4, 3, 3)

        #draw grid lines
        for iter in range(1,self.size):
            pygame.draw.line(screen, colour, ((iter*width/self.size), 0), ((iter*width/self.size), height), THICKNESS)
            pygame.draw.line(screen, colour, (0, (iter*height/self.size)), (width, (iter*height/self.size)), THICKNESS)

        for row in range(self.size):
            for column in range(self.size):
                if self.board[row][column]:
                    x = row + 1
                    y = column + 1
                    centre = (floor(x*(width/self.size)-(width/(2*self.size))), floor(y*(height/self.size)-(width/(2*self.size))))

                    if self.board[row][column] == 'white':
                        pygame.draw.circle(screen, white, centre, RADIUS)
                    elif self.board[row][column] == 'black':
                        pygame.draw.circle(screen, black, centre, RADIUS)


    #places a piece at the specified row and column
    def place(self, row, column, piece):
        self.board[row][column] = piece


    #returns a list of all available moves
    def findAvailable(self, piece):
        available = []
        for row in range(self.size):
            for column in range(self.size):
                if self.isValidMove(row, column, piece):
                    available.append((row, column))
        return available

    #returns a list of pieces to be flipped if the move is valid,
    #and returns false otherwise
    def isValidMove(self, row, column, piece):

        #if space is already filled or off the game board, it's invalid
        if (self.board[row][column] != '' or not self.isOnBoard(row, column)):
            return False

        #set piece on board temporarily
        self.place(row, column, piece)

        if piece == 'white':
            otherPiece = 'black'
        else:
            otherPiece = 'white'

        piecesToFlip = []
        #iterate through all possible directions
        for xdir, ydir in [(0,1), (1,1), (1,0), (1,-1), (0,-1), (-1,-1), (-1,0), (-1,1)]:
            x, y = row, column
            x += xdir
            y += ydir
            if self.isOnBoard(x, y) and self.board[x][y]==otherPiece:
                #there is an opponent's piece next to our piece, so we can keep moving
                x += xdir
                y += ydir
                if not self.isOnBoard(x, y):
                    continue
                while self.board[x][y]==otherPiece:
                    x += xdir
                    y += ydir
                    if not self.isOnBoard(x, y):
                        break
                if not self.isOnBoard(x,y):
                    continue
                if self.board[x][y]==piece:
                    #there are pieces to flip over,
                    #move backwards and log location of pieces
                    while True:
                        x -= xdir
                        y -= ydir
                        if x==row and y==column:
                            break
                        piecesToFlip.append((x, y))

        #undo the temporary placement
        self.board[row][column] = ''
        if len(piecesToFlip) == 0:
            #if no pieces were flipped, it is an invalid move
            return False
        return piecesToFlip


    #returns true if the row and column given are on the game board
    def isOnBoard(self, row, column):
        return (row>=0 and row<self.size and column>=0 and column<self.size)


    #returns true if the board is full
    def isFull(self):
        for row in range(self.size):
            for column in range(self.size):
                if self.board[row][column] == '':
                    return False
        return True


    #returns scores of each player
    def findWinner(self):
        human = 0
        computer = 0
        for row in range(self.size):
            for column in range(self.size):
                if self.board[row][column] == 'black':
                    human += 1
                elif self.board[row][column] == 'white':
                    computer += 1

        return (human, computer)


    #returns a computer move, trying to maximise the number of counters
    def computerMove(self):

        #chose move that will give the biggest score but take a corner if
        #one is available
        bestScore = -inf
        availableMoves = self.findAvailable('white')
        for (x, y) in availableMoves:

            if self.isOnCorner(x, y):
                return (x, y)

            #place all pieces
            piecesToFlip = self.isValidMove(x, y, 'white')
            self.place(x, y, 'white')
            for (row, column) in piecesToFlip:
                self.place(row, column, 'white')

            #calculate score
            score = self.getScore('white')

            #undo placements
            self.place(x, y, '')
            for (row, column) in piecesToFlip:
                self.place(row, column, 'black')

            if score > bestScore:
                bestScore = score
                (i, j) = (x, y)

        return (i, j)


    #returns true if the index is on a corner
    def isOnCorner(self, row, column):
        return ((row,column)==(0,0) or (row,column)==(0,self.size-1) or
            (row,column)==(self.size-1,0) or (row,column)==(self.size-1,self.size-1))


    #returns the score of the board by totalling the number of pieces for one side
    def getScore(self, piece):
        score = 0
        for row in range(self.size):
            for column in range(self.size):
                if self.board[row][column] == piece:
                    score += 1
        return score


    def minimaxMove(self):

        bestScore = -inf
        availableMoves = self.findAvailable('white')
        for (x, y) in availableMoves:

            if self.isOnCorner(x, y):
                return (x, y)

            #place all pieces
            piecesToFlip = self.isValidMove(x, y, 'white')
            self.place(x, y, 'white')
            for (row, column) in piecesToFlip:
                self.place(row, column, 'white')

            #calculate score
            alpha = -inf
            beta = inf
            score = self.minimax(0, 'black', alpha, beta)

            #undo placements
            self.place(x, y, '')
            for (row, column) in piecesToFlip:
                self.place(row, column, 'black')

            if score > bestScore:
                bestScore = score
                (i, j) = (x, y)

        return (i, j)


    def minimax(self, depth, turn, alpha, beta):

        availableMoves = self.findAvailable(turn)

        #difficulty level
        if (depth > 3 or availableMoves == []):
            return self.score()

        #computers turn to maximise
        if turn == 'white':
            bestScore = -inf
            for (x, y) in availableMoves:

                #place all pieces
                piecesToFlip = self.isValidMove(x, y, 'white')
                self.place(x, y, 'white')
                for (row, column) in piecesToFlip:
                    self.place(row, column, 'white')

                #calculate score
                score = self.minimax(depth+1, 'black', alpha, beta)

                #undo placements
                self.place(x, y, '')
                for (row, column) in piecesToFlip:
                    self.place(row, column, 'black')

                alpha = max(alpha, score)
                if alpha >= beta:
                    break

                bestScore = max(score, bestScore)

        else:
            bestScore = inf
            for (x, y) in availableMoves:

                #place all pieces
                piecesToFlip = self.isValidMove(x, y, 'black')
                self.place(x, y, 'black')
                for (row, column) in piecesToFlip:
                    self.place(row, column, 'black')

                #calculate score
                score = self.minimax(depth+1, 'white', alpha, beta)

                #undo placements
                self.place(x, y, '')
                for (row, column) in piecesToFlip:
                    self.place(row, column, 'white')

                beta = min(beta, score)
                if beta <= alpha:
                    break

                bestScore = min(score, bestScore)

        return bestScore


    def score(self):

        whiteScore = 0
        blackScore = 0

        for row in range(self.size):
            for column in range(self.size):
                if self.board[row][column] == 'white':
                    whiteScore += 1
                elif self.board[row][column] == 'black':
                    blackScore += 1

        score = whiteScore - blackScore
        return score
