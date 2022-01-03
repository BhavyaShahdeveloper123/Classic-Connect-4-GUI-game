import numpy as np
import pygame
import sys
import math
sizeofsquare=100
RADIUS = int(sizeofsquare/2 - 5)
BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)


ROW_COUNT = 6
COLUMN_COUNT = 7

# create a matrix/dataframe using numpy
def create_board():
	board = np.zeros((ROW_COUNT,COLUMN_COUNT))
	return board

def drop_piece(board, row, col, piece):
	board[row][col] = piece

def is_valid_location(board, col):
	return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
	for r in range(ROW_COUNT):
		if board[r][col] == 0:
			return r

def firstboard(board):
	print(np.flip(board, 0))

def winning_move(board, piece):
	# Check horizontal locations for winner
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT):
			if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
				return True

	# Check vertical locations  for winner
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
				return True

	# Check positively sloped diaganols for winner
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
				return True

	# Check negatively sloped diaganols for winner
	for c in range(COLUMN_COUNT-3):
		for r in range(3, ROW_COUNT):
			if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
				return True
# use pygame.draw.rect to make a rectangle
#use pygame.circle.rect to make a circle
def finalboard(board):
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):
                    #drawing the blue rectangle
			pygame.draw.rect(screen, BLUE, (c*100, r*100+100, 100, 100))
			# drawing the black circles for the actual chips to fill in
			pygame.draw.circle(screen, BLACK, (int(c*100+100/2), int(r*100+100+100/2)), int(100/2 - 5))
	
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):
                    #drawing the red circles that will be used in the game
			if board[r][c] == 1:
				pygame.draw.circle(screen, RED, (int(c*100+100/2), height-int(r*100+100/2)), int(100/2 - 5))
			elif board[r][c] == 2:
                            #drawing the yellow circles that will be used in the game
				pygame.draw.circle(screen, YELLOW, (int(c*100+100/2), height-int(r*100+100/2)), int(100/2 - 5))
	pygame.display.update()


board = create_board()
firstboard(board)
end = False
turn = 0

#initializing pygame
pygame.init()


#width of the board
width = COLUMN_COUNT * 100
#getting one more row count to account for circle to move
height = (ROW_COUNT+1) * 100

size = (width, height)


# displaying the board using pygame
screen = pygame.display.set_mode(size)
finalboard(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

while True:
# sucessfully quitting the game when the game is over 
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.MOUSEMOTION:
			pygame.draw.rect(screen, BLACK, (0,0, width, 100))
			posx = event.pos[0]
			if turn == 0:
				pygame.draw.circle(screen, RED, (posx, int(100/2)), int(100/2 - 5))
			else: 
				pygame.draw.circle(screen, YELLOW, (posx, int(100/2)), int(100/2 - 5))
		pygame.display.update()
# makes a move when the button is clicked 
		if event.type == pygame.MOUSEBUTTONDOWN:
			pygame.draw.rect(screen, BLACK, (0,0, width, 100))
			# Player 1 move and getting the respective positions and making sure it is functioning
			if turn == 0:
				posx = event.pos[0]
				#using math library, and dividing the position by 100 to get the values from 0-7 instead of 0-700
				col = int(math.floor(posx/100))

				if is_valid_location(board, col):
					row = get_next_open_row(board, col)
					drop_piece(board, row, col, 1)

					if winning_move(board, 1):
						label = myfont.render("Player 1 wins!! Better Luck next time player 2", 1, RED)
						screen.blit(label, (40,10))
						end = True


			# Player 2 move
			else:				
				posx = event.pos[0]
				col = int(math.floor(posx/100))

				if is_valid_location(board, col):
					row = get_next_open_row(board, col)
					drop_piece(board, row, col, 2)

					if winning_move(board, 2):
						label = myfont.render("Player 2 wins!! Better Luck next time player 1", 1, YELLOW)
						screen.blit(label, (40,10))
						end = True

			firstboard(board)
			finalboard(board)

			turn += 1
			turn = turn % 2

			if end:#pauses the game for 5000 miliseconds to make it functional normally
				pygame.time.wait(5000)

