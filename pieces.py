
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

	def get_threat_level(self):
		return self.threat_level

	def get_piece_type(self):
		return self.piece_type

	def get_is_user(self):
		return self.is_user

	def get_is_white(self):
		return self.is_white

	def set_threat_level(self, threat_level):
		self.threat_level = threat_level

	def set_piece_type(self, piece_type):
		self.piece_type = piece_type

class Tile:

	def __init__(self, piece = None, threat_level = 0):
		self.piece = piece
		self.threat_level = 0
	
	def get_piece(self):
		return self.piece

	def get_threat_level(self):
		return self.threat_level

	def set_piece(self, piece):
		self.piece = piece

	def set_threat_level(self, threat_level):
		self.threat_level = threat_level

class Constants:

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
	CHESSBOARD_BG = (128, 128, 128)
	CHESSBOARD_DK = (200, 200, 200)
	CHESSBOARD_WH = (240, 240, 240)
	WHITE = (255, 255, 255)

	# Others
	RESOURCES = "res/"
	BOARD_BUFFER = 10
	RED =   (255,   0,   0)
	BLUE =  (  0,   0, 255)
