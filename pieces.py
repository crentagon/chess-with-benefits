import threading
import os, sys
from subprocess import *

class Piece:

	#####################
	#    Piece Types    #
	# ----------------- #
	#	1 - Pawn		#
	#	3 - Knight		#
	#	4 - Bishop		#
	#	5 - Rook		#
	#	9 - Queen		#
	#	100 - King 		#
	#####################

	def __init__(self, piece_type, is_white = True, is_user = True):
		self.is_user = is_user
		self.is_white = is_white 
		self.piece_type = piece_type
		self.threat_level = 0
		self.piece_position = (0,0,0,0)
		self.is_moved = False

	def get_threat_level(self):
		return self.threat_level

	def get_piece_type(self):
		return self.piece_type

	def get_is_user(self):
		return self.is_user

	def get_is_white(self):
		return self.is_white

	def get_is_moved(self):
		return self.is_moved

	def get_piece_position(self):
		return self.piece_position

	def set_threat_level(self, threat_level):
		self.threat_level = threat_level

	def set_piece_type(self, piece_type):
		self.piece_type = piece_type

	def set_piece_position(self, rectangle):
		self.piece_position = rectangle

	def set_is_moved_true(self):
		self.is_moved = True

	def pressed(self, mouse):
		rect = self.piece_position
		if self.is_user:
			if mouse[0] > rect[0]:
				if mouse[1] > rect[1]:
					if mouse[0] < rect[0] + rect[2]:
						if mouse[1] < rect[1] + rect[3]:
							return True
						else: return False
					else: return False
				else: return False
			else: return False

class Tile:

	def __init__(self, piece = None, threat_level_user = 0, threat_level_opponent = 0):
		self.piece = piece
		self.threat_level_user = threat_level_user
		self.threat_level_opponent = threat_level_opponent
		self.is_traversable = False

	def get_piece(self):
		return self.piece

	def get_threat_level_user(self):
		return self.threat_level_user

	def get_threat_level_opponent(self):
		return self.threat_level_opponent

	def get_is_traversable(self):
		return self.is_traversable

	def set_piece(self, piece):
		self.piece = piece

	def set_threat_level_user(self, threat_level_user):
		self.threat_level_user = threat_level_user

	def set_threat_level_opponent(self, threat_level_opponent):
		self.threat_level_opponent = threat_level_opponent

	def set_is_traversable(self, is_traversable):
		self.is_traversable = is_traversable

	def remove_piece(self):
		self.piece = None

class StockfishThread(threading.Thread):

	def __init__(self, fen_string, process_time):

		super(StockfishThread, self).__init__()
		self.fen_string = fen_string
		self.process_time = process_time
		self.is_thread_done = False

		self.cpu_move = ''
		self.ponder = ''

	def run(self):

		p = Popen( ["stockfish_14053109_32bit.exe"], stdin=PIPE, stdout=PIPE)
		p.stdin.write("position fen "+self.fen_string+"\n")
		p.stdin.write("go movetime "+str(self.process_time)+"\n")

		while p.poll() is None:
			line = p.stdout.readline()
			if line[0] == 'b': break
			# print line,

		# Retrieving the best move
		line = line.split("\r")
		line = line[0].split(" ")

		self.cpu_move = line[1]
		self.ponder = line[3]
		self.is_thread_done = True

class Constants:

	PIECE_MAPPING = {
		'a': 0,
		'b': 1,
		'c': 2,
		'd': 3,
		'e': 4,
		'f': 5,
		'g': 6,
		'h': 7,
		'1': 0,
		'2': 1,
		'3': 2,
		'4': 3,
		'5': 4,
		'6': 5,
		'7': 6,
		'8': 7
	}

	CHAR_MAPPING = {
		0: 'a',
		1: 'b',
		2: 'c',
		3: 'd',
		4: 'e',
		5: 'f',
		6: 'g',
		7: 'h'
	}

	NUM_MAPPING = {
		0: '1',
		1: '2',
		2: '3',
		3: '4',
		4: '5',
		5: '6',
		6: '7',
		7: '8',
	}

	# Tile information
	TILE_A = 0
	TILE_B = 1
	TILE_C = 2
	TILE_D = 3
	TILE_E = 4
	TILE_F = 5
	TILE_G = 6
	TILE_H = 7
		
	TILE_1 = 0
	TILE_2 = 1
	TILE_3 = 2
	TILE_4 = 3
	TILE_5 = 4
	TILE_6 = 5
	TILE_7 = 6
	TILE_8 = 7

	# Piece information
	P_KING = 0
	P_PAWN = 1
	P_ROOK = 5
	P_QUEEN = 9
	P_KNIGHT = 3
	P_BISHOP = 4

	# Board information
	SCREENSIZE = [800, 500]
	OUTERBOARD_WIDTH = 500
	OUTERBOARD_HEIGHT = 500
	INNERBOARD_WIDTH = 480
	INNERBOARD_HEIGHT = 480
	TILE_LENGTH = INNERBOARD_HEIGHT/8

	# Colors
	TRAVERSABLE_BORDER = (10, 80, 100)
	TRAVERSABLE_SEMI = (100, 50, 255)
	TRAVERSABLE_COLOR = (120, 200, 240)
	TRAVERSABLE_MINI = (220, 200, 255)

	TRAVERSABLE_SEMIRADIUS = 8
	TRAVERSABLE_RADIUS = 5
	TRAVERSABLE_MINIRADIUS = 4
	
	CHESSBOARD_BG = (128, 128, 128)
	CHESSBOARD_DK = (200, 200, 200)
	CHESSBOARD_WH = (240, 240, 240)
	WHITE = (255, 255, 255)

	# Others
	RESOURCES = "res/"
	BOARD_BUFFER = 10
	RED =   (255,   0,   0)
	BLUE =  (  0,   0, 255)