import pygame
import time

from board import *
from functions import *

#constants
WINDOW_SIZE = height, width = 800, 800
GREEN = (50, 100, 73)
GAME_SIZE = 8

screen = pygame.display.set_mode(WINDOW_SIZE)
screen.fill(GREEN)

run = True
playersTurn = True
human = 'black'
computer = 'white'

#initisalise game board
board = board(GAME_SIZE)
board.display(screen, width, height, human)


while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #display updated board
    pygame.display.flip()

    #check for finished game and find winner
    if (board.isFull() or (board.findAvailable(human) ==[] and board.findAvailable(computer) == [])):
        (playerScore, computerScore) = board.findWinner()
        if (playerScore == computerScore):
            print(f'The game is a tie, {playerScore} tiles each')
        elif (playerScore<computerScore):
            winner = 'computer'
            print(f'The winner is {winner}:\nPlayer: {playerScore}\nComputer: {computerScore}')
        else:
            winner = 'player'
            print(f'The winner is {winner}:\nPlayer: {playerScore}\nComputer: {computerScore}')

        time.sleep(5)
        run = False

    # PLAYERS TURN #
    if playersTurn:

        #if there are no available positions, forfeit turn
        if board.findAvailable(human) == []:
            playersTurn = False
            board.display(screen, width, height, computer)
            continue

        if pygame.mouse.get_pressed()[0]:

            #if a valid sqaure is clicked, place piece and flip surrounded pieces
            (row, column) = getIndex(width, GAME_SIZE)
            piecesToFlip = board.isValidMove(row, column, human)
            if piecesToFlip:
                board.place(row, column, human)
                for (row, column) in piecesToFlip:
                    board.place(row, column, human)
                playersTurn = False

                board.display(screen, width, height, computer)
                pygame.display.flip()
                continue


    # COMPUTERS TURN #
    elif not playersTurn:

        #if there are no available positions, forfeit turn
        if board.findAvailable(computer) == []:
            playersTurn = True
            board.display(screen, width, height, human)
            continue

        #pick highest scoring move
        (row, column) = board.minimaxMove()
        piecesToFlip = board.isValidMove(row, column, computer)

        #place/ flip pieces
        board.place(row, column, computer)
        for (row, column) in piecesToFlip:
            board.place(row, column, computer)
        playersTurn = True

        board.display(screen, width, height, human)
        continue
