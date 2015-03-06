import sys, string, os, threading
import math
import pygame, copy
from pygame import gfxdraw
import time
from subprocess import *
from pieces import *

class Chesselate:

	def __init__(self, is_player_white = True, cpu_level = 2000, fen_string = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
		# Move piece animations
		self.animate = True

		# Avatars and names
		self.image_file_user = "res/avatars/dragonite_sample.png"
		self.image_file_opp = "res/avatars/stockfish_sample.png"
		self.name_opp = "Stockfish"
		self.name_user = "Dragonite"

		# Captured pieces
		self.user_captured = Stack()
		self.opponent_captured = Stack()

		# Player color specifics
		self.is_player_white = is_player_white
		self.goal_rank = 7 if self.is_player_white else 0

		# Initialize the board and the stack
		self.board = [[Tile() for i in range(8)] for i in range(8)]
		self.stack = Stack()

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
		self.is_undergoing_promotion = False
		self.halfmove_clock = 0
		self.fullmove_clock = 1

		# Set up the board given the fen_string
		self.convert_fen_to_board(fen_string, True)

		# Game Window information
		pygame.init()
		pygame.display.set_caption("Chess with Benefits")
		self.clock = pygame.time.Clock()

		# Source move
		self.source_x = 0
		self.source_y = 0

		# Stockfish
		self.cpu_level = cpu_level

		# Board stuff
		self.is_board_clickable = True
		self.temp_board = [[Tile() for i in range(8)] for i in range(8)]

		# Right panel buttons
		self.promotions = {}

		# Debug mode: Disables opponent's moves
		self.debug_mode = False

		# Sidebar buttons
		self.sidebar_buttons = []
		self.populate_sidebar()

		# Checks and checkmate
		self.is_user_check = False
		self.is_user_checkmate = False
		self.is_opponent_check = False
		self.is_opponent_checkmate = False

		self.screen = pygame.display.set_mode(Constants.SCREENSIZE)
		self.screen.fill(Constants.WHITE)
		pygame.display.flip()

	def populate_sidebar(self):
		self.sidebar_buttons.append(["sidebar_undo.png", "Undo Move", "undo"])
		self.sidebar_buttons.append(["sidebar_undo.png", "Undo Move2", "undo2"])

	def print_board(self):
		print "==piece_types=="
		for i in range(8):
			for j in range(8):
				if self.board[i][j].piece is not None:
					sys.stdout.write(str(self.board[i][j].piece.piece_type))
				else:
					sys.stdout.write("0")
			print ""

		print "==is_user=="
		for i in range(8):
			for j in range(8):
				if self.board[i][j].piece is not None:
					sys.stdout.write("A") if self.board[i][j].piece.is_user else sys.stdout.write("E")
				else:
					sys.stdout.write("0")
			print ""

		print "==colors=="
		for i in range(8):
			for j in range(8):
				if self.board[i][j].piece is not None:
					sys.stdout.write("W") if self.board[i][j].piece.is_white else sys.stdout.write("B")
				else:
					sys.stdout.write("0")
			print ""

	def is_check(self, board_input):
		self.build_threats(board_input, peek=True)

		for i in range(8):
			for j in range(8):
				tile = board_input[i][j]
				piece = tile.piece
				is_piece = piece is not None

				if is_piece and piece.is_user and piece.piece_type == Constants.P_KING:
					if tile.threat_level_opponent > 0:
						return True
					else:
						return False

	def build_threats(self, board_input, peek=False):
		# Clear threats
		for i in range(8):
			for j in range(8):
				board_input[i][j].threat_level_user = 0
				board_input[i][j].threat_level_opponent = 0

		# Build threats
		for i in range(8):
			for j in range(8):
				target_tiles = []
				tile = board_input[i][7-j]
				piece = tile.piece

				if(piece is not None):
					# This is to prevent the index-out-of-range errors
					is_i_lt_7 = i < 7
					is_i_lt_6 = i < 6
					is_7j_lt_7 = 7-j < 7
					is_7j_lt_6 = 7-j < 6

					is_i_gt_1 = i > 1
					is_i_gt_0 = i > 0
					is_7j_gt_1 = 7-j > 1
					is_7j_gt_0 = 7-j > 0

					is_user = piece.is_user
					piece_type = piece.piece_type

					if(piece_type == Constants.P_KNIGHT):
						if(is_i_gt_0):
							if(is_7j_lt_6):
								target_tile = board_input[i-1][7-j+2]
								target_tiles.append(target_tile)
							if(is_7j_gt_1):
								target_tile = board_input[i-1][7-j-2]
								target_tiles.append(target_tile)
							
						if(is_i_lt_7):
							if(is_7j_lt_6):
								target_tile = board_input[i+1][7-j+2]
								target_tiles.append(target_tile)
							if(is_7j_gt_1):
								target_tile = board_input[i+1][7-j-2]
								target_tiles.append(target_tile)

							
						if(is_i_gt_1):
							if(is_7j_lt_7):
								target_tile = board_input[i-2][7-j+1]
								target_tiles.append(target_tile)
							if(is_7j_gt_0):
								target_tile = board_input[i-2][7-j-1]
								target_tiles.append(target_tile)

						if(is_i_lt_6):
							if(is_7j_lt_7):
								target_tile = board_input[i+2][7-j+1]
								target_tiles.append(target_tile)
							if(is_7j_gt_0):
								target_tile = board_input[i+2][7-j-1]
								target_tiles.append(target_tile)

					elif(piece_type == Constants.P_BISHOP):
						dirNE = True
						dirSE = True
						dirNW = True
						dirSW = True
						for k in range(1, 8):
							is_ik_lte_7 = i+k <= 7
							is_ik_gte_0 = i-k >= 0
							if_7j_lte_7 = 7-j+k <= 7
							if_7j_gte_0 = 7-j-k >= 0

							if(is_ik_lte_7):
								if(if_7j_lte_7 and dirNE):
									target_tile = board_input[i+k][7-j+k]
									target_tiles.append(target_tile)
									if(target_tile.piece is not None):
										dirNE = False
								else:
									dirNE = False

								if(if_7j_gte_0 and dirSE):
									target_tile = board_input[i+k][7-j-k]
									target_tiles.append(target_tile)
									if(target_tile.piece is not None):
										dirSE = False
								else:
									dirSE = False

							if(is_ik_gte_0):
								if(if_7j_lte_7 and dirNW):
									target_tile = board_input[i-k][7-j+k]
									target_tiles.append(target_tile)
									if(target_tile.piece is not None):
										dirNW = False
								else:
									dirNW = False

								if(if_7j_gte_0 and dirSW):
									target_tile = board_input[i-k][7-j-k]
									target_tiles.append(target_tile)
									if(target_tile.piece is not None):
										dirSW = False
								else:
									dirSW = False

					elif(piece.piece_type == Constants.P_ROOK):
						dirN = True
						dirS = True
						dirE = True
						dirW = True
						for k in range(1, 8):
							is_ik_lte_7 = i+k <= 7
							is_ik_gte_0 = i-k >= 0
							if_7j_lte_7 = 7-j+k <= 7
							if_7j_gte_0 = 7-j-k >= 0

							if(is_ik_lte_7 and dirE):
								target_tile = board_input[i+k][7-j]
								target_tiles.append(target_tile)
								if(target_tile.piece is not None):
									dirE = False
							else:
								dirE = False

							if(is_ik_gte_0 and dirW):
								target_tile = board_input[i-k][7-j]
								target_tiles.append(target_tile)
								if(target_tile.piece is not None):
									dirW = False
							else:
								dirW = False

							if(if_7j_lte_7 and dirN):
								target_tile = board_input[i][7-j+k]
								target_tiles.append(target_tile)
								if(target_tile.piece is not None):
									dirN = False
							else:
								dirN = False

							if(if_7j_gte_0 and dirS):
								target_tile = board_input[i][7-j-k]
								target_tiles.append(target_tile)
								if(target_tile.piece is not None):
									dirS = False
							else:
								dirS = False

					elif(piece_type == Constants.P_QUEEN):
						dirN = True
						dirS = True
						dirE = True
						dirW = True
						dirNE = True
						dirSE = True
						dirNW = True
						dirSW = True
						for k in range(1, 8):
							is_ik_lte_7 = i+k <= 7
							is_ik_gte_0 = i-k >= 0
							if_7j_lte_7 = 7-j+k <= 7
							if_7j_gte_0 = 7-j-k >= 0

							if(is_ik_lte_7 and dirE):
								target_tile = board_input[i+k][7-j]
								target_tiles.append(target_tile)
								if(target_tile.piece is not None):
									dirE = False
							else:
								dirE = False

							if(is_ik_gte_0 and dirW):
								target_tile = board_input[i-k][7-j]
								target_tiles.append(target_tile)
								if(target_tile.piece is not None):
									dirW = False
							else:
								dirW = False

							if(if_7j_lte_7 and dirN):
								target_tile = board_input[i][7-j+k]
								target_tiles.append(target_tile)
								if(target_tile.piece is not None):
									dirN = False
							else:
								dirN = False

							if(if_7j_gte_0 and dirS):
								target_tile = board_input[i][7-j-k]
								target_tiles.append(target_tile)
								if(target_tile.piece is not None):
									dirS = False
							else:
								dirS = False

							if(is_ik_lte_7):
								if(if_7j_lte_7 and dirNE):
									target_tile = board_input[i+k][7-j+k]
									target_tiles.append(target_tile)
									if(target_tile.piece is not None):
										dirNE = False
								else:
									dirNE = False

								if(if_7j_gte_0 and dirSE):
									target_tile = board_input[i+k][7-j-k]
									target_tiles.append(target_tile)
									if(target_tile.piece is not None):
										dirSE = False
								else:
									dirSE = False

							if(is_ik_gte_0):
								if(if_7j_lte_7 and dirNW):
									target_tile = board_input[i-k][7-j+k]
									target_tiles.append(target_tile)
									if(target_tile.piece is not None):
										dirNW = False
								else:
									dirNW = False

								if(if_7j_gte_0 and dirSW):
									target_tile = board_input[i-k][7-j-k]
									target_tiles.append(target_tile)
									if(target_tile.piece is not None):
										dirSW = False
								else:
									dirSW = False

					# This also checks if the King is in checkmate MARKER
					elif(piece_type == Constants.P_KING):
						is_i_lte_7 = i+1 <= 7
						is_i_gte_0 = i-1 >= 0
						is_7j_lte_7 = 7-j+1 <= 7
						is_7j_gte_0 = 7-j-1 >= 0

						if(is_i_lte_7):
							target_tile = board_input[i+1][7-j]
							target_tiles.append(target_tile)

							if(is_7j_lte_7):
								target_tile = board_input[i+1][7-j+1]
								target_tiles.append(target_tile)
							
							if(is_7j_gte_0):
								target_tile = board_input[i+1][7-j-1]
								target_tiles.append(target_tile)
							
						if(is_i_gte_0):
							target_tile = board_input[i-1][7-j]
							target_tiles.append(target_tile)
							
							if(is_7j_lte_7):
								target_tile = board_input[i-1][7-j+1]
								target_tiles.append(target_tile)
							
							if(is_7j_gte_0):
								target_tile = board_input[i-1][7-j-1]
								target_tiles.append(target_tile)
							
						if(is_7j_lte_7):
							target_tile = board_input[i][7-j+1]
							target_tiles.append(target_tile)
						
						if(is_7j_gte_0):
							target_tile = board_input[i][7-j-1]
							target_tiles.append(target_tile)

					elif(piece_type == Constants.P_PAWN):
						is_white = piece.is_white
						factor = 1 if is_user else -1

						if is_white:
							if(is_i_lt_7 and is_7j_lt_7):
								target_tile = board_input[i+1][7-j+1]
								target_tiles.append(target_tile)

							if(is_i_gt_0 and is_7j_lt_7):
								target_tile = board_input[i-1][7-j+1]
								target_tiles.append(target_tile)

						else:
							if(is_i_lt_7 and is_7j_gt_0):
								target_tile = board_input[i+1][7-j-1]
								target_tiles.append(target_tile)

							if(is_i_gt_0 and is_7j_gt_0):
								target_tile = board_input[i-1][7-j-1]
								target_tiles.append(target_tile)

					is_user_king_detected = False
					is_opponent_king_detected = False

					if is_user:
						for element in target_tiles:
							element.threat_level_user += 1

							is_piece_none = element.piece is None
							if not is_piece_none and peek is False:
								is_piece_king = element.piece.piece_type == Constants.P_KING
								is_piece_opponent = element.piece.is_user is False

								if is_piece_king and is_piece_opponent:
									self.is_opponent_check = True
									is_opponent_king_detected = True

					else:
						for element in target_tiles:
							element.threat_level_opponent += 1

							is_piece_none = element.piece is None
							if not is_piece_none and peek is False:
								is_piece_king = element.piece.piece_type == Constants.P_KING
								is_piece_user = element.piece.is_user is True

								if is_piece_king and is_piece_user:
									self.is_user_check = True
									is_user_king_detected = True


	def render_captured(self, x, y, cmax, side, all_captured):
		i = 0
		j = 0
		for element in all_captured:
			rect_x = x + (Constants.CAPTURED_SIZE)*i
			rect_y = y + (Constants.CAPTURED_SIZE)*j
			piece_rect = (rect_x, rect_y, side, side)

			image_file = "mini_"+ element[0] + ".png"

			image_piece = pygame.image.load(Constants.RESOURCES+image_file)
			self.screen.blit(image_piece, piece_rect)

			j = j + 1 if i == cmax else j
			i = 0 if i == cmax else i+1

	def render_board(self):
		self.screen.fill(Constants.BG)
		font = Constants.RESOURCES+Constants.FONT
		font_reg = Constants.RESOURCES+Constants.FONT_REG

		# Render the board background
		rect_x = 0
		rect_y = 0
		rect_w = Constants.OUTERBOARD_WIDTH
		rect_h = Constants.OUTERBOARD_HEIGHT
		rect = (rect_x, rect_y, rect_w, rect_h)
		pygame.draw.rect(self.screen, Constants.CHESSBOARD_BG, rect, 0)
		
		# User is undergoing pawn promotion
		if self.is_undergoing_promotion:

			# Promotion button setup
			promotionable_pieces = [Constants.P_KNIGHT, Constants.P_BISHOP, Constants.P_ROOK, Constants.P_QUEEN]
			color = "w" if self.is_player_white else "b"
			size = Constants.TILE_LENGTH

			# Promotion button positioning
			for i in range(2):
				for j in range(2):
					rect_x = Constants.PROMOTION_COORD[0] + (i-1)*(Constants.TILE_LENGTH + Constants.BOARD_BUFFER)
					rect_y = Constants.BOARD_BUFFER*3 + Constants.PROMOTION_COORD[1] + (Constants.TILE_LENGTH + Constants.BOARD_BUFFER)*j
					rect_w = size
					rect_h = size
					rect = (rect_x, rect_y, rect_w, rect_h)
					image_file = color + str(promotionable_pieces[i*2+j]) + ".png"
					image_piece = pygame.image.load(Constants.RESOURCES+image_file)
					self.screen.blit(image_piece, rect)

					piece = Piece(promotionable_pieces[i*2+j], is_white=self.is_player_white, is_user = True)
					piece.piece_position = rect
					self.promotions[i*2+j] = piece

			# Promotion text
			char_text = "Select a piece to promote to:"
			basic_font = pygame.font.Font(font, 20)
			promotion_text = basic_font.render(char_text, True, Constants.WHITE)
			promotion_rect = promotion_text.get_rect()
			promotion_rect.center = Constants.PROMOTION_COORD
			self.screen.blit(promotion_text, promotion_rect)

		# If the user isn't undergoing promotion
		else:
			# Render the sidebar
			rect_x = Constants.SCREENSIZE[0] - Constants.SIDEBAR_WIDTH
			rect_y = 0
			rect_w = Constants.SIDEBAR_WIDTH
			rect_h = Constants.OUTERBOARD_HEIGHT
			rect = (rect_x, rect_y, rect_w, rect_h)
			pygame.draw.rect(self.screen, Constants.SIDEBAR_BG, rect, 0)

			# Render the sidebar buttons
			rect_x = ((Constants.SIDEBAR_WIDTH - Constants.SIDEBAR_BUTTON)/2) + (Constants.SCREENSIZE[0] - Constants.SIDEBAR_WIDTH)
			size = Constants.SIDEBAR_BUTTON
			i = 0

			for element in self.sidebar_buttons:
				image_file = element[0]
				image_text = element[1]
				image_icon = pygame.image.load(Constants.RESOURCES+image_file)

				# The button
				rect_y = Constants.BOARD_BUFFER + (size + Constants.BOARD_BUFFER)*i
				button_rect = (rect_x, rect_y, size, size)
				pygame.draw.rect(self.screen, Constants.SIDEBAR_BUTTON_BG, button_rect, 0)

				# The icon
				image_piece = pygame.image.load(Constants.RESOURCES+image_file)
				icon_rect = (rect_x, rect_y, size, size)
				self.screen.blit(image_piece, icon_rect)

				i+=1

			# Setup the HP bar
			hp_container_height = Constants.HP_CONTAINER_HEIGHT
			hp_container_width = Constants.HP_CONTAINER_WIDTH

			# Render the background of the captured pieces
			opp_y = Constants.BOARD_BUFFER + hp_container_height
			usr_y = Constants.BOARD_BUFFER + Constants.USER_CAPTURE_BUFFER
			cap_x = Constants.OUTERBOARD_WIDTH + Constants.BOARD_BUFFER
			buff = Constants.CAPTURED_BUFFER
			border = Constants.CAPTURED_BORDER
			cap_width = Constants.CAPTURED_WIDTH
			cap_height = Constants.CAPTURED_HEIGHT

			opp_rect = (cap_x + buff, opp_y, cap_width, cap_height)
			usr_rect = (cap_x + buff, usr_y, cap_width, cap_height)
			pygame.draw.rect(self.screen, Constants.SIDEBAR_BG, opp_rect, 0)
			pygame.draw.rect(self.screen, Constants.SIDEBAR_BUTTON_BG, opp_rect, border)
			pygame.draw.rect(self.screen, Constants.SIDEBAR_BG, usr_rect, 0)
			pygame.draw.rect(self.screen, Constants.SIDEBAR_BUTTON_BG, usr_rect, border)

			# Render captured pieces
			cur_max = 3
			cur_x = cap_x + Constants.MINIBUFFER
			side = Constants.CAPTURED_SIZE

			# Opponent's captured pieces
			cur_y = opp_y + Constants.MINIBUFFER
			self.render_captured(cur_x, cur_y, cur_max, side, self.opponent_captured.container)
			
			# User's captured pieces
			cur_y = usr_y + Constants.MINIBUFFER
			self.render_captured(cur_x, cur_y, cur_max, side, self.user_captured.container)

			# Render opponent checkmate
			if self.is_opponent_checkmate:
				rect_x = cap_x + buff
				rect_y = opp_y + Constants.MINIBUFFER
				rect_w = cap_width
				rect_h = int(rect_w*2.0/3.0)
				image_file = "checkmate.png"

				image_piece = pygame.image.load(Constants.RESOURCES+image_file)
				image_piece = pygame.transform.scale(image_piece, (rect_w,rect_h))
				piece_rect = image_piece.get_rect()
				piece_rect = piece_rect.move((rect_x, rect_y))
				self.screen.blit(image_piece, piece_rect)

			# Render opponent check
			elif self.is_opponent_check:
				rect_x = cap_x + buff
				rect_y = opp_y + Constants.MINIBUFFER
				rect_w = cap_width
				rect_h = int(rect_w*2.0/3.0)
				image_file = "check.png"

				image_piece = pygame.image.load(Constants.RESOURCES+image_file)
				image_piece = pygame.transform.scale(image_piece, (rect_w,rect_h))
				piece_rect = image_piece.get_rect()
				piece_rect = piece_rect.move((rect_x, rect_y))
				self.screen.blit(image_piece, piece_rect)

			# Render user checkmate
			if self.is_user_checkmate:
				rect_x = cap_x + buff
				rect_y = usr_y + Constants.MINIBUFFER
				rect_w = cap_width
				rect_h = int(rect_w*2.0/3.0)
				image_file = "checkmate.png"

				image_piece = pygame.image.load(Constants.RESOURCES+image_file)
				image_piece = pygame.transform.scale(image_piece, (rect_w,rect_h))
				piece_rect = image_piece.get_rect()
				piece_rect = piece_rect.move((rect_x, rect_y))
				self.screen.blit(image_piece, piece_rect)

			# Render user check
			elif self.is_user_check:
				rect_x = cap_x + buff
				rect_y = usr_y + Constants.MINIBUFFER
				rect_w = cap_width
				rect_h = int(rect_w*2.0/3.0)
				image_file = "check.png"

				image_piece = pygame.image.load(Constants.RESOURCES+image_file)
				image_piece = pygame.transform.scale(image_piece, (rect_w,rect_h))
				piece_rect = image_piece.get_rect()
				piece_rect = piece_rect.move((rect_x, rect_y))
				self.screen.blit(image_piece, piece_rect)

			# Render the HP text
			border = Constants.HP_TEXT_BORDER
			buff = Constants.HP_TEXT_BUFFER

			# Render the opponent's HP text board
			opp_y = Constants.BOARD_BUFFER
			hp_container_opponent_rect = (cap_x + buff, opp_y + buff, hp_container_width, hp_container_height - border)
			pygame.draw.rect(self.screen, Constants.SIDEBAR_BUTTON_BG, hp_container_opponent_rect, 0)
			pygame.draw.rect(self.screen, Constants.SIDEBAR_BUTTON_BG, hp_container_opponent_rect, border)
			
			# Render the user's HP text board
			usr_y = usr_y - hp_container_height
			hp_container_user_rect = (cap_x + buff, usr_y + buff, hp_container_width, hp_container_height - border)
			pygame.draw.rect(self.screen, Constants.SIDEBAR_BUTTON_BG, hp_container_user_rect, 0)
			pygame.draw.rect(self.screen, Constants.SIDEBAR_BUTTON_BG, hp_container_user_rect, border)

			# Render the text, "HP"
			font_hp = Constants.RESOURCES+Constants.FONT_HP
			basic_font = pygame.font.Font(font_hp, Constants.HP_TEXT_FONT_SIZE)
			hp_text = "HP"
			hp_text_render = basic_font.render(hp_text, True, Constants.CHESSBOARD_DK)
			hp_text_rect = hp_text_render.get_rect()

			# Render "HP" for the opponent
			hp_text_rect.centerx = cap_x + Constants.HP_TEXT_CENTER_X
			hp_text_rect.centery = opp_y + Constants.HP_TEXT_CENTER_Y
			self.screen.blit(hp_text_render, hp_text_rect)

			# Render "HP" for the user
			hp_text_rect.centery = usr_y + Constants.HP_TEXT_CENTER_Y
			self.screen.blit(hp_text_render, hp_text_rect)

			# Render the HP bar
			hp_border_width = Constants.HP_BAR_BORDER
			hp_bar_height = Constants.HP_BAR_HEIGHT - (hp_border_width/2)
			hp_bar_width = Constants.HP_BAR_WIDTH
			hp_bar_x = cap_x + hp_container_width
			hp_bar_y_opp = opp_y + (hp_border_width/2) -1
			hp_bar_y_user = usr_y + (hp_border_width/2) -1
			hp_current_user = self.user_hp_current 
			hp_current_user_before = self.user_hp_current_before
			hp_current_opponent = self.opponent_hp_current
			hp_current_opponent_before = self.opponent_hp_current_before

			# HP bar: percentage
			percentage_user = hp_current_user_before*1.0/self.user_hp_max
			percentage_opponent = hp_current_opponent_before*1.0/self.opponent_hp_max 

			# HP bar: color (user)
			hp_color_user = Constants.HP_GOOD
			if percentage_user <= 0.25:
				hp_color_user = Constants.HP_POOR
			elif percentage_user <= 0.5:
				hp_color_user = Constants.HP_FAIR

			# HP bar: color (opponent)
			hp_color_opp = Constants.HP_GOOD
			if percentage_opponent <= 0.25:
				hp_color_opp = Constants.HP_POOR
			elif percentage_opponent <= 0.5:
				hp_color_opp = Constants.HP_FAIR

			# HP while increasing/decreasing (user)
			if hp_current_user_before > hp_current_user:
				self.user_hp_current_before -= 1
				hp_color_user = Constants.WHITE
				self.alpha_hp_user = 255
			elif hp_current_user_before < hp_current_user:
				self.user_hp_current_before += 1
				hp_color_user = Constants.WHITE
				self.alpha_hp_user = 255

			# HP while increasing/decreasing (opponent)
			if hp_current_opponent_before > hp_current_opponent:
				self.opponent_hp_current_before -= 1
				hp_color_opp = Constants.WHITE
				self.alpha_hp_opponent = 255
			elif hp_current_opponent_before < hp_current_opponent:
				self.opponent_hp_current_before += 1
				hp_color_opp = Constants.WHITE
				self.alpha_hp_opponent = 255

			# HP bar rectangle configurations
			hp_user_rect = (hp_bar_x, hp_bar_y_user, hp_bar_width, hp_bar_height)
			hp_user_rect_curr = (hp_bar_x, hp_bar_y_user, hp_bar_width*percentage_user, hp_bar_height)
			hp_opponent_rect = (hp_bar_x, hp_bar_y_opp, hp_bar_width, hp_bar_height)
			hp_opponent_rect_curr = (hp_bar_x, hp_bar_y_opp, hp_bar_width*percentage_opponent, hp_bar_height)

			# Rendering the bars
			pygame.draw.rect(self.screen, hp_color_opp, hp_opponent_rect_curr, 0)
			pygame.draw.rect(self.screen, Constants.SIDEBAR_BUTTON_BG, hp_opponent_rect, hp_border_width)
			pygame.draw.rect(self.screen, hp_color_user, hp_user_rect_curr, 0)
			pygame.draw.rect(self.screen, Constants.SIDEBAR_BUTTON_BG, hp_user_rect, hp_border_width)

			# Rendering "32/40" for the HP
			hp_text_user = str(self.user_hp_current_before)+"/"+str(self.user_hp_max)
			hp_text_opponent = str(self.opponent_hp_current_before)+"/"+str(self.opponent_hp_max)

			font_size = Constants.HP_TEXT_FONT_SIZE
			basic_font = pygame.font.Font(font_hp, font_size)
			hp_user = basic_font.render(hp_text_user, True, Constants.SIDEBAR_BUTTON_BG)
			hp_opponent = basic_font.render(hp_text_opponent, True, Constants.SIDEBAR_BUTTON_BG)

			hp_text_x = hp_bar_x + hp_container_width - (font_size/2)
			hp_text_y_user = hp_bar_y_user + hp_container_height/2 -1
			hp_text_y_opp = hp_bar_y_opp + hp_container_height/2 -1

			hp_user_rect = hp_user.get_rect()
			hp_user_rect.centerx = hp_text_x
			hp_user_rect.centery = hp_text_y_user
			hp_opponent_rect = hp_opponent.get_rect()
			hp_opponent_rect.centerx = hp_text_x
			hp_opponent_rect.centery = hp_text_y_opp

			self.screen.blit(hp_user, hp_user_rect)
			self.screen.blit(hp_opponent, hp_opponent_rect)

			# Render the avatars
			avatar_size = Constants.AVATAR_SIZE
			avatar_border_width = Constants.AVATAR_BORDER_WIDTH
			avatar_x = cap_x + cap_width + avatar_border_width
			user_avatar_y = hp_bar_y_user + hp_bar_height + avatar_border_width
			opp_avatar_y = hp_bar_y_opp + hp_bar_height + avatar_border_width
			
			# Set up the rectangle of the avatars
			user_avatar_rect = (avatar_x, user_avatar_y, avatar_size, avatar_size)
			opp_avatar_rect = (avatar_x, opp_avatar_y, avatar_size, avatar_size)

			# Avatar rectangle borders
			opp_avatar_border_rect = (avatar_x - (avatar_border_width/2), opp_avatar_y - (avatar_border_width/2), avatar_size + avatar_border_width, avatar_size + avatar_border_width)
			user_avatar_border_rect = (avatar_x - (avatar_border_width/2), user_avatar_y - (avatar_border_width/2), avatar_size + avatar_border_width, avatar_size + avatar_border_width)

			# Avatar image files
			image_file_user = self.image_file_user
			image_file_opp = self.image_file_opp

			# Load both images and render them
			image_user = pygame.image.load(image_file_user)
			image_opp = pygame.image.load(image_file_opp)
			self.screen.blit(image_user, user_avatar_rect)
			self.screen.blit(image_opp, opp_avatar_rect)

			# Render the borders
			pygame.draw.rect(self.screen, Constants.SIDEBAR_BUTTON_BG, opp_avatar_border_rect, avatar_border_width)
			pygame.draw.rect(self.screen, Constants.SIDEBAR_BUTTON_BG, user_avatar_border_rect, avatar_border_width)

			# Player names
			name_width = Constants.NAME_WIDTH
			name_height = Constants.NAME_HEIGHT
			name_x = avatar_x + (avatar_border_width/2)
			name_user_y = user_avatar_y + avatar_size + (avatar_border_width) 
			name_opp_y = opp_avatar_y + avatar_size + (avatar_border_width) 
			name_user_rect = (name_x, name_user_y, name_width, name_height)
			name_opp_rect = (name_x, name_opp_y, name_width, name_height)
			name_user_rect_border = (name_x-2, name_user_y, name_width+2, name_height)
			name_opp_rect_border = (name_x-2, name_opp_y, name_width+2, name_height)

			pygame.draw.rect(self.screen, Constants.SIDEBAR_BUTTON_BG, name_opp_rect)
			pygame.draw.rect(self.screen, Constants.SIDEBAR_BUTTON_BG, name_user_rect)
			pygame.draw.rect(self.screen, Constants.SIDEBAR_BUTTON_BG, name_opp_rect_border, avatar_border_width)
			pygame.draw.rect(self.screen, Constants.SIDEBAR_BUTTON_BG, name_user_rect_border, avatar_border_width)

			name_opp = self.name_opp
			name_user = self.name_user

			font_hp = Constants.RESOURCES+Constants.FONT_HP
			basic_font = pygame.font.Font(font_hp, Constants.HP_TEXT_FONT_SIZE)

			# User's name
			name_user_render = basic_font.render(name_user, True, Constants.WHITE)
			name_user_rect = name_user_render.get_rect()
			name_user_rect.centerx = avatar_x + Constants.NAME_BUFFER
			name_user_rect.centery = user_avatar_y + avatar_size + (avatar_border_width*2) + border
			
			# Opponent's name
			name_opp_render = basic_font.render(name_opp, True, Constants.WHITE)
			name_opp_rect = name_opp_render.get_rect()
			name_opp_rect.centerx = avatar_x + Constants.NAME_BUFFER
			name_opp_rect.centery = opp_avatar_y + avatar_size + (avatar_border_width*2) + border

			self.screen.blit(name_user_render, name_user_rect)
			self.screen.blit(name_opp_render, name_opp_rect)

		# Render board contents
		for i in range(8):
			is_king_and_threatened = False

			for j in range(8):
				# Render the tile
				self.render_tile(i, j)

				# Render the board guide
				if j == 0:
					if self.is_player_white:
						num_text = Constants.NUM_MAPPING[7-i]
						char_text = Constants.CHAR_MAPPING[i]
					else:
						num_text = Constants.NUM_MAPPING[i]
						char_text = Constants.CHAR_MAPPING[7-i]

					basic_font = pygame.font.Font(font, 15)
					guide_text_char = basic_font.render(char_text, True, Constants.WHITE)
					guide_text_num = basic_font.render(num_text, True, Constants.WHITE)

					char_rect = guide_text_char.get_rect()
					char_rect.centerx = Constants.BOARD_BUFFER + Constants.TILE_LENGTH*i + Constants.TILE_LENGTH/2
					char_rect.centery = Constants.BOARD_BUFFER/2

					num_rect = guide_text_num.get_rect()
					num_rect.centerx = Constants.BOARD_BUFFER/2
					num_rect.centery = Constants.BOARD_BUFFER + Constants.TILE_LENGTH*i + Constants.TILE_LENGTH/2

					self.screen.blit(guide_text_char, char_rect)
					self.screen.blit(guide_text_num, num_rect)

		pygame.display.flip()

	def render_tile(self, i, j):

		is_king_and_threatened = False
		font = Constants.RESOURCES+Constants.FONT
		font_reg = Constants.RESOURCES+Constants.FONT_REG

		if(i % 2 == 0):
			leading_color = Constants.CHESSBOARD_WH
			lagging_color = Constants.CHESSBOARD_DK
		else:
			leading_color = Constants.CHESSBOARD_DK
			lagging_color = Constants.CHESSBOARD_WH

		tile_color = leading_color if j % 2 == 0 else lagging_color

		# Render the tile
		tile_color = leading_color if j % 2 == 0 else lagging_color

		if self.is_player_white:
			x_coord = i
			y_coord = 7-j
		else:
			x_coord = 7-i
			y_coord = j

		tile = self.board[x_coord][y_coord]
		piece = tile.piece
		render_threats = False
		is_urgent = False

		rect_x = Constants.BOARD_BUFFER+Constants.TILE_LENGTH*i
		rect_y = Constants.BOARD_BUFFER+Constants.TILE_LENGTH*j
		side = Constants.TILE_LENGTH
		pygame.draw.rect(self.screen, tile_color, (rect_x, rect_y, side, side), 0)

		if tile.is_last_movement:
			thickness = Constants.LAST_MOVEMENT_BORDER_THICKNESS
			decrease = Constants.LAST_MOVEMENT_DECREASE_FACTOR
			coord_buffer = side*(1-decrease)/2
			pygame.draw.rect(self.screen, Constants.JUST_MOVED, (rect_x+coord_buffer, rect_y+coord_buffer, side*decrease, side*decrease), thickness)

		threat_level_user = tile.threat_level_user
		threat_level_opponent = tile.threat_level_opponent
		cumulative_threat = threat_level_user - threat_level_opponent

		if(piece is not None):

			# Render the pieces
			piece_rect = (rect_x, rect_y, side, side)
			piece_type = piece.piece_type
			piece.piece_position = piece_rect

			color = "w" if piece.is_white else "b"
			image_file = color + str(piece_type) + ".png"

			image_piece = pygame.image.load(Constants.RESOURCES+image_file)
			self.screen.blit(image_piece, piece_rect)

			# Render the threatened pieces
			is_king_and_threatened = piece_type == Constants.P_KING and piece.is_user and threat_level_opponent > 0
			if ((cumulative_threat < 0 and piece.is_user) or (cumulative_threat > 0 and not piece.is_user)) or is_king_and_threatened:
				render_threats = True
				is_urgent = True

		# Render the empty tile threats
		else:
			render_threats = True

		if render_threats:
			difference = Constants.TILE_DIFFERENCE
			alpha = 0
			basic_font = pygame.font.Font(font_reg, Constants.THREAT_FONT_SIZE)

			# The opponent is guarding the tile!
			if cumulative_threat < 0:
				color = Constants.RED
				threat_string = str(abs(cumulative_threat))
				alpha = 255.0*abs(cumulative_threat)/12.0

			# The user is guarding the tile!
			elif cumulative_threat > 0:
				color = Constants.BLUE
				threat_string = str(abs(cumulative_threat))
				alpha = 255.0*abs(cumulative_threat)/12.0

			# Special case: even though it's 0, you still can't just put your queen there 'cause you'll be captured!
			elif cumulative_threat == 0:
				if threat_level_opponent > 0:
					alpha = 21.25 #255*1/12
					threat_string = str(threat_level_opponent)+"*"
					color = Constants.RED
				elif threat_level_user > 0:
					alpha = 21.25 #255*1/12
					threat_string = str(threat_level_user)+"*"
					color = Constants.BLUE

			if is_urgent:
				alpha = 64

			if is_king_and_threatened:
				threat_string = "*"
				color = Constants.RED

			s = pygame.Surface((Constants.TILE_LENGTH-difference, Constants.TILE_LENGTH-difference))
			s.set_alpha(alpha)

			if(alpha != 0):
				s.fill(color)
				alpha_text = alpha * 1.5 if alpha * 1.5 < 255 else 255
				threat_text = basic_font.render(threat_string, True, color, tile_color)

				text_rect = threat_text.get_rect()
				text_rect.centerx = Constants.BOARD_BUFFER+(difference/2)+Constants.TILE_LENGTH*i + 5
				text_rect.centery = Constants.BOARD_BUFFER+(difference/2)+Constants.TILE_LENGTH*j + 10

				threat_text.set_alpha(alpha_text)
				self.screen.blit(threat_text, text_rect)

			self.screen.blit(s, (Constants.BOARD_BUFFER+(difference/2)+Constants.TILE_LENGTH*i, Constants.BOARD_BUFFER+(difference/2)+Constants.TILE_LENGTH*j))

		# Render traversibility
		if tile.is_traversable:
			circle_x = Constants.BOARD_BUFFER+Constants.TILE_LENGTH*i+Constants.TILE_LENGTH/2
			circle_y = Constants.BOARD_BUFFER+Constants.TILE_LENGTH*j+Constants.TILE_LENGTH/2

			pygame.gfxdraw.filled_circle(self.screen, circle_x, circle_y, Constants.TRAVERSABLE_SEMIRADIUS, Constants.TRAVERSABLE_SEMI)
			pygame.gfxdraw.filled_circle(self.screen, circle_x, circle_y, Constants.TRAVERSABLE_MINIRADIUS, Constants.TRAVERSABLE_MINI)

	def move_piece(self, source_x, source_y, destination_x, destination_y, promotion = False):
		# Flag for checking if the move is a capture
		hp_converter = {
			0: 1,
			9: 9,
			5: 5,
			3: 3,
			4: 3,
			1: 1,
		}
		is_capture = self.board[destination_x][destination_y].piece is not None
		if is_capture:

			captured_piece = self.board[destination_x][destination_y].piece
			captured_color = 'w' if captured_piece.is_white else 'b'
			active_color = self.active_turn

			if self.is_player_white:
				if active_color == 'w':
					self.user_captured.push([captured_color+str(captured_piece.piece_type), self.fullmove_clock])
					self.user_captured.sort()
					self.opponent_hp_current -= hp_converter[captured_piece.piece_type]
				else: 
					self.opponent_captured.push([captured_color+str(captured_piece.piece_type), self.fullmove_clock])
					self.opponent_captured.sort()
					self.user_hp_current -= hp_converter[captured_piece.piece_type]
			else:
				if active_color == 'w':
					self.opponent_captured.push([captured_color+str(captured_piece.piece_type), self.fullmove_clock])
					self.opponent_captured.sort()
					self.user_hp_current -= hp_converter[captured_piece.piece_type]
				else: 
					self.user_captured.push([captured_color+str(captured_piece.piece_type), self.fullmove_clock])
					self.user_captured.sort()
					self.opponent_hp_current -= hp_converter[captured_piece.piece_type]

		piece = self.board[source_x][source_y].piece

		# Clear last movement
		self.clear_last_movement()

		# Move the piece in the game
		destination_piece = self.board[source_x][source_y].piece
		self.board[source_x][source_y].remove_piece()

		# Animate the movement
		if self.animate:
			if self.is_player_white:
				source_coord_x = (source_x * Constants.TILE_LENGTH) + Constants.BOARD_BUFFER
				source_coord_y = ((7 - source_y)*Constants.TILE_LENGTH) + Constants.BOARD_BUFFER
				destination_coord_x = (destination_x * Constants.TILE_LENGTH) + Constants.BOARD_BUFFER
				destination_coord_y = ((7 - destination_y)*Constants.TILE_LENGTH) + Constants.BOARD_BUFFER
			else:
				source_coord_x = ((7 - source_x)*Constants.TILE_LENGTH) + Constants.BOARD_BUFFER
				source_coord_y = (source_y * Constants.TILE_LENGTH) + Constants.BOARD_BUFFER
				destination_coord_x = ((7 - destination_x)*Constants.TILE_LENGTH) + Constants.BOARD_BUFFER
				destination_coord_y = (destination_y * Constants.TILE_LENGTH) + Constants.BOARD_BUFFER

			is_vertical = destination_coord_x - source_coord_x == 0
			is_horizontal = destination_coord_y - source_coord_y == 0

			m = 0
			b = 0
			if not (is_vertical or is_horizontal):
				m = (destination_coord_y - source_coord_y)/(destination_coord_x - source_coord_x)
				b = destination_coord_y - (m * destination_coord_x)

			x = source_coord_x
			y = source_coord_y

			frames = 30
			i = 0

			if is_vertical:
				multiplier = 1 if destination_coord_y - source_coord_y < 0 else -1
				increment = abs((destination_coord_y - source_coord_y)/(frames*1.25))
			elif is_horizontal:
				multiplier = 1 if destination_coord_x - source_coord_x < 0 else -1
				increment = abs((destination_coord_x - source_coord_x)/(frames*1.25))
			else:
				multiplier_x = 1 if destination_coord_x - source_coord_x < 0 else -1
				multiplier_y = 1 if destination_coord_y - source_coord_y < 0 else -1
				temp_x = destination_coord_x - source_coord_x
				temp_y = destination_coord_y - source_coord_y
				temp_x = temp_x * temp_x
				temp_y = temp_y * temp_y
				increment = abs(math.pow(((temp_x)+(temp_x)), 0.5)/frames)

			clock = pygame.time.Clock()

			while True:

				if not (is_vertical or is_horizontal):
					x -= multiplier_x*(increment)
					y = m*x + b

					x = int(x)
					y = int(y)

					i_temp = (x - Constants.BOARD_BUFFER)/Constants.TILE_LENGTH
					i_temp_1 = i_temp + 1
					i_temp_2 = i_temp - 1
					j_temp = (y - Constants.BOARD_BUFFER)/Constants.TILE_LENGTH
					j_temp_1 = j_temp + 1
					j_temp_2 = j_temp - 1

					i_temp = int(i_temp)
					i_temp_1 = int(i_temp_1)
					i_temp_2 = int(i_temp_2)
					j_temp = int(j_temp)
					j_temp_1 = int(j_temp_1)
					j_temp_2 = int(j_temp_2)

					i1_gte_0 = i_temp_1 >= 0
					i2_gte_0 = i_temp_2 >= 0
					j1_gte_0 = j_temp_1 >= 0
					j2_gte_0 = j_temp_2 >= 0

					i1_lte_7 = i_temp_1 <= 7
					i2_lte_7 = i_temp_2 <= 7
					j1_lte_7 = j_temp_1 <= 7
					j2_lte_7 = j_temp_2 <= 7

					i_withinrange = i_temp >= 0 and i_temp <= 7
					j_withinrange = j_temp >= 0 and j_temp <= 7

					if i_withinrange and j_withinrange:
						self.render_tile(i_temp, j_temp)
						if i1_lte_7 and i1_gte_0:
							self.render_tile(i_temp_1, j_temp)
						if i2_lte_7 and i2_gte_0:
							self.render_tile(i_temp_2, j_temp)

						if j1_gte_0 and j1_lte_7:
							self.render_tile(i_temp, j_temp_1)

							if i1_lte_7 and i1_gte_0:
								self.render_tile(i_temp_1, j_temp_1)
							if i2_lte_7 and i2_gte_0:
								self.render_tile(i_temp_2, j_temp_1)

						if j2_gte_0 and j2_lte_7:
							self.render_tile(i_temp, j_temp_2)
							if i1_lte_7 and i1_gte_0:
								self.render_tile(i_temp_1, j_temp_2)
							if i2_lte_7 and i2_gte_0:
								self.render_tile(i_temp_2, j_temp_2)

					if multiplier_x*x < multiplier_x*destination_coord_x:
						break

				elif is_vertical:
					y -= multiplier*(increment)
					y = int(y)

					i = (x - Constants.BOARD_BUFFER)/Constants.TILE_LENGTH
					j_before = (y - Constants.BOARD_BUFFER)/Constants.TILE_LENGTH
					j_after = j_before + multiplier

					if i >= 0 and i <= 7:
						if j_before >= 0 and j_before <= 7:
							self.render_tile(i, j_before)
						if j_after >= 0 and j_after <= 7:
							self.render_tile(i, j_after)

					if multiplier*y < multiplier*destination_coord_y:
						break
				elif is_horizontal:

					x -= multiplier*(increment)

					i_before = int((x - Constants.BOARD_BUFFER)/Constants.TILE_LENGTH)
					i_after = int(i_before + multiplier)
					j = int((y - Constants.BOARD_BUFFER)/Constants.TILE_LENGTH)
					
					if j >= 0 and j <= 7:
						if i_before >= 0 and i_before <= 7:
							self.render_tile(i_before, j)
						if i_after >= 0 and i_after <= 7:
							self.render_tile(i_after, j)

					if multiplier*x < multiplier*destination_coord_x:
						break

				side = Constants.TILE_LENGTH
				piece_rect = (x, y, side, side)
				piece_type = piece.piece_type
				piece.piece_position = piece_rect

				color = "w" if piece.is_white else "b"
				image_file = color + str(piece_type) + ".png"

				image_piece = pygame.image.load(Constants.RESOURCES+image_file)
				self.screen.blit(image_piece, piece_rect)

				pygame.display.update()
				clock.tick(240)

		# Destination
		self.board[destination_x][destination_y].piece = destination_piece

		if promotion:
			self.board[destination_x][destination_y].piece.piece_type = promotion
			self.opponent_hp_current += (hp_converter[promotion] - 1)


		# Mark the last moved piece
		self.board[destination_x][destination_y].is_last_movement = True
		self.board[source_x][source_y].is_last_movement = True

		# Half-move clock and full-move clock
		is_pawn_move = piece.piece_type == Constants.P_PAWN

		self.halfmove_clock = 0 if is_pawn_move or is_capture else self.halfmove_clock + 1
		self.fullmove_clock = self.fullmove_clock + 1 if self.active_turn == 'b' else self.fullmove_clock
		
		# Set the is_moved to True
		if not piece.is_moved:
			piece.is_moved = True

		difference_x = destination_x - source_x
		difference_y = destination_y - source_y

		# Check if it's an en passant
		is_piece_pawn = piece.piece_type == Constants.P_PAWN
		if self.en_passant != '-' and is_piece_pawn and destination_x == Constants.PIECE_MAPPING[self.en_passant[0]] and destination_y == Constants.PIECE_MAPPING[self.en_passant[1]]:
			factor = -1 if piece.is_white else 1
			self.board[destination_x][destination_y+factor].remove_piece()
			self.en_passant = '-'

		# Check if the pawn that just moved is en passant-able
		if piece.piece_type == Constants.P_PAWN and abs(difference_y) == 2:
			passant_mapping_y = destination_y - 1 if piece.is_white else destination_y + 1

			self.en_passant = Constants.CHAR_MAPPING[destination_x] + Constants.NUM_MAPPING[passant_mapping_y]
			# print "The piece is en passant-able!"
			# print "The target en passant square is ", self.en_passant

		else:
			self.en_passant = '-'

		# Check if it's a castle. If yes, move the rook as well
		if piece.piece_type == Constants.P_KING and abs(difference_x) == 2:
			# Kingside castle:
			if destination_x == Constants.TILE_C:
				rook_destination = Constants.TILE_D
				rook_source = Constants.TILE_A

			# Queenside castle:
			else:
				rook_destination = Constants.TILE_F
				rook_source = Constants.TILE_H
				
			self.board[rook_destination][destination_y].piece = self.board[rook_source][destination_y].piece
			self.board[rook_source][destination_y].remove_piece()

			# Update the FEN notation to bar the side from castling again
			if piece.is_white:
				self.kingside_white = '-'
				self.queenside_white = '-'

			else:
				self.kingside_black = '-'
				self.queenside_black = '-'

	def convert_to_fen(self):

		fen_piece = {
			Constants.P_PAWN: 'p',
			Constants.P_KNIGHT: 'n',
			Constants.P_BISHOP: 'b',
			Constants.P_ROOK: 'r',
			Constants.P_QUEEN: 'q',
			Constants.P_KING: 'k'
		}
		fen_string = ""

		for i in range(8):
			blank = 0
			for j in range(8):
				piece = self.board[j][7-i].piece

				if piece is not None:
					if blank is not 0:
						fen_string += str(blank)
						blank = 0
					fen_string += fen_piece[piece.piece_type].upper() if piece.is_white else fen_piece[piece.piece_type]
				else:
					blank += 1
			if blank is not 0:
				fen_string += str(blank)
			if i < 7:
				fen_string += "/"

		fen_string += " " + self.active_turn + " " + self.kingside_white + self.queenside_white + self.kingside_black + self.queenside_black + " " + self.en_passant + " " + str(self.halfmove_clock) + " " + str(self.fullmove_clock)
		# print ">>> BOARD_TO_FEN:", fen_string
		return fen_string

	def clear_traversable(self):
		for x in range(8):
			for y in range(8):
				self.board[x][y].is_traversable = False

	def show_traversable(self, i, j):
		self.clear_traversable()

		piece = self.board[i][j].piece

		is_i_lt_7 = i < 7
		is_i_lt_6 = i < 6
		is_7j_lt_7 = j < 7
		is_7j_lt_6 = j < 6

		is_i_gt_1 = i > 1
		is_i_gt_0 = i > 0
		is_7j_gt_1 = j > 1
		is_7j_gt_0 = j > 0

		is_i_lte_7 = i+1 <= 7
		is_i_gte_0 = i-1 >= 0
		is_7j_lte_7 = j+1 <= 7
		is_7j_gte_0 = j-1 >= 0
		
		if piece.piece_type == Constants.P_KNIGHT:
			if(is_i_gt_0):
				if(is_7j_lt_6):
					target_tile = self.board[i-1][j+2]

					temp_board = copy.deepcopy(self.board)
					temp_board[i-1][j+2].set_piece(temp_board[i][j].get_piece())
					temp_board[i][j].remove_piece()
					is_check_after_move = self.is_check(temp_board)

					if (target_tile.piece == None or target_tile.piece.is_user == False) and not is_check_after_move:
						target_tile.is_traversable = True

				if(is_7j_gt_1):
					target_tile = self.board[i-1][j-2]

					temp_board = copy.deepcopy(self.board)
					temp_board[i-1][j-2].set_piece(temp_board[i][j].get_piece())
					temp_board[i][j].remove_piece()
					is_check_after_move = self.is_check(temp_board)

					if (target_tile.piece == None or target_tile.piece.is_user == False) and not is_check_after_move:
						target_tile.is_traversable = True
											
			if(is_i_lt_7):
				if(is_7j_lt_6):
					target_tile = self.board[i+1][j+2]

					temp_board = copy.deepcopy(self.board)
					temp_board[i+1][j+2].set_piece(temp_board[i][j].get_piece())
					temp_board[i][j].remove_piece()
					is_check_after_move = self.is_check(temp_board)

					if (target_tile.piece == None or target_tile.piece.is_user == False) and not is_check_after_move:
						target_tile.is_traversable = True
						
				if(is_7j_gt_1):
					target_tile = self.board[i+1][j-2]						

					temp_board = copy.deepcopy(self.board)
					temp_board[i+1][j-2].set_piece(temp_board[i][j].get_piece())
					temp_board[i][j].remove_piece()
					is_check_after_move = self.is_check(temp_board)

					if (target_tile.piece == None or target_tile.piece.is_user == False) and not is_check_after_move:
						target_tile.is_traversable = True

			if(is_i_gt_1):
				if(is_7j_lt_7):
					target_tile = self.board[i-2][j+1]

					temp_board = copy.deepcopy(self.board)
					temp_board[i-2][j+1].set_piece(temp_board[i][j].get_piece())
					temp_board[i][j].remove_piece()
					is_check_after_move = self.is_check(temp_board)

					if (target_tile.piece == None or target_tile.piece.is_user == False) and not is_check_after_move:
						target_tile.is_traversable = True
						
				if(is_7j_gt_0):
					target_tile = self.board[i-2][j-1]

					temp_board = copy.deepcopy(self.board)
					temp_board[i-2][j-1].set_piece(temp_board[i][j].get_piece())
					temp_board[i][j].remove_piece()
					is_check_after_move = self.is_check(temp_board)

					if (target_tile.piece == None or target_tile.piece.is_user == False) and not is_check_after_move:
						target_tile.is_traversable = True
						

			if(is_i_lt_6):
				if(is_7j_lt_7):
					target_tile = self.board[i+2][j+1]

					temp_board = copy.deepcopy(self.board)
					temp_board[i+2][j+1].set_piece(temp_board[i][j].get_piece())
					temp_board[i][j].remove_piece()
					is_check_after_move = self.is_check(temp_board)

					if (target_tile.piece == None or target_tile.piece.is_user == False) and not is_check_after_move:
						target_tile.is_traversable = True
						
				if(is_7j_gt_0):
					target_tile = self.board[i+2][j-1]

					temp_board = copy.deepcopy(self.board)
					temp_board[i+2][j-1].set_piece(temp_board[i][j].get_piece())
					temp_board[i][j].remove_piece()
					is_check_after_move = self.is_check(temp_board)

					if (target_tile.piece == None or target_tile.piece.is_user == False) and not is_check_after_move:
						target_tile.is_traversable = True
							
		elif piece.piece_type == Constants.P_BISHOP:
			dirNE = True
			dirSE = True
			dirNW = True
			dirSW = True

			for k in range(1, 8):
				is_ik_lte_7 = i+k <= 7
				is_ik_gte_0 = i-k >= 0
				if_7j_lte_7 = j+k <= 7
				if_7j_gte_0 = j-k >= 0

				if(is_ik_lte_7):
					if(if_7j_lte_7 and dirNE):
						target_tile = self.board[i+k][j+k]

						temp_board = copy.deepcopy(self.board)
						temp_board[i+k][j+k].set_piece(temp_board[i][j].get_piece())
						temp_board[i][j].remove_piece()
						is_check_after_move = self.is_check(temp_board)

						if (target_tile.piece == None or target_tile.piece.is_user == False):
							if not is_check_after_move:
								target_tile.is_traversable = True
							if(target_tile.piece is not None and target_tile.piece.is_user == False):
								dirNE = False
						else:
							dirNE = False
					else:
						dirNE = False

					if(if_7j_gte_0 and dirSE):
						target_tile = self.board[i+k][j-k]

						temp_board = copy.deepcopy(self.board)
						temp_board[i+k][j-k].set_piece(temp_board[i][j].get_piece())
						temp_board[i][j].remove_piece()
						is_check_after_move = self.is_check(temp_board)

						if (target_tile.piece == None or target_tile.piece.is_user == False):
							if not is_check_after_move:
								target_tile.is_traversable = True
							if(target_tile.piece is not None and target_tile.piece.is_user == False):
								dirSE = False
						else:
							dirSE = False
					else:
						dirSE = False

				if(is_ik_gte_0):
					if(if_7j_lte_7 and dirNW):
						target_tile = self.board[i-k][j+k]

						temp_board = copy.deepcopy(self.board)
						temp_board[i-k][j+k].set_piece(temp_board[i][j].get_piece())
						temp_board[i][j].remove_piece()
						is_check_after_move = self.is_check(temp_board)

						if (target_tile.piece == None or target_tile.piece.is_user == False):
							if not is_check_after_move:
								target_tile.is_traversable = True
							if(target_tile.piece is not None and target_tile.piece.is_user == False):
								dirNW = False
						else:
							dirNW = False
					else:
						dirNW = False

					if(if_7j_gte_0 and dirSW):
						target_tile = self.board[i-k][j-k]

						temp_board = copy.deepcopy(self.board)
						temp_board[i-k][j-k].set_piece(temp_board[i][j].get_piece())
						temp_board[i][j].remove_piece()
						is_check_after_move = self.is_check(temp_board)

						if (target_tile.piece == None or target_tile.piece.is_user == False):
							if not is_check_after_move:
								target_tile.is_traversable = True
							if(target_tile.piece is not None and target_tile.piece.is_user == False):
								dirSW = False
						else:
							dirSW = False
					else:
						dirSW = False
		
		elif piece.piece_type == Constants.P_ROOK:
			dirN = True
			dirS = True
			dirE = True
			dirW = True
			for k in range(1, 8):
				is_ik_lte_7 = i+k <= 7
				is_ik_gte_0 = i-k >= 0
				if_7j_lte_7 = j+k <= 7
				if_7j_gte_0 = j-k >= 0

				if(is_ik_lte_7 and dirE):
					target_tile = self.board[i+k][j]

					temp_board = copy.deepcopy(self.board)
					temp_board[i+k][j].set_piece(temp_board[i][j].get_piece())
					temp_board[i][j].remove_piece()
					is_check_after_move = self.is_check(temp_board)

					if (target_tile.piece == None or target_tile.piece.is_user == False):
						if not is_check_after_move:
							target_tile.is_traversable = True
						if(target_tile.piece is not None and target_tile.piece.is_user == False):
							dirE = False
					else:
						dirE = False
				else:
					dirE = False

				if(is_ik_gte_0 and dirW):
					target_tile = self.board[i-k][j]

					temp_board = copy.deepcopy(self.board)
					temp_board[i-k][j].set_piece(temp_board[i][j].get_piece())
					temp_board[i][j].remove_piece()
					is_check_after_move = self.is_check(temp_board)

					if (target_tile.piece == None or target_tile.piece.is_user == False):
						if not is_check_after_move:
							target_tile.is_traversable = True
						if(target_tile.piece is not None and target_tile.piece.is_user == False):
							dirW = False
					else:
						dirW = False
				else:
					dirW = False

				if(if_7j_lte_7 and dirN):
					target_tile = self.board[i][j+k]

					temp_board = copy.deepcopy(self.board)
					temp_board[i][j+k].set_piece(temp_board[i][j].get_piece())
					temp_board[i][j].remove_piece()
					is_check_after_move = self.is_check(temp_board)

					if (target_tile.piece == None or target_tile.piece.is_user == False):
						if not is_check_after_move:
							target_tile.is_traversable = True
						if(target_tile.piece is not None and target_tile.piece.is_user == False):
							dirN = False
					else:
						dirN = False
				else:
					dirN = False

				if(if_7j_gte_0 and dirS):
					target_tile = self.board[i][j-k]

					temp_board = copy.deepcopy(self.board)
					temp_board[i][j-k].set_piece(temp_board[i][j].get_piece())
					temp_board[i][j].remove_piece()
					is_check_after_move = self.is_check(temp_board)

					if (target_tile.piece == None or target_tile.piece.is_user == False):
						if not is_check_after_move:
							target_tile.is_traversable = True
						if(target_tile.piece is not None and target_tile.piece.is_user == False):
							dirS = False
					else:
						dirS = False
				else:
					dirS = False
		
		elif piece.piece_type == Constants.P_QUEEN:
			dirNE = True
			dirSE = True
			dirNW = True
			dirSW = True

			dirN = True
			dirS = True
			dirE = True
			dirW = True
			for k in range(1, 8):
				is_ik_lte_7 = i+k <= 7
				is_ik_gte_0 = i-k >= 0
				if_7j_lte_7 = j+k <= 7
				if_7j_gte_0 = j-k >= 0

				if(is_ik_lte_7 and dirE):
					target_tile = self.board[i+k][j]

					temp_board = copy.deepcopy(self.board)
					temp_board[i+k][j].set_piece(temp_board[i][j].get_piece())
					temp_board[i][j].remove_piece()
					is_check_after_move = self.is_check(temp_board)

					if (target_tile.piece == None or target_tile.piece.is_user == False):
						if not is_check_after_move:
							target_tile.is_traversable = True
						if(target_tile.piece is not None and target_tile.piece.is_user == False):
							dirE = False
					else:
						dirE = False
				else:
					dirE = False

				if(is_ik_gte_0 and dirW):
					target_tile = self.board[i-k][j]

					temp_board = copy.deepcopy(self.board)
					temp_board[i-k][j].set_piece(temp_board[i][j].get_piece())
					temp_board[i][j].remove_piece()
					is_check_after_move = self.is_check(temp_board)

					if (target_tile.piece == None or target_tile.piece.is_user == False):
						if not is_check_after_move:
							target_tile.is_traversable = True
						if(target_tile.piece is not None and target_tile.piece.is_user == False):
							dirW = False
					else:
						dirW = False
				else:
					dirW = False

				if(if_7j_lte_7 and dirN):
					target_tile = self.board[i][j+k]

					temp_board = copy.deepcopy(self.board)
					temp_board[i][j+k].set_piece(temp_board[i][j].get_piece())
					temp_board[i][j].remove_piece()
					is_check_after_move = self.is_check(temp_board)

					if (target_tile.piece == None or target_tile.piece.is_user == False):
						if not is_check_after_move:
							target_tile.is_traversable = True
						if(target_tile.piece is not None and target_tile.piece.is_user == False):
							dirN = False
					else:
						dirN = False
				else:
					dirN = False

				if(if_7j_gte_0 and dirS):
					target_tile = self.board[i][j-k]

					temp_board = copy.deepcopy(self.board)
					temp_board[i][j-k].set_piece(temp_board[i][j].get_piece())
					temp_board[i][j].remove_piece()
					is_check_after_move = self.is_check(temp_board)

					if (target_tile.piece == None or target_tile.piece.is_user == False):
						if not is_check_after_move:
							target_tile.is_traversable = True
						if(target_tile.piece is not None and target_tile.piece.is_user == False):
							dirS = False
					else:
						dirS = False
				else:
					dirS = False

				if(is_ik_lte_7):
					if(if_7j_lte_7 and dirNE):
						target_tile = self.board[i+k][j+k]

						temp_board = copy.deepcopy(self.board)
						temp_board[i+k][j+k].set_piece(temp_board[i][j].get_piece())
						temp_board[i][j].remove_piece()
						is_check_after_move = self.is_check(temp_board)

						if (target_tile.piece == None or target_tile.piece.is_user == False):
							if not is_check_after_move:
								target_tile.is_traversable = True
							if(target_tile.piece is not None and target_tile.piece.is_user == False):
								dirNE = False
						else:
							dirNE = False
					else:
						dirNE = False

					if(if_7j_gte_0 and dirSE):
						target_tile = self.board[i+k][j-k]

						temp_board = copy.deepcopy(self.board)
						temp_board[i+k][j-k].set_piece(temp_board[i][j].get_piece())
						temp_board[i][j].remove_piece()
						is_check_after_move = self.is_check(temp_board)

						if (target_tile.piece == None or target_tile.piece.is_user == False):
							if not is_check_after_move:
								target_tile.is_traversable = True
							if(target_tile.piece is not None and target_tile.piece.is_user == False):
								dirSE = False
						else:
							dirSE = False
					else:
						dirSE = False

				if(is_ik_gte_0):
					if(if_7j_lte_7 and dirNW):
						target_tile = self.board[i-k][j+k]

						temp_board = copy.deepcopy(self.board)
						temp_board[i-k][j+k].set_piece(temp_board[i][j].get_piece())
						temp_board[i][j].remove_piece()
						is_check_after_move = self.is_check(temp_board)

						if (target_tile.piece == None or target_tile.piece.is_user == False):
							if not is_check_after_move:
								target_tile.is_traversable = True
							if(target_tile.piece is not None and target_tile.piece.is_user == False):
								dirNW = False
						else:
							dirNW = False
					else:
						dirNW = False

					if(if_7j_gte_0 and dirSW):
						target_tile = self.board[i-k][j-k]

						temp_board = copy.deepcopy(self.board)
						temp_board[i-k][j-k].set_piece(temp_board[i][j].get_piece())
						temp_board[i][j].remove_piece()
						is_check_after_move = self.is_check(temp_board)

						if (target_tile.piece == None or target_tile.piece.is_user == False):
							if not is_check_after_move:
								target_tile.is_traversable = True
							if(target_tile.piece is not None and target_tile.piece.is_user == False):
								dirSW = False
						else:
							dirSW = False
					else:
						dirSW = False
		
		elif piece.piece_type == Constants.P_KING:
			if(is_i_lte_7):
				target_tile = self.board[i+1][j]

				temp_board = copy.deepcopy(self.board)
				temp_board[i+1][j].set_piece(temp_board[i][j].get_piece())
				temp_board[i][j].remove_piece()
				is_check_after_move = self.is_check(temp_board)

				if(target_tile.threat_level_opponent <= 0 and (target_tile.piece == None or target_tile.piece.is_user == False)) and not is_check_after_move:
					target_tile.is_traversable = True
				
				if(is_7j_lte_7):
					target_tile = self.board[i+1][j+1]

					temp_board = copy.deepcopy(self.board)
					temp_board[i+1][j+1].set_piece(temp_board[i][j].get_piece())
					temp_board[i][j].remove_piece()
					is_check_after_move = self.is_check(temp_board)

					if(target_tile.threat_level_opponent <= 0 and (target_tile.piece == None or target_tile.piece.is_user == False)) and not is_check_after_move:
						target_tile.is_traversable = True
				
				if(is_7j_gte_0):
					target_tile = self.board[i+1][j-1]

					temp_board = copy.deepcopy(self.board)
					temp_board[i+1][j-1].set_piece(temp_board[i][j].get_piece())
					temp_board[i][j].remove_piece()
					is_check_after_move = self.is_check(temp_board)

					if(target_tile.threat_level_opponent <= 0 and (target_tile.piece == None or target_tile.piece.is_user == False)) and not is_check_after_move:
						target_tile.is_traversable = True
				
			if(is_i_gte_0):
				target_tile = self.board[i-1][j]

				temp_board = copy.deepcopy(self.board)
				temp_board[i-1][j].set_piece(temp_board[i][j].get_piece())
				temp_board[i][j].remove_piece()
				is_check_after_move = self.is_check(temp_board)

				if(target_tile.threat_level_opponent <= 0 and (target_tile.piece == None or target_tile.piece.is_user == False)) and not is_check_after_move:
					target_tile.is_traversable = True
				
				if(is_7j_lte_7):
					target_tile = self.board[i-1][j+1]

					temp_board = copy.deepcopy(self.board)
					temp_board[i-1][j+1].set_piece(temp_board[i][j].get_piece())
					temp_board[i][j].remove_piece()
					is_check_after_move = self.is_check(temp_board)

					if(target_tile.threat_level_opponent <= 0 and (target_tile.piece == None or target_tile.piece.is_user == False)) and not is_check_after_move:
						target_tile.is_traversable = True
				
				if(is_7j_gte_0):
					target_tile = self.board[i-1][j-1]

					temp_board = copy.deepcopy(self.board)
					temp_board[i-1][j-1].set_piece(temp_board[i][j].get_piece())
					temp_board[i][j].remove_piece()
					is_check_after_move = self.is_check(temp_board)

					if(target_tile.threat_level_opponent <= 0 and (target_tile.piece == None or target_tile.piece.is_user == False)) and not is_check_after_move:
						target_tile.is_traversable = True
				
			if(is_7j_lte_7):
				target_tile = self.board[i][j+1]

				temp_board = copy.deepcopy(self.board)
				temp_board[i][j+1].set_piece(temp_board[i][j].get_piece())
				temp_board[i][j].remove_piece()
				is_check_after_move = self.is_check(temp_board)

				if(target_tile.threat_level_opponent <= 0 and (target_tile.piece == None or target_tile.piece.is_user == False)) and not is_check_after_move:
					target_tile.is_traversable = True
			
			if(is_7j_gte_0):
				target_tile = self.board[i][j-1]

				temp_board = copy.deepcopy(self.board)
				temp_board[i][j-1].set_piece(temp_board[i][j].get_piece())
				temp_board[i][j].remove_piece()
				is_check_after_move = self.is_check(temp_board)

				if(target_tile.threat_level_opponent <= 0 and (target_tile.piece == None or target_tile.piece.is_user == False)) and not is_check_after_move:
					target_tile.is_traversable = True

			# Castling
			if not piece.is_moved and self.board[i][j].threat_level_opponent <= 0:
				can_castle_kingside = True
				can_castle_queenside = True

				rank = Constants.TILE_1 if piece.is_white else Constants.TILE_8

				kingside_rook = self.board[Constants.TILE_H][rank].piece is not None and not self.board[Constants.TILE_H][rank].piece.is_moved and self.board[Constants.TILE_H][rank].piece.piece_type == Constants.P_ROOK
				queenside_rook = self.board[Constants.TILE_A][rank].piece is not None and not self.board[Constants.TILE_A][rank].piece.is_moved and self.board[Constants.TILE_A][rank].piece.piece_type == Constants.P_ROOK
				
				if kingside_rook or queenside_rook:
					for k in range(1,3):
						if can_castle_kingside and kingside_rook:
							kingside_tile = self.board[i+k][rank]
							if kingside_tile.piece is not None or kingside_tile.threat_level_opponent > 0:
								can_castle_kingside = False
						else:
							can_castle_kingside = False

						if can_castle_queenside and queenside_rook:
							queenside_tile = self.board[i-k][rank]
							if queenside_tile.piece is not None or queenside_tile.threat_level_opponent > 0:
								can_castle_queenside = False
						else:
							can_castle_queenside = False

				else:
					can_castle_kingside = False
					can_castle_queenside = False

				if can_castle_kingside:
					self.board[i + 1][rank].is_traversable = True
					self.board[i + 2][rank].is_traversable = True

				if can_castle_queenside:
					self.board[i - 1][rank].is_traversable = True
					self.board[i - 2][rank].is_traversable = True

		elif piece.piece_type == Constants.P_PAWN:
			factor = 1 if piece.is_white else -1

			if is_7j_lte_7:
				# Normal movement: moving one square up (or below) a rank
				target_tile = self.board[i][j+factor*1]

				temp_board = copy.deepcopy(self.board)
				temp_board[i][j+factor*1].set_piece(temp_board[i][j].get_piece())
				temp_board[i][j].remove_piece()
				is_check_after_move = self.is_check(temp_board)

				if target_tile.piece == None and not is_check_after_move:
					target_tile.is_traversable = True

				# That movement from where the pawn moves two spaces. I don't know what it's called
				start_rank = Constants.PIECE_MAPPING['2'] if self.is_player_white else Constants.PIECE_MAPPING['7']
				if(j == start_rank and self.board[i][j+factor].piece == None):
					target_tile = self.board[i][j+factor*2]

					temp_board = copy.deepcopy(self.board)
					temp_board[i][j+factor*2].set_piece(temp_board[i][j].get_piece())
					temp_board[i][j].remove_piece()
					is_check_after_move = self.is_check(temp_board)

					if(target_tile.piece == None) and not is_check_after_move:
						target_tile.is_traversable = True

				# Pawn's doing a capture!
				if(is_i_lt_7 and is_7j_lt_7):
					target_tile = self.board[i+1][j+factor*1]

					temp_board = copy.deepcopy(self.board)
					temp_board[i+1][j+factor*1].set_piece(temp_board[i][j].get_piece())
					temp_board[i][j].remove_piece()
					is_check_after_move = self.is_check(temp_board)

					if(target_tile.piece is not None and target_tile.piece.is_user == False) and not is_check_after_move:
						target_tile.is_traversable = True

				if(is_i_gt_0 and is_7j_lt_7):
					target_tile = self.board[i-1][j+factor*1]

					temp_board = copy.deepcopy(self.board)
					temp_board[i-1][j+factor*1].set_piece(temp_board[i][j].get_piece())
					temp_board[i][j].remove_piece()
					is_check_after_move = self.is_check(temp_board)

					if(target_tile.piece is not None and target_tile.piece.is_user == False)  and not is_check_after_move:
						target_tile.is_traversable = True
			
 
			# En Passant
			if self.en_passant != '-' :
				target_tile_x = Constants.PIECE_MAPPING[self.en_passant[0]]
				target_tile_y = Constants.PIECE_MAPPING[self.en_passant[1]]
				
				factor = 1 if self.is_player_white else -1

				if j == target_tile_y - factor and (i == target_tile_x + factor or i == target_tile_x - factor):
					target_tile = self.board[target_tile_x][target_tile_y]
					target_tile.is_traversable = True

	def clear_last_movement(self):
		for x in range(8):
			for y in range(8):
				self.board[x][y].is_last_movement = False

	def clear_board(self):
		for i in range(8):
			for j in range(8):
				self.board[i][j].piece = None

	def convert_fen_to_board(self, fen_string, is_init = False):
		self.user_hp_current = 0
		self.opponent_hp_current = 0

		board_pieces = {
			"P": 8,
			"R": 2,
			"N": 2,
			"B": 2,
			"Q": 1,
			"K": 1,
			"p": 8,
			"r": 2,
			"n": 2,
			"b": 2,
			"q": 1,
			"k": 1
		}

		# print ">>> FEN_TO_BOARD:", fen_string
		# sys.exit(0)
		self.clear_board()
		fen = fen_string.split(" ")

		# No additional processing required
		self.active_turn = fen[1]
		self.en_passant = fen[3]
		self.halfmove_clock = int(fen[4])
		self.fullmove_clock = int(fen[5])

		# Castling information
		castling_info = fen[2]
		self.kingside_white = castling_info[0]
		self.queenside_white = castling_info[1]
		self.kingside_black = castling_info[2]
		self.queenside_black = castling_info[3]

		# Board information
		board_info = fen[0]
		rows = board_info.split("/")

		converter = {
			"K": [Constants.P_KING, True],
			"Q": [Constants.P_QUEEN, True],
			"R": [Constants.P_ROOK, True],
			"B": [Constants.P_BISHOP, True],
			"N": [Constants.P_KNIGHT, True],
			"P": [Constants.P_PAWN, True],
			"k": [Constants.P_KING, False],
			"q": [Constants.P_QUEEN, False],
			"r": [Constants.P_ROOK, False],
			"b": [Constants.P_BISHOP, False],
			"n": [Constants.P_KNIGHT, False],
			"p": [Constants.P_PAWN, False],
		}

		hp_converter = {
			"K": 1,
			"Q": 9,
			"R": 5,
			"B": 3,
			"N": 3,
			"P": 1,
			"k": 1,
			"q": 9,
			"r": 5,
			"b": 3,
			"n": 3,
			"p": 1,
		}

		i = 0
		j = 0
		for row in rows:
			for element in row:
				try:
				    element = int(element)
				    j += element
				except ValueError:
					is_piece_player = True if (self.is_player_white and converter[element][1]) or (not self.is_player_white and not converter[element][1]) else False
					if is_init:
						board_pieces[element] -= 1
					self.board[j][7-i].piece = Piece(converter[element][0], converter[element][1], is_piece_player)
					if is_piece_player:
						self.user_hp_current += hp_converter[element]
					else:
						self.opponent_hp_current += hp_converter[element]
					j += 1
			i+=1
			j=0

		self.user_hp_current_before = self.user_hp_current
		self.opponent_hp_current_before = self.opponent_hp_current

		if is_init:
			for element in board_pieces:	
				# print element, board_pieces[element]
				while board_pieces[element] > 0:
					captured_color = 'w' if converter[element][1] else 'b'
					if self.is_player_white:
						if captured_color == 'b':
							self.user_captured.push([captured_color+str(converter[element][0]), self.fullmove_clock])
							self.user_captured.sort()
						else: 
							self.opponent_captured.push([captured_color+str(converter[element][0]), self.fullmove_clock])
							self.opponent_captured.sort()
					else:
						if captured_color == 'b':
							self.opponent_captured.push([captured_color+str(converter[element][0]), self.fullmove_clock])
							self.opponent_captured.sort()
						else: 
							self.user_captured.push([captured_color+str(converter[element][0]), self.fullmove_clock])
							self.user_captured.sort()
					board_pieces[element] -= 1
					# print "PUSHED!!!"

	def game_over(self):
		while True:
			self.render_board()

	def play(self):
		self.build_threats(self.board)
		
		fen_string = self.convert_to_fen()
		current_move = ''
		self.stack.push([fen_string, current_move])
		# print "Pushed:", fen_string

		has_player_moved = False
		has_opponent_moved = False

		if fen_string == "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1":
			is_turn_user = True if self.is_player_white else False
			is_turn_opponent = False if is_turn_user else True
		else:
			is_active_turn_white = self.active_turn == 'w'
			is_turn_user = self.is_player_white == is_active_turn_white
			is_turn_opponent = False if is_turn_user else True

		thread = None

		while(True):			
			self.render_board()
			
			if has_player_moved or has_opponent_moved:
				self.is_user_check = False
				self.is_opponent_check = False
				self.clear_traversable()
				self.build_threats(self.board)
				self.render_board()

				if has_player_moved:
					self.active_turn = 'b' if self.is_player_white else 'w'
					has_player_moved = False
					is_turn_opponent = True
					is_turn_user = False

				elif has_opponent_moved:
					self.active_turn = 'w' if self.is_player_white else 'b'
					has_opponent_moved = False
					is_turn_opponent = False
					is_turn_user = True

				if not self.is_undergoing_promotion:
					fen_string = self.convert_to_fen()
					self.stack.push([fen_string, current_move])
					print "After:", fen_string

			if self.debug_mode:
				is_turn_opponent = False
				is_turn_user = True

			# Opponent's Turn
			if not self.debug_mode and is_turn_opponent and not self.is_undergoing_promotion:
				print fen_string
				thread = StockfishThread(fen_string, self.cpu_level)

				thread.start()
				is_turn_opponent = False

			if thread is not None and thread.is_thread_done is not None and thread.is_thread_done:

				thread.join()

				if not thread.is_undo_clicked:
					cpu_move = thread.cpu_move
					current_move = cpu_move
					ponder = thread.ponder

					print cpu_move
					print ponder

					# TO-DO: Condition for Stalemate
					# if cpu_move == '(none)' and ponder == '(none)':
					# 	print "Stalemate!"
					# 	time.sleep(2)
					# 	sys.exit(0)
					if cpu_move == '(none)':
						self.is_opponent_checkmate = True
						print "User won!"
						self.game_over()
						# time.sleep(2)
						# sys.exit(0)

					source_x = Constants.PIECE_MAPPING[cpu_move[:1]]
					source_y = Constants.PIECE_MAPPING[cpu_move[1:2]]
					destination_x = Constants.PIECE_MAPPING[cpu_move[2:3]]
					destination_y = Constants.PIECE_MAPPING[cpu_move[3:4]]
					promotion = False

					if len(cpu_move) == 5:
						promotion = cpu_move[4:5]
						promotion_map = {
							"r": Constants.P_ROOK,
							"b": Constants.P_BISHOP,
							"n": Constants.P_KNIGHT,
							"q": Constants.P_QUEEN
						}
						promotion = promotion_map[promotion]
	
					self.move_piece(source_x, source_y, destination_x, destination_y, promotion)

					has_opponent_moved = True
					thread.is_thread_done = False

					if ponder == '(none)':
						self.clear_traversable()
						self.build_threats(self.board)
						self.render_board()
						self.is_user_checkmate = True
						print "Stockfish won!"
						self.game_over()
						# time.sleep(2)
						# sys.exit(0)

			events = pygame.event.get()
			for event in events: 
				if event.type == pygame.QUIT: 
					sys.exit(0)

				# User's turn
				elif event.type == 5:
					mouse_pos = pygame.mouse.get_pos()

					if self.is_player_white:
						board_x = (mouse_pos[0] - Constants.BOARD_BUFFER)/Constants.TILE_LENGTH
						board_y = 7-((mouse_pos[1] - Constants.BOARD_BUFFER)/Constants.TILE_LENGTH)
					else:
						board_x = 7-((mouse_pos[0] - Constants.BOARD_BUFFER)/Constants.TILE_LENGTH)
						board_y = (mouse_pos[1] - Constants.BOARD_BUFFER)/Constants.TILE_LENGTH

					is_piece_clicked = False
					is_traversable = False
					promotion = ''

					# Did the user click on the board?
					if 0 <= board_x <= 7 and 0 <= board_y <= 7 and self.is_board_clickable and is_turn_user:
						# What did the user click? A piece? A tile? Is the tile traversable?
						tile = self.board[board_x][board_y]
						piece = tile.piece
						is_traversable = tile.is_traversable
						is_piece_clicked = piece is not None

					# The user clicked somewhere else!
					else:
						# Is the user clicking on the sidebar?
						if mouse_pos[0] >= (Constants.SCREENSIZE[0] - Constants.SIDEBAR_WIDTH):
							index = 65536
							if mouse_pos[1] % (Constants.SIDEBAR_BUTTON) >= Constants.BOARD_BUFFER:
								index = (mouse_pos[1]/Constants.SIDEBAR_BUTTON)

							if index < len(self.sidebar_buttons):
								if self.sidebar_buttons[index][2] == 'undo':
									# Cannot undo if stack only has one element
									if self.stack.size() > 1:
										# After an undo, it'll always be your turn unless it's the first move
										self.active_turn = 'w' if self.is_player_white else 'b'

										# print has_player_moved
										# sys.exit(0)

										# If the player has just moved, we pop twice
										if not is_turn_user:
											self.stack.pop()
											element = self.stack.pop()
											fen = element[0]
											thread.is_undo_clicked = True

											self.stack.push(element)
											
											is_turn_opponent = False
											is_turn_user = True

										# If the opponent has just moved...
										else:
											# If it's the very first move, we push it again.
											if self.stack.size() == 2:
												self.stack.pop()
												element = self.stack.pop()
												fen = element[0]
												# print "Popped thrice?", fen

												is_turn_opponent = False
												is_turn_user = True

												self.stack.push(element)
												# print "Pushed*:", fen

												if not self.is_player_white:
													self.active_turn = 'w'
													is_turn_opponent = True
													is_turn_user = False
												else:
													thread.is_undo_clicked = True

											else:
												# ...we pop thrice.
												self.stack.pop()
												self.stack.pop()
												element = self.stack.pop()
												fen = element[0]
												# print "Popped thrice?", fen

												is_turn_opponent = False
												is_turn_user = True

												self.stack.push(element)
												# print "Pushed*:", fen


										fen_string = fen
										self.convert_fen_to_board(fen)

										self.is_user_check = False
										self.is_opponent_check = False

										index = self.fullmove_clock #if self.is_player_white else self.fullmove_clock - 1
										opp_index = self.fullmove_clock if self.is_player_white else self.fullmove_clock + 1
										self.opponent_captured.search_and_pop(opp_index)
										self.user_captured.search_and_pop(index)

										self.clear_traversable()
										self.build_threats(self.board)
										self.render_board()
										self.clear_last_movement()

						# Is the user clicking on the promotion buttons?
						for i in range(4):
							if self.is_undergoing_promotion and self.promotions[i].pressed(mouse_pos):
								promotion = self.promotions[i].piece_type

								if promotion != '':
									self.board[self.source_x][self.source_y].piece.piece_type = promotion
									hp_converter = {
										0: 1,
										9: 9,
										5: 5,
										3: 3,
										4: 3,
										1: 1,
									}
									self.user_hp_current += (hp_converter[promotion] - 1)
									self.is_board_clickable = True
									self.is_undergoing_promotion = False

								has_player_moved = True
								break

					# A piece has been clicked!
					if is_piece_clicked and self.is_board_clickable and is_turn_user:
						# Let's check if it's a friendly piece
						if piece.pressed(mouse_pos):
							self.source_x = board_x
							self.source_y = board_y
							self.show_traversable(board_x, board_y)

						# It clicked on a traversable piece? User's gonna do a capture! Good for you, user.
						elif tile.is_traversable:
							is_traversable = True

						# User clicked on an enemy, uncapturable piece. Not this time!
						else:
							self.clear_traversable()

					# Looks like user clicked on a traversable tile
					if is_traversable:						
						self.clear_traversable()
						source_move_x = Constants.CHAR_MAPPING[self.source_x]
						source_move_y = Constants.NUM_MAPPING[self.source_y]
						destination_move_x = Constants.CHAR_MAPPING[board_x]
						destination_move_y = Constants.NUM_MAPPING[board_y]
						current_move = source_move_x + source_move_y + destination_move_x + destination_move_y

						self.move_piece(self.source_x, self.source_y, board_x, board_y)
						has_player_moved = True

						# Pawn promotion
						if board_y == self.goal_rank and self.board[board_x][board_y].piece.piece_type == Constants.P_PAWN:
							self.is_board_clickable = False
							self.is_undergoing_promotion = True
							self.source_x = board_x
							self.source_y = board_y

					# User clicked on tile that is not traversable? We cool as long as user didn't click on its own piece.
					else:
						if not is_piece_clicked:
							self.clear_traversable()

				# else: 
				# 	print event

if __name__ == '__main__':
	# test = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
	# test = "7R/7P/5p2/2p3k1/8/7K/1pr5/8 b ---- - 0 65" #promotion test!
	# test = "r5k1/R7/1P4p1/5p1p/2P5/1P6/3p1PPP/3K4 w ---- - 1 33" #temp test!
	# Chesselate(is_player_white=False, cpu_level=2000, fen_string=test).play()
	Chesselate(is_player_white=False, cpu_level=2000).play()
