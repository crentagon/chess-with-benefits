import sys, string, os
import math
import pygame
import Buttons
import time
from subprocess import *

'''
# Communication test
p = Popen( ["stockfish_14053109_32bit.exe"], stdin=PIPE, stdout=PIPE )
p.stdin.write("position fen rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2\n")
p.stdin.write("go movetime 1000\n")
time.sleep(1)
p.stdin.write("quit\n")

# Retrieving the best move
x = p.stdout.read().split("\n")
print x[-2]
'''
# Constants
# Board constants
nA = 0
nB = 1
nC = 2
nD = 3
nE = 4
nF = 5
nG = 6
nH = 7

n1 = 0
n2 = 1
n3 = 2
n4 = 3
n5 = 4
n6 = 5
n7 = 6
n8 = 7

bPAWN = -1
bROOK = -5
bKNIGHT = -3
bBISHOP = -4
bQUEEN = -9
bKING = -10

wPAWN = 1
wROOK = 5
wKNIGHT = 3
wBISHOP = 4
wQUEEN = 9
wKING = 10

# Board information
OuterBoardWidth = 500
OuterBoardHeight = 500
InnerBoardWidth = 480
InnerBoardHeight = 480
TileLength = InnerBoardHeight/8

# Colors
WHITE = (255, 255, 255)
BLACK = (  0,   0,   0)
CHESSBOARD_BG = ( 62,  24, 114)
# CHESSBOARD_DK = (184, 153, 227)
# CHESSBOARD_WH = (227, 206, 255)
CHESSBOARD_DK = (225, 225, 225)
CHESSBOARD_WH = (255, 255, 255)

BLUE =  (  0,   0, 255)
GREEN = (  0, 200,   0)
VIOLET = (100,  0, 200)
RED =   (255,   0,   0)

# Pygame initialization
pygame.init()
pygame.display.set_caption("Chesselate")
clock = pygame.time.Clock()
screenSize = [800, 500]

screen = pygame.display.set_mode(screenSize)
screen.fill(WHITE)
pygame.display.flip()


# Board Initializations
board = [[100 for i in range(8)] for i in range(8)] 

for i in range(8):
	board[i][n7] = -1
	board[i][n2] = 1

board[nA][n8] = bROOK
board[nB][n8] = bKNIGHT
board[nC][n8] = bBISHOP
board[nD][n8] = bQUEEN
board[nE][n8] = bKING
board[nF][n8] = bBISHOP
board[nG][n8] = bKNIGHT
board[nH][n8] = bROOK

board[nA][n1] = wROOK
board[nB][n1] = wKNIGHT
board[nC][n1] = wBISHOP
board[nD][n1] = wQUEEN
board[nE][n1] = wKING
board[nF][n1] = wBISHOP
board[nG][n1] = wKNIGHT
board[nH][n1] = wROOK

