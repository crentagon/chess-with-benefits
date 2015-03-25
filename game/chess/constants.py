import os

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
	
	# The base directory is two folders up
	BASE_DIR = os.path.join( os.path.dirname( __file__ ), '../../' )

	# Fonts
	FONT = "fonts/DisposableDroidBB_bld.ttf"
	FONT_REG = "fonts/DisposableDroidBB_bld.ttf"
	FONT_HP = "fonts/DisposableDroidBB_bld.ttf"

	# Board information
	PROMOTION_COORD = (650, 125)
	SCREENSIZE = [800, 500]
	OUTERBOARD_WIDTH = 500
	OUTERBOARD_HEIGHT = 500
	INNERBOARD_WIDTH = 480
	INNERBOARD_HEIGHT = 480
	TILE_LENGTH = INNERBOARD_HEIGHT/8

	# Sidebar information
	SIDEBAR_WIDTH = 55
	SIDEBAR_BUTTON = 45
	SIDEBAR_BUTTON_ICON = 40

	# Sidebar: Captured pieces
	CAPTURED_WIDTH = 153
	CAPTURED_HEIGHT = 150
	USER_CAPTURE_BUFFER = 330
	MINIBUFFER = 5
	CAPTURED_SIZE = 35
	CAPTURED_BUFFER = 1
	CAPTURED_BORDER = 4

	# Sidebar: HP	
	HP_CONTAINER_HEIGHT = 20
	HP_CONTAINER_WIDTH = 35
	HP_TEXT_BORDER = 5
	HP_TEXT_FONT_SIZE = 15
	HP_TEXT_BUFFER = 2
	HP_TEXT_CENTER_X = 19
	HP_TEXT_CENTER_Y = 10
	HP_BAR_BORDER = 4
	HP_BAR_WIDTH = 190
	HP_BAR_HEIGHT = 18

	# Sidebar: Avatars
	AVATAR_SIZE = 65
	AVATAR_BORDER_WIDTH = 4
	NAME_WIDTH = 65
	NAME_HEIGHT = 15
	NAME_BUFFER = 33

	# Colors
	TRAVERSABLE_BORDER = (10, 80, 100)
	TRAVERSABLE_SEMI = (100, 50, 255)
	TRAVERSABLE_COLOR = (120, 200, 240)
	TRAVERSABLE_MINI = (220, 200, 255)
	HP_GOOD = (46, 204, 50)
	HP_FAIR = (230, 126, 34)
	HP_POOR = (192, 57, 43)

	TRAVERSABLE_SEMIRADIUS = 8
	TRAVERSABLE_RADIUS = 5
	TRAVERSABLE_MINIRADIUS = 4
	
	CHESSBOARD_BG = (128, 128, 128)
	CHESSBOARD_DK = (200, 200, 200)
	CHESSBOARD_WH = (240, 240, 240)
	SIDEBAR_BG = (64, 64, 64)
	SIDEBAR_BUTTON_BG = (32, 32, 32)
	WHITE = (255, 255, 255)
	BLACK = (  0,   0,   0)
	BG = (96, 96, 96)
	RED =   (255,   0,   0)
	BLUE =  (  0,   0, 255)
	JUST_MOVED = (180, 120, 255)
	CURR_MOVEMENT = (100, 240, 140)

	# Aftergame stuff
	AFTERGAME_WIDTH = 200
	AFTERGAME_HEIGHT = 50
	AFTERGAME_COORD = (550, 150)

	# Others
	RESOURCES = BASE_DIR+"res/"
	BOARD_BUFFER = 10
	LAST_MOVEMENT_BORDER_THICKNESS = 4
	LAST_MOVEMENT_DECREASE_FACTOR = 0.95
	TILE_DIFFERENCE = 15
	THREAT_FONT_SIZE = 25
	ENDGAME_FONT_SIZE = 22
	GAMEOVER_FONT_SIZE = 22