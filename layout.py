import pygame
import sys
import os
from math import inf
from BOARD import BOARD
import time

# Initialize Pygame
# Constants
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
DIM_ORANGE = (200, 112, 0)

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

board=BOARD()
    
def draw_board(table):
    for row in range(ROWS):
        for col in range(COLS):
            if table[row][col]==1:
                pygame.draw.rect(screen, GRAY, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            elif table[row][col]==2:
                pygame.draw.circle(screen, GRAY, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 5)
            elif table[row][col]==3:
                pygame.draw.circle(screen, DIM_ORANGE, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 5)
            elif (row+col)%2:
                pygame.draw.rect(screen, BLACK, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            else:
                pygame.draw.rect(screen, WHITE, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
def draw_pieces(red_coins,blue_coins):
    for row,col in red_coins:
        pygame.draw.circle(screen, RED, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 5)
    for row,col in blue_coins:
        pygame.draw.circle(screen, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 5)

def draw(table,red_coins,blue_coins):
    draw_board(table)
    draw_pieces(red_coins,blue_coins)
    pygame.display.update()
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Checkers")

active = False
active_coin = None
mandatory_jump=False

running = True
bot=False
if len(sys.argv) == 2:
    if sys.argv[1] == "bot":
        bot=True


while running:
    mandatory_jump = board.check()
    draw(board.table,board.red_coins,board.blue_coins)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:  # Left mouse button clicked

                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                if active:
                    if mandatory_jump and board.table[row][col]!=3:
                        continue
                    elif board.table[row][col] in [2, 3]:
                        board.move(active_coin, [row, col])
                        board.is_current_blue = not board.is_current_blue
                    board.reset()
                    active = not active
                    
                else:
                    board.reset()
                    
                    if [row, col] in board.red_coins and not board.is_current_blue:
                        active = not active
                        active_coin = [row, col]
                        board.table[row][col] = 1
                        board.table=board.update_legal_moves(row, col)

                    elif [row, col] in board.blue_coins and board.is_current_blue:
                        active = not active
                        active_coin = [row, col]
                        board.table[row][col] = 1
                        board.table=board.update_legal_moves( row, col)
                    else:
                        # this is a wrong move/misclick
                        pass
                draw(board.table,board.red_coins,board.blue_coins)

   
    if bot and not board.is_current_blue:
        max_val=-inf
        max_board=None
        draw(board.table,board.red_coins,board.blue_coins)
        print("drew")
        time.sleep(1)
        for i in board.get_next_moves():
            # print("see now")
            # draw(i.table,i.red_coins,i.blue_coins)
            # time.sleep(0.5)
            # print("reset")
            # draw(board.table,board.red_coins,board.blue_coins)
            # time.sleep(0.5)
            # print("done")
            x=i.alpha_beta(3, -inf, inf, False)
            #print(x)
            if x>max_val:
                max_val=x
                max_board=i
        if not max_board:
            print("robot loses")
            running=False
        else:
            #print("choosing:",max_val )
            time.sleep(1)
            board=max_board
            board.is_current_blue = not board.is_current_blue


pygame.quit()
sys.exit()

# MIN MAX with ALPHA-BETA pruning