# Tile threats
for i in range(8):
	for j in range(8):
		if(board[i][7-j] == wPAWN):
			if(i < 7 and 7-j < 7 and board[i+1][7-j+1] > 20):
				board[i+1][7-j+1] += 1
			if(i > 0 and 7-j < 7 and board[i-1][7-j+1] > 20):
				board[i-1][7-j+1] += 1

		elif(abs(board[i][7-j]) == wKNIGHT):
			if(i > 0 and 7-j < 6 and board[i-1][7-j+2] > 20):
				board[i-1][7-j+2] += board[i][7-j]*1.0/abs(board[i][7-j])
			if(i > 0 and 7-j > 1 and board[i-1][7-j-2] > 20):
				board[i-1][7-j-2] += board[i][7-j]*1.0/abs(board[i][7-j])
				
			if(i < 7 and 7-j < 6 and board[i+1][7-j+2] > 20):
				board[i+1][7-j+2] += board[i][7-j]*1.0/abs(board[i][7-j])
			if(i < 7 and 7-j > 1 and board[i+1][7-j-2] > 20):
				board[i+1][7-j-2] += board[i][7-j]*1.0/abs(board[i][7-j])

			if(i > 1 and 7-j < 7 and board[i-2][7-j+1] > 20):
				board[i-2][7-j+1] += board[i][7-j]*1.0/abs(board[i][7-j])
			if(i > 1 and 7-j > 0 and board[i-2][7-j-1] > 20):
				board[i-2][7-j-1] += board[i][7-j]*1.0/abs(board[i][7-j])

			if(i < 6 and 7-j < 7 and board[i+2][7-j+1] > 20):
				board[i+2][7-j+1] += board[i][7-j]*1.0/abs(board[i][7-j])
			if(i < 6 and 7-j > 0 and board[i+2][7-j-1] > 20):
				board[i+2][7-j-1] += board[i][7-j]*1.0/abs(board[i][7-j])

		elif(abs(board[i][7-j]) == wBISHOP):
			dirNE = True
			dirNW = True
			dirSE = True
			dirSW = True
			for k in range(1, 8):
				if(i+k <= 7 and 7-j+k <= 7 and board[i+k][7-j+k] > 20 and dirNE):
					board[i+k][7-j+k] += board[i][7-j]*1.0/abs(board[i][7-j])
				else:
					dirNE = False

				if(i+k <= 7 and 7-j-k >= 0 and board[i+k][7-j-k] > 20 and dirNW):
					board[i+k][7-j-k] += board[i][7-j]*1.0/abs(board[i][7-j])
				else:
					dirNW = False
				
				if(i-k >= 0 and 7-j+k <= 7 and board[i-k][7-j+k] > 20 and dirSE):
					board[i-k][7-j+k] += board[i][7-j]*1.0/abs(board[i][7-j])
				else:
					dirSE = False
				
				if(i-k >= 0 and 7-j-k >= 0 and board[i-k][7-j-k] > 20 and dirSW):
					board[i-k][7-j-k] += board[i][7-j]*1.0/abs(board[i][7-j])
				else:
					dirSW = False

		elif(abs(board[i][7-j]) == wROOK):
			dirN = True
			dirS = True
			dirE = True
			dirW = True
			for k in range(1, 8):
				if(i+k <= 7 and board[i+k][7-j] > 20 and dirN):
					board[i+k][7-j] += board[i][7-j]*1.0/abs(board[i][7-j])
				else:
					dirN = False

				if(i-k >= 0 and board[i-k][7-j] > 20 and dirS):
					board[i-k][7-j] += board[i][7-j]*1.0/abs(board[i][7-j])
				else:
					dirS = False
				
				if(7-j+k <= 7 and board[i][7-j+k] > 20 and dirE):
					print "A"
					board[i][7-j+k] += board[i][7-j]*1.0/abs(board[i][7-j])
				else:
					print "B"
					dirE = False
				
				# MARKER
				if(7-j-k >= 0 and board[i][7-j-k] > 20 and dirW):
					board[i][7-j-k] += board[i][7-j]*1.0/abs(board[i][7-j])
				else:
					dirW = False

		elif(abs(board[i][7-j]) == wQUEEN):
			dirNE = True
			dirNW = True
			dirSE = True
			dirSW = True
			for k in range(1, 8):
				if(i+k <= 7 and 7-j+k <= 7 and board[i+k][7-j+k] > 20 and dirNE):
					board[i+k][7-j+k] += board[i][7-j]*1.0/abs(board[i][7-j])
				else:
					dirNE = False

				if(i+k <= 7 and 7-j-k >= 0 and board[i+k][7-j-k] > 20 and dirNW):
					board[i+k][7-j-k] += board[i][7-j]*1.0/abs(board[i][7-j])
				else:
					dirNW = False
				
				if(i-k >= 0 and 7-j+k <= 7 and board[i-k][7-j+k] > 20 and dirSE):
					board[i-k][7-j+k] += board[i][7-j]*1.0/abs(board[i][7-j])
				else:
					dirSE = False
				
				if(i-k >= 0 and 7-j-k >= 0 and board[i-k][7-j-k] > 20 and dirSW):
					board[i-k][7-j-k] += board[i][7-j]*1.0/abs(board[i][7-j])
				else:
					dirSW = False
			dirN = True
			dirS = True
			dirE = True
			dirW = True
			for k in range(1, 8):
				if(i+k <= 7 and board[i+k][7-j] > 20 and dirN):
					board[i+k][7-j] += board[i][7-j]*1.0/abs(board[i][7-j])
				else:
					dirN = False

				if(i-k >= 0 and board[i-k][7-j] > 20 and dirS):
					board[i-k][7-j] += board[i][7-j]*1.0/abs(board[i][7-j])
				else:
					dirS = False
				
				if(7-j+k <= 7 and board[i][7-j+k] > 20 and dirE):
					board[i][7-j+k] += board[i][7-j]*1.0/abs(board[i][7-j])
				else:
					dirE = False
				
				if(7-j-k >= 0 and board[i][7-j-k] > 20 and dirW):
					board[i][7-j-k] += board[i][7-j]*1.0/abs(board[i][7-j])
				else:
					dirW = False
		elif(abs(board[i][7-j]) == wKING):
			if(i+1 <= 7 and 7-j+1 <= 7 and board[i+1][7-j+1] > 20):
				board[i+1][7-j+1] += board[i][7-j]*1.0/abs(board[i][7-j])
			if(7-j+1 <= 7 and board[i][7-j+1] > 20):
				board[i][7-j+1] += board[i][7-j]*1.0/abs(board[i][7-j])
			if(i-1 >= 0 and 7-j+1 <= 7 and board[i-1][7-j+1] > 20):
				board[i-1][7-j+1] += board[i][7-j]*1.0/abs(board[i][7-j])

			if(i+1 <= 7 and board[i+1][7-j] > 20):
				board[i+1][7-j] += board[i][7-j]*1.0/abs(board[i][7-j])
			if(i-1 >= 0 and board[i-1][7-j] > 20):
				board[i-1][7-j] += board[i][7-j]*1.0/abs(board[i][7-j])

			if(i+1 <= 7 and 7-j-1 >= 0 and board[i+1][7-j-1] > 20):
				board[i+1][7-j-1] += board[i][7-j]*1.0/abs(board[i][7-j])
			if(7-j-1 >= 0 and board[i+1][7-j-1] > 20):
				board[i][7-j-1] += board[i][7-j]*1.0/abs(board[i][7-j])
			if(i-1 and 7-j-1 >= 0 and board[i+1][7-j-1] > 20):
				board[i-1][7-j-1] += board[i][7-j]*1.0/abs(board[i][7-j])

		if(board[i][7-j] == bPAWN):	
			if(i < 7 and 7-j > 0 and board[i+1][7-j-1] > 20):
				board[i+1][7-j-1] -= 1
			if(i > 0 and 7-j > 0 and board[i-1][7-j-1] > 20):
				board[i-1][7-j-1] -= 1

