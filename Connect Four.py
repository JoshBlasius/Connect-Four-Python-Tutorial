import numpy as np
import pygame
import sys


import math

blue = (0,0,255)
red = (255,0,0)
yellow = (255,255,0)
black = (0,0,0)
rowCount = 6
colCount = 7

def createBoard():
    board = np.zeros((rowCount,colCount))
    return board

def dropPiece(board, row, col, piece):
    board[row][col] = piece

def isValid(board, col):
    return board[rowCount-1][col] == 0

def getNextRow(board, col):
    for r in range(rowCount):
        if board[r][col] == 0:
            return r

def printBoard(board):
    print(np.flip(board,0))

def winningMove(board, piece):
    #Check horizontal locations for a win
    for c in range(colCount - 3):
        for r in range(rowCount):
            if board[r][c] == piece and board [r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    #Check vertical locations for a win
    for c in range(colCount):
        for r in range(rowCount - 3):
            if board[r][c] == piece and board [r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    #Check positive diaganol
    for c in range(colCount - 3):
        for r in range(rowCount - 3):
            if board[r][c] == piece and board [r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    #Check negative diaganol
    for c in range(colCount):
        for r in range(3, rowCount):
            if board[r][c] == piece and board [r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True


def drawBoard(board):
    for c in range(colCount):
        for r in range(rowCount):
            pygame.draw.rect(screen, blue, (c * squareSize, r * squareSize + squareSize, squareSize, squareSize))
            pygame.draw.circle(screen, black, (int(c * squareSize + squareSize / 2), int(r * squareSize + squareSize + squareSize / 2 )), radius)

    for c in range(colCount):
        for r in range(rowCount):
            if board[r][c] == 1:
                pygame.draw.circle(screen, red, (int(c * squareSize + squareSize / 2), screenHeight - (r * squareSize + squareSize / 2)), radius)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, yellow, (int(c * squareSize + squareSize / 2), screenHeight - int(r * squareSize + squareSize / 2)), radius)
    pygame.display.update()

board = createBoard()
printBoard(board)
gameOver = False
turn = 0

pygame.init()

squareSize = 100
screenWidth = colCount * squareSize
screenHeight = (rowCount + 1) * squareSize
screenSize = (screenWidth, screenHeight)
radius = int(squareSize / 2 - 5)

screen = pygame.display.set_mode(screenSize)
drawBoard(board)
pygame.display.update()

myFont = pygame.font.SysFont("monospace", 75)

while not gameOver:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, black, (0,0, screenWidth, squareSize))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, red, (posx, int(squareSize / 2)), radius)
            else:
                pygame.draw.circle(screen, yellow, (posx, int(squareSize / 2)), radius)
            pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, black, (0,0, screenWidth, squareSize))


            #Ask for player 1 input
            if turn == 0:
                posx = event.pos[0]
                col = int(math.floor(posx / squareSize))

                if isValid(board, col):
                    row = getNextRow(board, col)

                    dropPiece(board, row, col, 1)

                if winningMove(board, 1):
                    label = myFont.render("Player 1 wins!", 1, red)
                    screen.blit(label, (40,10))
                    print("Player 1 has won!")
                    gameOver = True


            # Ask for player 2 input
            else:
                posx = event.pos[0]
                col = int(math.floor(posx / squareSize))

                if isValid(board, col):
                    row = getNextRow(board, col)
                    dropPiece(board, row, col, 2)

                if winningMove(board, 2):
                    label = myFont.render("Player 2 wins!", 1, yellow)
                    screen.blit(label, (40,10))
                    print("Player 2 has won!")
                    gameOver = True

            printBoard(board)
            drawBoard(board)

    #Increment turn order after submissions
            turn += 1
            turn = turn % 2

            if gameOver:
                pygame.time.wait(3000)
