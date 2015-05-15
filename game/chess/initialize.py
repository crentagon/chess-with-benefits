from tile import *
from stack import *
from constants import *
import pygame

def run(self, screen, is_player_white, is_two_player, cpu_level, img_user, img_opponent,
	name_user, name_opponent, fen_string, listener, speaker):

	# Move piece animations
	self.animate = True
	self.is_animating = False
	self.is_board_changed = False
	self.will_render_guides = True
	self.will_render_opponent_threat = True
	self.will_render_user_threat = True

	# Avatars and names
	self.image_file_user = "res/avatars/char-"+str(img_user)+".png"
	self.image_file_opp = "res/avatars/char-"+str(img_opponent)+".png"
	self.name_opp = name_opponent
	self.name_user = name_user

	# Captured pieces
	self.user_captured = Stack()
	self.opponent_captured = Stack()

	# Player color specifics
	self.is_player_white = is_player_white
	self.goal_rank = 7 if self.is_player_white else 0

	# Initialize the board and the stack
	self.board = [[Tile() for i in range(8)] for i in range(8)]
	self.stack = Stack()
	self.active_stack_index = 0
	self.currently_active_index = 0

	# HP bars
	self.user_hp_max = 40
	self.user_hp_current = 40
	self.user_hp_current_before = 40
	self.opponent_hp_max = 40
	self.opponent_hp_current = 40
	self.opponent_hp_current_before = 40

	# Important attributes for the FEN notation
	self.active_turn = 'w'
	self.kingside_white = 'K'
	self.kingside_black = 'k'
	self.queenside_white = 'Q'
	self.queenside_black = 'q'
	self.en_passant = '-'
	self.halfmove_clock = 0
	self.fullmove_clock = 1

	# Set up the board given the fen_string
	self.convert_fen_to_board(fen_string, True)

	# Game Window information
	self.clock = pygame.time.Clock()

	# Source move
	self.source_x = 0
	self.source_y = 0

	# Stockfish
	self.cpu_level = cpu_level

	# Board stuff
	self.is_board_clickable = True
	self.temp_board = [[Tile() for i in range(8)] for i in range(8)]
	self.currmove_source_x = 0
	self.currmove_source_y = 0
	self.currmove_destination_x = 0
	self.currmove_destination_y = 0
	self.last_source_x = 0
	self.last_source_y = 0
	self.last_destination_x = 0
	self.last_destination_y = 0
	self.converted_move = ''

	# Right panel buttons
	self.promotions = {}

	# Debug mode: Disables opponent's moves
	self.debug_mode = False

	# Board statuses:
	# 'in_game', 'stalemate', 'user_check', 'user_checkmate',
	# 'opponent_check', 'opponent_checkmate', '50_move_rule',
	# 'forfeit', 'promoting', 'review_game_endgame', 'review_game_midgame'
	self.board_status = 'in_game'
	self.endgame_status = '' # for review game's back button.

	# Two player inits
	self.is_two_player = is_two_player
	self.listener = listener
	self.speaker = speaker
	self.move_string = ''

	# Piece stats
	self.piece_stats = {}

	# Lists
	self.aftergame_options = []
	self.sidebar_buttons = []
	self.is_game_over = {}
	self.traversable = []
	self.buttons = []
	self.populate_lists()

	self.screen = screen
	pygame.display.flip()