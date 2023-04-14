import numpy as np
import pygame
import sys
import math
import random
ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARE_SIZE = 100
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
RADIUS = 45
PLAYER = 0
AI = 1


def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0


def get_next_open_row(board, col):
    for row in range(ROW_COUNT):
        if board[row][col] == 0:
            return row


def print_board(board):
    print(np.flip(board, 0))


def wining_move(board, piece):
    # Check horizontal direction
    for col in range(COLUMN_COUNT - 3):
        for row in range(ROW_COUNT):
            if board[row][col] == piece and board[row][col+1] == piece and board[row][col+2] == piece and board[row][col+3] == piece:
                return True

    # Check vertical direction
    for row in range(ROW_COUNT - 3):
        for col in range(COLUMN_COUNT):
            if board[row][col] == piece and board[row+1][col] == piece and board[row+2][col] == piece and board[row+3][col] == piece:
                return True

    # Check right dig direction
    for col in range(COLUMN_COUNT - 3):
        for row in range(ROW_COUNT - 3):
            if board[row][col] == piece and board[row+1][col+1] == piece and board[row+2][col+2] == piece and board[row+3][col+3] == piece:
                return True

    # Check left dig direction
    for row in range(ROW_COUNT - 1, ROW_COUNT - 4, - 1):
        for col in range(COLUMN_COUNT - 3):
            if board[row][col] == piece and board[row-1][col+1] == piece and board[row-2][col+2] == piece and board[row-3][col+3] == piece:
                return True

    return False


def draw_board(board):
    for col in range(COLUMN_COUNT):
        for row in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (col * SQUARE_SIZE, row *
                             SQUARE_SIZE + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            if board[row][col] == 0:
                pygame.draw.circle(screen, BLACK, (int(col * SQUARE_SIZE + SQUARE_SIZE/2), int(row *
                                                                                               SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE/2)), RADIUS)
            elif board[row][col] == 1:
                pygame.draw.circle(screen, RED, (int(col * SQUARE_SIZE + SQUARE_SIZE/2), int(
                    row * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE/2)), RADIUS)
            else:
                pygame.draw.circle(screen, GREEN, (int(col * SQUARE_SIZE + SQUARE_SIZE/2), int(
                    row * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE/2)), RADIUS)


board = create_board()
game_over = False
turn = 0

pygame.init()
font = pygame.font.SysFont("monospace", 75)
height = (ROW_COUNT + 1) * SQUARE_SIZE
width = COLUMN_COUNT * SQUARE_SIZE
size = (width, height)
screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(
                screen, BLACK, (0, 0, width, SQUARE_SIZE))
            posX = event.pos[0]
            if turn == PLAYER:
                pygame.draw.circle(
                    screen, RED, (posX, int(SQUARE_SIZE/2)), RADIUS)
            else:
                pygame.draw.circle(
                    screen, GREEN, (posX, int(SQUARE_SIZE/2)), RADIUS)

            pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            posX = event.pos[0]
            col = int(math.floor(posX/SQUARE_SIZE))
            if (is_valid_location(board, col)):
                row = get_next_open_row(board, col)
                if turn == PLAYER:
                    drop_piece(board, row, col, 1)
                    if wining_move(board, 1):
                        pygame.draw.rect(
                            screen, BLACK, (0, 0, width, SQUARE_SIZE))
                        label = font.render("Player  wins!!", 1, RED)
                        screen.blit(label, (40, 10))
                        game_over = True
                    turn += 1
                    turn %= 2
            print_board(board)
            draw_board(np.flip(board, 0))
            pygame.display.update()

    if turn == AI and not game_over:
        col = random.randrange(COLUMN_COUNT)
        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, 2)
            if wining_move(board, 2):
                pygame.draw.rect(
                    screen, BLACK, (0, 0, width, SQUARE_SIZE))
                label = font.render("AI wins!!", 1, GREEN)
                screen.blit(label, (40, 10))
                game_over = True
            turn += 1
            turn %= 2
        print_board(board)
        draw_board(np.flip(board, 0))
        pygame.display.update()

    if game_over:
        pygame.time.wait(3000)
