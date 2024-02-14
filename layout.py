import pygame
import sys
import numpy

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Checkers")

# Load images

# Define the board
board =numpy.zeros((8,8))
reds = [[0, 1], [0, 3], [0, 5], [0, 7],
        [1, 0], [1, 2], [1, 4], [1, 6],
        [2, 1], [2, 3], [2, 5], [2, 7]]

blues = [[5, 0], [5, 2], [5, 4], [5, 6],
         [6, 1], [6, 3], [6, 5], [6, 7],
         [7, 0], [7, 2], [7, 4], [7, 6]]

# Functions
def draw_board():
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col]==1:
                pygame.draw.rect(screen, GRAY, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            elif board[row][col]==2:
                pygame.draw.circle(screen, GRAY, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 5)
            elif (row+col)%2:
                pygame.draw.rect(screen, BLACK, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            else:
                pygame.draw.rect(screen, WHITE, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))



def draw_pieces():
    for row,col in reds:
        pygame.draw.circle(screen, RED, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 5)
    for row,col in blues:
        pygame.draw.circle(screen, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 5)

def draw():
    draw_board()
    draw_pieces()
    pygame.display.update()

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

active=False
isitblu=True
active_coin= None
# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:  # Left mouse button clicked
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                print("Clicked at:", row, col)  # Just for demonstration purposes, you can replace this with your logic
                if active:
                    if board[row][col]==2:
                        if isitblu:
                            blues=[x for x in blues if x !=active_coin]
                            blues.insert(0,[row,col])
                            if (row+active_coin[0])%2==0:
                                remove=[(row+active_coin[0])/2,(col+active_coin[1])/2]
                                reds=[x for x in reds if x !=remove]
                            isitblu=False
                        else:
                            reds=[x for x in reds if x !=active_coin]
                            reds.insert(0,[row,col])
                            if (row+active_coin[0])%2==0:
                                remove=[(row+active_coin[0])/2,(col+active_coin[1])/2]
                                blues=[x for x in blues if x !=remove]
                            isitblu=True
                    active=False
                    board =numpy.zeros((8,8))
                    draw()
                else:
                    board =numpy.zeros((8,8))
                    draw()
                    if [row,col] in reds and not isitblu:
                        active=True
                        active_coin=[row,col]
                        board[row][col]=1
                        legal_row=row+1
                        legal_col1=col-1
                        legal_col2=col+1
                        if legal_row<8:
                            if legal_col1>=0 and [legal_row,legal_col1] not in reds:
                                if [legal_row,legal_col1] not in blues:
                                    board[legal_row][legal_col1]=2
                                else:
                                    legal_row+=1
                                    legal_col1-=1
                                    if legal_row<8:
                                        if legal_col1>=0 and [legal_row,legal_col1] not in reds and [legal_row,legal_col1] not in blues:
                                            board[legal_row][legal_col1]=2
                                    legal_row-=1
                            
                            if legal_col2<8 and [legal_row,legal_col2] not in reds:
                                if [legal_row,legal_col2] not in blues:
                                    board[legal_row][legal_col2]=2
                                else:
                                    legal_row+=1
                                    legal_col2+=1
                                    if legal_row<8:
                                        if legal_col2<8 and [legal_row,legal_col2] not in reds and [legal_row,legal_col2] not in blues:
                                            board[legal_row][legal_col2]=2
                                    legal_row-=1

                    elif [row,col] in blues and isitblu:
                        active=True
                        active_coin=[row,col]
                        board[row][col]=1
                        legal_row=row-1
                        legal_col1=col-1
                        legal_col2=col+1
                        if legal_row>=0:
                            if legal_col1>=0 and [legal_row,legal_col1] not in blues:
                                if [legal_row,legal_col1] not in reds:
                                    board[legal_row][legal_col1]=2
                                else:
                                    legal_row-=1
                                    legal_col1-=1
                                    if legal_row>=0:
                                        if legal_col1>=0 and [legal_row,legal_col1] not in blues and [legal_row,legal_col1] not in reds:
                                            board[legal_row][legal_col1]=2
                                    legal_row+=1
                            if legal_col2<8 and [legal_row,legal_col2] not in blues:
                                if [legal_row,legal_col2] not in reds:
                                    board[legal_row][legal_col2]=2
                                else:
                                    legal_row-=1
                                    legal_col2+=1
                                    if legal_row>=0:
                                        if legal_col2<8 and [legal_row,legal_col2] not in blues and [legal_row,legal_col2] not in reds:
                                            board[legal_row][legal_col2]=2
                                    legal_row+=1

                        

    draw()
    

pygame.quit()
sys.exit()
