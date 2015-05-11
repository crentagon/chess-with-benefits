import os

class Constants:
	
	# The base directory is two folders up
	BASE_DIR = os.path.join( os.path.dirname( __file__ ), '../../' )

	# Fonts
	FONT = "fonts/DisposableDroidBB_bld.ttf"

	# Board information
	SCREENSIZE = [800, 500]

	# Sidebar: Avatars
	AVATAR_SIZE = 65
	AVATAR_BORDER_WIDTH = 4
	NAME_WIDTH = 65
	NAME_HEIGHT = 15
	NAME_BUFFER = 33

	# Colors
	HP_GOOD = (46, 204, 50)
	HP_FAIR = (230, 126, 34)
	HP_POOR = (192, 57, 43)
	HP_BG = (114, 114, 114)

	# Main menu
	BG = (225, 225, 225)
	SINGLE_PLAYER_BUTTON = (200, 28, 28)
	SINGLE_PLAYER_BUTTON_DK = (180, 28, 28)
	TWO_PLAYER_BUTTON = (28, 28, 200)
	TWO_PLAYER_BUTTON_DK = (28, 28, 180)
	BG_CAPTURED = (1, 48, 56)

	# Single-player
	CPU_LEVEL_BG = (32,32,32)
	LEVEL_COLORS = {
		0: (80,80,220),
		1: (0,191,232),
		2: (23,206,45),
		3: (213,181,3),
		4: (227,89,5),
		5: (227,5,5)
	}

	PLAY_AS_WHITE_BG = (250,250,250)
	PLAY_AS_BLACK_BG = (32,32,32)
	PLAY_AS_RANDOM_BG = (100,100,100)

	PLAY_AS_WHITE_TEXT = (16,16,16)
	PLAY_AS_BLACK_TEXT = (250,250,250)
	PLAY_AS_RANDOM_TEXT = (250,250,250)
	
	WHITE = (255, 255, 255)
	BLACK = (  0,   0,   0)
	RED =   (255,   0,   0)
	BLUE =  (  0,   0, 255)
	JUST_MOVED = (128, 128, 128)
	CURR_MOVEMENT = (180, 120, 255)

	# Two player
	WAIT_COLOR = {
		0: (128,128,128),
		1: (148,148,148),
		2: (168,168,168),
		3: (148,148,148)
	}

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