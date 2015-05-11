import os

class Constants:
	
	# The base directory is two folders up
	BASE_DIR = os.path.join( os.path.dirname( __file__ ), '../../' )

	# Fonts
	FONT = "fonts/DisposableDroidBB_bld.ttf"
	FONT_REG = "fonts/DisposableDroidBB_bld.ttf"
	FONT_HP = "fonts/DisposableDroidBB_bld.ttf"

	# Board information
	SCREENSIZE = [400, 400]

	# Main menu
	BG = (225, 225, 225)
	SINGLE_PLAYER_BUTTON = (200, 28, 28)
	SINGLE_PLAYER_BUTTON_DK = (180, 28, 28)
	
	WHITE = (255, 255, 255)
	BLACK = (  0,   0,   0)
	RED =   (255,   0,   0)
	BLUE =  (  0,   0, 255)

	# Others
	RESOURCES = BASE_DIR+"res/"