for i in range(8):
	print board[i]

while True:
	# Refresh rate
	clock.tick(10)
	screen.fill(WHITE)

	events = pygame.event.get()
	for event in events: 
		if event.type == pygame.QUIT: 
			sys.exit(0)
		else: 
			print event

	# Rendering
	# Render the board
	pygame.draw.rect(screen, CHESSBOARD_BG, (0, 0, OuterBoardWidth, OuterBoardHeight), 0)
	pygame.draw.rect(screen, WHITE, (10, 10, InnerBoardWidth, InnerBoardHeight), 0)

	for i in range(8):
		if(i % 2 == 0):
			leadingColor = CHESSBOARD_WH
			laggingColor = CHESSBOARD_DK
		else:
			leadingColor = CHESSBOARD_DK
			laggingColor = CHESSBOARD_WH
		for j in range(8):
			if(j % 2 == 0):
				pygame.draw.rect(screen, leadingColor, (10+60*i, 10+60*j, TileLength, TileLength), 0)
			else:
				pygame.draw.rect(screen, laggingColor, (10+60*i, 10+60*j, TileLength, TileLength), 0)

	# Render the pieces, it must come from the databoard
	for i in range(8):
		for j in range(8):
			pieceRect = (10+TileLength*i, 10+TileLength*j, TileLength, TileLength)
			if(board[i][7-j] <= 20):
				isThreatened = False

				if(board[i][7-j] > 10):
					board[i][7-j] -= 10
					isThreatened = True

				if(board[i][7-j] == wPAWN):
					imageFile = "wpawn.png"
				elif(board[i][7-j] == wKNIGHT):
					imageFile = "wknight.png"
				elif(board[i][7-j] == wBISHOP):
					imageFile = "wbishop.png"
				elif(board[i][7-j] == wROOK):
					imageFile = "wrook.png"
				elif(board[i][7-j] == wQUEEN):
					imageFile = "wqueen.png"
				elif(board[i][7-j] == wKING):
					imageFile = "wking.png"

				elif(board[i][7-j] == bPAWN):
					imageFile = "bpawn.png"
				elif(board[i][7-j] == bKNIGHT):
					imageFile = "bknight.png"
				elif(board[i][7-j] == bBISHOP):
					imageFile = "bbishop.png"
				elif(board[i][7-j] == bROOK):
					imageFile = "brook.png"
				elif(board[i][7-j] == bQUEEN):
					imageFile = "bqueen.png"
				elif(board[i][7-j] == bKING):
					imageFile = "bking.png"

				if(isThreatened):
					board[i][7-j] += 10
					#add code for displaying threatened piece here

				imagePiece = pygame.image.load(imageFile)
				screen.blit(imagePiece, pieceRect)

			else:
				difference = 15

				alpha = board[i][7-j]-100
				s = pygame.Surface((TileLength-difference, TileLength-difference))
				s.set_alpha(255.0*abs(alpha)/10.0)

				if(alpha >= 0):
					s.fill(BLUE)
				else:
					s.fill(RED)

				screen.blit(s, (10+(difference/2)+TileLength*i, 10+(difference/2)+TileLength*j))



	# User makes a move

	# Convert the board into the fen format

	# AI makes a move

	# Do all of the above while the game hasn't ended

	# Refresh the display
	pygame.display.flip()
