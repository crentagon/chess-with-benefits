import sys, string, os, threading
import math
import pygame
from pygame import gfxdraw
import time
from subprocess import *
from pieces import *

class Chesselate:

	def __init__(self, is_player_white = True, cpu_level = 2000):
		self.is_player_white = is_player_white
		self.goal_rank = 7
		if not self.is_player_white:
			self.goal_rank = 0

		# Active turn for the FEN notation
		self.active_turn = 'w'

		# Castling availability for the FEN notation
		self.kingside_white = 'K'
		self.kingside_black = 'k'
		self.queenside_white = 'Q'
		self.queenside_black = 'q'

		# En Passant for the FEN notation
		self.en_passant = '-'
		self.is_undergoing_promotion = False

		# Half-move and full-move clock for the FEN notation
		self.halfmove_clock = 0
		self.fullmove_clock = 1

		# Game Window information
		pygame.init()
		pygame.display.set_caption("Chesselate")
		self.clock = pygame.time.Clock()

		# Source move
		self.source_x = 0
		self.source_y = 0

		# Stockfish
		self.cpu_level = cpu_level

		# Board stuff
		self.is_board_clickable = True
		self.initialize_board()

		# Right panel buttons
		self.promotions = {}

		# Debug mode: Disables opponent's moves
		self.debug_mode = True

		self.screen = pygame.display.set_mode(Constants.SCREENSIZE)
		self.screen.fill(Constants.WHITE)
		pygame.display.flip()

	def initialize_board(self):
		# Board information
		self.board = [[Tile() for i in range(8)] for i in range(8)]

		testing = 0

		# En Passant test
		if testing == 10:
			self.en_passant = "d6"
			self.board[Constants.TILE_D][Constants.TILE_5].piece = Piece(Constants.P_PAWN, is_white=False, is_user = not self.is_player_white)
			self.board[Constants.TILE_E][Constants.TILE_5].piece = Piece(Constants.P_PAWN, is_white=True, is_user = self.is_player_white)
			self.board[Constants.TILE_A][Constants.TILE_8].piece = Piece(Constants.P_KING, is_white=False, is_user = not self.is_player_white)
			self.board[Constants.TILE_H][Constants.TILE_8].piece = Piece(Constants.P_KING, is_white=True, is_user = self.is_player_white)

		# elif testing == 20:
		# self.board[Constants.TILE_D][Constants.TILE_7].piece = Piece(Constants.P_PAWN, is_white=True, is_user = self.is_player_white)

		elif testing == 0:
			for i in range(8):
				# Set the pawns
				self.board[i][Constants.TILE_7].piece = Piece(Constants.P_PAWN, is_white=False, is_user = not self.is_player_white)
				self.board[i][Constants.TILE_2].piece = Piece(Constants.P_PAWN, is_white=True, is_user = self.is_player_white)

				# Set the rooks
				if(i == 0 or i == 7):
					self.board[i][Constants.TILE_8].piece = Piece(Constants.P_ROOK, is_white=False, is_user = not self.is_player_white)
					self.board[i][Constants.TILE_1].piece = Piece(Constants.P_ROOK, is_white=True, is_user = self.is_player_white)

				# Set the knights
				elif(i == 1 or i == 6):
					self.board[i][Constants.TILE_8].piece = Piece(Constants.P_KNIGHT, is_white=False, is_user = not self.is_player_white)
					self.board[i][Constants.TILE_1].piece = Piece(Constants.P_KNIGHT, is_white=True, is_user = self.is_player_white)

				# Set the bishops
				elif(i == 2 or i == 5):
					self.board[i][Constants.TILE_8].piece = Piece(Constants.P_BISHOP, is_white=False, is_user = not self.is_player_white)
					self.board[i][Constants.TILE_1].piece = Piece(Constants.P_BISHOP, is_white=True, is_user = self.is_player_white)

				elif(i == 3):
					self.board[i][Constants.TILE_8].piece = Piece(Constants.P_QUEEN, is_white=False, is_user = not self.is_player_white)
					self.board[i][Constants.TILE_1].piece = Piece(Constants.P_QUEEN, is_white=True, is_user = self.is_player_white)
					
				else:
					self.board[i][Constants.TILE_8].piece = Piece(Constants.P_KING, is_white=False, is_user = not self.is_player_white)
					self.board[i][Constants.TILE_1].piece = Piece(Constants.P_KING, is_white=True, is_user = self.is_player_white)
			
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

		print "==threat_levels=="
		for i in range(8):
			for j in range(8):
				if self.board[i][j] is not None:
					sys.stdout.write("["+str(self.board[i][j].threat_level)+"]")
				else:
					sys.stdout.write("0")
			print ""

	def build_threats(self):
		# Clear threats
		for i in range(8):
			for j in range(8):
				self.board[i][j].threat_level_user = 0
				self.board[i][j].threat_level_opponent = 0

		# Build threats
		for i in range(8):
			for j in range(8):
				tile = self.board[i][7-j]
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
								target_tile = self.board[i-1][7-j+2]
								if is_user:
									target_tile.threat_level_user += 1
								else:
									target_tile.threat_level_opponent += 1
							if(is_7j_gt_1):
								target_tile = self.board[i-1][7-j-2]
								if is_user:
									target_tile.threat_level_user += 1
								else:
									target_tile.threat_level_opponent += 1
							
						if(is_i_lt_7):
							if(is_7j_lt_6):
								target_tile = self.board[i+1][7-j+2]
								if is_user:
									target_tile.threat_level_user += 1
								else:
									target_tile.threat_level_opponent += 1
							if(is_7j_gt_1):
								target_tile = self.board[i+1][7-j-2]
								if is_user:
									target_tile.threat_level_user += 1
								else:
									target_tile.threat_level_opponent += 1

							
						if(is_i_gt_1):
							if(is_7j_lt_7):
								target_tile = self.board[i-2][7-j+1]
								if is_user:
									target_tile.threat_level_user += 1
								else:
									target_tile.threat_level_opponent += 1
							if(is_7j_gt_0):
								target_tile = self.board[i-2][7-j-1]
								if is_user:
									target_tile.threat_level_user += 1
								else:
									target_tile.threat_level_opponent += 1

						if(is_i_lt_6):
							if(is_7j_lt_7):
								target_tile = self.board[i+2][7-j+1]
								if is_user:
									target_tile.threat_level_user += 1
								else:
									target_tile.threat_level_opponent += 1
							if(is_7j_gt_0):
								target_tile = self.board[i+2][7-j-1]
								if is_user:
									target_tile.threat_level_user += 1
								else:
									target_tile.threat_level_opponent += 1

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
									target_tile = self.board[i+k][7-j+k]
									if is_user:
										target_tile.threat_level_user += 1
									else:
										target_tile.threat_level_opponent += 1
									if(target_tile.piece is not None):
										dirNE = False
								else:
									dirNE = False

								if(if_7j_gte_0 and dirSE):
									target_tile = self.board[i+k][7-j-k]
									if is_user:
										target_tile.threat_level_user += 1
									else:
										target_tile.threat_level_opponent += 1
									if(target_tile.piece is not None):
										dirSE = False
								else:
									dirSE = False

							if(is_ik_gte_0):
								if(if_7j_lte_7 and dirNW):
									target_tile = self.board[i-k][7-j+k]
									if is_user:
										target_tile.threat_level_user += 1
									else:
										target_tile.threat_level_opponent += 1
									if(target_tile.piece is not None):
										dirNW = False
								else:
									dirNW = False

								if(if_7j_gte_0 and dirSW):
									target_tile = self.board[i-k][7-j-k]
									if is_user:
										target_tile.threat_level_user += 1
									else:
										target_tile.threat_level_opponent += 1
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
								target_tile = self.board[i+k][7-j]
								if is_user:
									target_tile.threat_level_user += 1
								else:
									target_tile.threat_level_opponent += 1
								if(target_tile.piece is not None):
									dirE = False
							else:
								dirE = False

							if(is_ik_gte_0 and dirW):
								target_tile = self.board[i-k][7-j]
								if is_user:
									target_tile.threat_level_user += 1
								else:
									target_tile.threat_level_opponent += 1
								if(target_tile.piece is not None):
									dirW = False
							else:
								dirW = False

							if(if_7j_lte_7 and dirN):
								target_tile = self.board[i][7-j+k]
								if is_user:
									target_tile.threat_level_user += 1
								else:
									target_tile.threat_level_opponent += 1
								if(target_tile.piece is not None):
									dirN = False
							else:
								dirN = False

							if(if_7j_gte_0 and dirS):
								target_tile = self.board[i][7-j-k]
								if is_user:
									target_tile.threat_level_user += 1
								else:
									target_tile.threat_level_opponent += 1
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
								target_tile = self.board[i+k][7-j]
								if is_user:
									target_tile.threat_level_user += 1
								else:
									target_tile.threat_level_opponent += 1
								if(target_tile.piece is not None):
									dirE = False
							else:
								dirE = False

							if(is_ik_gte_0 and dirW):
								target_tile = self.board[i-k][7-j]
								if is_user:
									target_tile.threat_level_user += 1
								else:
									target_tile.threat_level_opponent += 1
								if(target_tile.piece is not None):
									dirW = False
							else:
								dirW = False

							if(if_7j_lte_7 and dirN):
								target_tile = self.board[i][7-j+k]
								if is_user:
									target_tile.threat_level_user += 1
								else:
									target_tile.threat_level_opponent += 1
								if(target_tile.piece is not None):
									dirN = False
							else:
								dirN = False

							if(if_7j_gte_0 and dirS):
								target_tile = self.board[i][7-j-k]
								if is_user:
									target_tile.threat_level_user += 1
								else:
									target_tile.threat_level_opponent += 1
								if(target_tile.piece is not None):
									dirS = False
							else:
								dirS = False

							if(is_ik_lte_7):
								if(if_7j_lte_7 and dirNE):
									target_tile = self.board[i+k][7-j+k]
									if is_user:
										target_tile.threat_level_user += 1
									else:
										target_tile.threat_level_opponent += 1
									if(target_tile.piece is not None):
										dirNE = False
								else:
									dirNE = False

								if(if_7j_gte_0 and dirSE):
									target_tile = self.board[i+k][7-j-k]
									if is_user:
										target_tile.threat_level_user += 1
									else:
										target_tile.threat_level_opponent += 1
									if(target_tile.piece is not None):
										dirSE = False
								else:
									dirSE = False

							if(is_ik_gte_0):
								if(if_7j_lte_7 and dirNW):
									target_tile = self.board[i-k][7-j+k]
									if is_user:
										target_tile.threat_level_user += 1
									else:
										target_tile.threat_level_opponent += 1
									if(target_tile.piece is not None):
										dirNW = False
								else:
									dirNW = False

								if(if_7j_gte_0 and dirSW):
									target_tile = self.board[i-k][7-j-k]
									if is_user:
										target_tile.threat_level_user += 1
									else:
										target_tile.threat_level_opponent += 1
									if(target_tile.piece is not None):
										dirSW = False
								else:
									dirSW = False

					elif(piece_type == Constants.P_KING):
						is_i_lte_7 = i+1 <= 7
						is_i_gte_0 = i-1 >= 0
						is_7j_lte_7 = 7-j+1 <= 7
						is_7j_gte_0 = 7-j-1 >= 0

						if(is_i_lte_7):
							target_tile = self.board[i+1][7-j]
							if is_user:
								target_tile.threat_level_user += 1
							else:
								target_tile.threat_level_opponent += 1
							
							if(is_7j_lte_7):
								target_tile = self.board[i+1][7-j+1]
								if is_user:
									target_tile.threat_level_user += 1
								else:
									target_tile.threat_level_opponent += 1
							
							if(is_7j_gte_0):
								target_tile = self.board[i+1][7-j-1]
								if is_user:
									target_tile.threat_level_user += 1
								else:
									target_tile.threat_level_opponent += 1
							
						if(is_i_gte_0):
							target_tile = self.board[i-1][7-j]
							if is_user:
								target_tile.threat_level_user += 1
							else:
								target_tile.threat_level_opponent += 1
							
							if(is_7j_lte_7):
								target_tile = self.board[i-1][7-j+1]
								if is_user:
									target_tile.threat_level_user += 1
								else:
									target_tile.threat_level_opponent += 1
							
							if(is_7j_gte_0):
								target_tile = self.board[i-1][7-j-1]
								if is_user:
									target_tile.threat_level_user += 1
								else:
									target_tile.threat_level_opponent += 1
							
						if(is_7j_lte_7):
							target_tile = self.board[i][7-j+1]
							if is_user:
								target_tile.threat_level_user += 1
							else:
								target_tile.threat_level_opponent += 1
						
						if(is_7j_gte_0):
							target_tile = self.board[i][7-j-1]
							if is_user:
								target_tile.threat_level_user += 1
							else:
								target_tile.threat_level_opponent += 1
							
					elif(piece_type == Constants.P_PAWN):
						is_white = piece.is_white
						factor = 1 if is_user else -1

						if is_white:
							if(is_i_lt_7 and is_7j_lt_7):
								target_tile = self.board[i+1][7-j+1]
								if is_user:
									target_tile.threat_level_user += 1
								else:
									target_tile.threat_level_opponent += 1

							if(is_i_gt_0 and is_7j_lt_7):
								target_tile = self.board[i-1][7-j+1]
								if is_user:
									target_tile.threat_level_user += 1
								else:
									target_tile.threat_level_opponent += 1

						else:
							if(is_i_lt_7 and is_7j_gt_0):
								target_tile = self.board[i+1][7-j-1]
								if is_user:
									target_tile.threat_level_user += 1
								else:
									target_tile.threat_level_opponent += 1
							if(is_i_gt_0 and is_7j_gt_0):
								target_tile = self.board[i-1][7-j-1]
								if is_user:
									target_tile.threat_level_user += 1
								else:
									target_tile.threat_level_opponent += 1

	def render_board(self):
		self.screen.fill(Constants.BG)
		font = Constants.RESOURCES+Constants.FONT
		font_reg = Constants.RESOURCES+Constants.FONT_REG

		# Render the board
		pygame.draw.rect(self.screen, Constants.CHESSBOARD_BG, (0, 0, Constants.OUTERBOARD_HEIGHT, Constants.OUTERBOARD_WIDTH), 0)
		
		if self.is_undergoing_promotion:

			# Promotion buttons
			promotionable_pieces = [Constants.P_KNIGHT, Constants.P_BISHOP, Constants.P_ROOK, Constants.P_QUEEN]
			color = "w" if self.is_player_white else "b"

			for i in range(2):
				for j in range(2):
					rect_x = Constants.PROMOTION_COORD[0] + (i-1)*(Constants.TILE_LENGTH + Constants.BOARD_BUFFER)
					rect_y = Constants.BOARD_BUFFER*3 + Constants.PROMOTION_COORD[1] + (Constants.TILE_LENGTH + Constants.BOARD_BUFFER)*j
					size = Constants.TILE_LENGTH

					image_file = color + str(promotionable_pieces[i*2+j]) + ".png"
					image_piece = pygame.image.load(Constants.RESOURCES+image_file)

					piece_rect = (rect_x, rect_y, size, size)
					self.screen.blit(image_piece, piece_rect)

					piece = Piece(promotionable_pieces[i*2+j], is_white=self.is_player_white, is_user = True)
					piece.piece_position = piece_rect

					self.promotions[i*2+j] = piece

			# Promotion text
			char_text = "Select a piece to promote to:"
			basic_font = pygame.font.Font(font, 20)
			promotion_text = basic_font.render(char_text, True, Constants.WHITE)

			promotion_rect = promotion_text.get_rect()
			promotion_rect.center = Constants.PROMOTION_COORD

			self.screen.blit(promotion_text, promotion_rect)

		# Render board contents
		for i in range(8):
			if(i % 2 == 0):
				leading_color = Constants.CHESSBOARD_WH
				lagging_color = Constants.CHESSBOARD_DK
			else:
				leading_color = Constants.CHESSBOARD_DK
				lagging_color = Constants.CHESSBOARD_WH

			for j in range(8):
				# Render the tile
				tile_color = leading_color if j % 2 == 0 else lagging_color

				rect_x = Constants.BOARD_BUFFER+Constants.TILE_LENGTH*i
				rect_y = Constants.BOARD_BUFFER+Constants.TILE_LENGTH*j
				side = Constants.TILE_LENGTH
				pygame.draw.rect(self.screen, tile_color, (rect_x, rect_y, side, side), 0)

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
					if ((cumulative_threat < 0 and piece.is_user) or (cumulative_threat > 0 and not piece.is_user)):
						render_threats = True
						is_urgent = True

				# Render the empty tile threats
				else:
					render_threats = True

				if render_threats:
					difference = 15
					alpha = 0
					basic_font = pygame.font.Font(font_reg, 20)

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
						# threat_string = "("+str(threat_level_opponent)+")"
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

					s = pygame.Surface((Constants.TILE_LENGTH-difference, Constants.TILE_LENGTH-difference))
					s.set_alpha(alpha)

					if(alpha != 0):
						s.fill(color)
						alpha_text = alpha * 1.5 if alpha * 1.5 < 255 else 255
						threat_text = basic_font.render(threat_string, True, color, tile_color)

						text_rect = threat_text.get_rect()
						text_rect.centerx = Constants.BOARD_BUFFER+(difference/2)+Constants.TILE_LENGTH*i + 5
						text_rect.centery = Constants.BOARD_BUFFER+(difference/2)+Constants.TILE_LENGTH*j + 8

						threat_text.set_alpha(alpha_text)
						self.screen.blit(threat_text, text_rect)

					self.screen.blit(s, (Constants.BOARD_BUFFER+(difference/2)+Constants.TILE_LENGTH*i, Constants.BOARD_BUFFER+(difference/2)+Constants.TILE_LENGTH*j))

				# Render traversibility
				if tile.is_traversable:
					circle_x = Constants.BOARD_BUFFER+Constants.TILE_LENGTH*i+Constants.TILE_LENGTH/2
					circle_y = Constants.BOARD_BUFFER+Constants.TILE_LENGTH*j+Constants.TILE_LENGTH/2

					pygame.gfxdraw.filled_circle(self.screen, circle_x, circle_y, Constants.TRAVERSABLE_SEMIRADIUS, Constants.TRAVERSABLE_SEMI)
					pygame.gfxdraw.filled_circle(self.screen, circle_x, circle_y, Constants.TRAVERSABLE_MINIRADIUS, Constants.TRAVERSABLE_MINI)

				# Render the board guide
				if j == 0:
					if self.is_player_white:
						num_text = Constants.NUM_MAPPING[7-i]
						char_text = Constants.CHAR_MAPPING[i]
					else:
						num_text = Constants.NUM_MAPPING[i]
						char_text = Constants.CHAR_MAPPING[7-i]

					basic_font = pygame.font.SysFont(font, 15)
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

	def move_piece(self, source_x, source_y, destination_x, destination_y):
		# Flag for checking if the move is a capture
		is_capture = self.board[destination_x][destination_y].piece is not None
		
		# Move the piece in the game
		self.board[destination_x][destination_y].piece = self.board[source_x][source_y].piece

		# self.board[destination_x][destination_y].set_piece(self.board[source_x][source_y].piece)
		self.board[source_x][source_y].remove_piece()

		piece = self.board[destination_x][destination_y].piece

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

		# print fen_string
		# sys.exit(0)

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
			# This is to prevent the index-out-of-range errors
			if(piece.piece_type == Constants.P_KNIGHT):
				if(is_i_gt_0):
					if(is_7j_lt_6):
						target_tile = self.board[i-1][j+2]
						if(target_tile.piece == None or target_tile.piece.is_user == False):
							target_tile.is_traversable = True
					if(is_7j_gt_1):
						target_tile = self.board[i-1][j-2]
						if(target_tile.piece == None or target_tile.piece.is_user == False):
							target_tile.is_traversable = True
					
				if(is_i_lt_7):
					if(is_7j_lt_6):
						target_tile = self.board[i+1][j+2]
						if(target_tile.piece == None or target_tile.piece.is_user == False):
							target_tile.is_traversable = True
					if(is_7j_gt_1):
						target_tile = self.board[i+1][j-2]
						if(target_tile.piece == None or target_tile.piece.is_user == False):
							target_tile.is_traversable = True

					
				if(is_i_gt_1):
					if(is_7j_lt_7):
						target_tile = self.board[i-2][j+1]
						if(target_tile.piece == None or target_tile.piece.is_user == False):
							target_tile.is_traversable = True
					if(is_7j_gt_0):
						target_tile = self.board[i-2][j-1]
						if(target_tile.piece == None or target_tile.piece.is_user == False):
							target_tile.is_traversable = True

				if(is_i_lt_6):
					if(is_7j_lt_7):
						target_tile = self.board[i+2][j+1]
						if(target_tile.piece == None or target_tile.piece.is_user == False):
							target_tile.is_traversable = True
					if(is_7j_gt_0):
						target_tile = self.board[i+2][j-1]
						if(target_tile.piece == None or target_tile.piece.is_user == False):
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
						if(target_tile.piece == None or target_tile.piece.is_user == False):
							target_tile.is_traversable = True
							if(target_tile.piece is not None and target_tile.piece.is_user == False):
								dirNE = False
						else:
							dirNE = False
					else:
						dirNE = False

					if(if_7j_gte_0 and dirSE):
						target_tile = self.board[i+k][j-k]
						if(target_tile.piece == None or target_tile.piece.is_user == False):
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
						if(target_tile.piece == None or target_tile.piece.is_user == False):
							target_tile.is_traversable = True
							if(target_tile.piece is not None and target_tile.piece.is_user == False):
								dirNW = False
						else:
							dirNW = False
					else:
						dirNW = False

					if(if_7j_gte_0 and dirSW):
						target_tile = self.board[i-k][j-k]
						if(target_tile.piece == None or target_tile.piece.is_user == False):
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
					if(target_tile.piece == None or target_tile.piece.is_user == False):
						target_tile.is_traversable = True
						if(target_tile.piece is not None and target_tile.piece.is_user == False):
							dirE = False
					else:
						dirE = False
				else:
					dirE = False

				if(is_ik_gte_0 and dirW):
					target_tile = self.board[i-k][j]
					if(target_tile.piece == None or target_tile.piece.is_user == False):
						target_tile.is_traversable = True
						if(target_tile.piece is not None and target_tile.piece.is_user == False):
							dirW = False
					else:
						dirW = False
				else:
					dirW = False

				if(if_7j_lte_7 and dirN):
					target_tile = self.board[i][j+k]
					if(target_tile.piece == None or target_tile.piece.is_user == False):
						target_tile.is_traversable = True
						if(target_tile.piece is not None and target_tile.piece.is_user == False):
							dirN = False
					else:
						dirN = False
				else:
					dirN = False

				if(if_7j_gte_0 and dirS):
					target_tile = self.board[i][j-k]
					if(target_tile.piece == None or target_tile.piece.is_user == False):
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
					if(target_tile.piece == None or target_tile.piece.is_user == False):
						target_tile.is_traversable = True
						if(target_tile.piece is not None and target_tile.piece.is_user == False):
							dirE = False
					else:
						dirE = False
				else:
					dirE = False

				if(is_ik_gte_0 and dirW):
					target_tile = self.board[i-k][j]
					if(target_tile.piece == None or target_tile.piece.is_user == False):
						target_tile.is_traversable = True
						if(target_tile.piece is not None and target_tile.piece.is_user == False):
							dirW = False
					else:
						dirW = False
				else:
					dirW = False

				if(if_7j_lte_7 and dirN):
					target_tile = self.board[i][j+k]
					if(target_tile.piece == None or target_tile.piece.is_user == False):
						target_tile.is_traversable = True
						if(target_tile.piece is not None and target_tile.piece.is_user == False):
							dirN = False
					else:
						dirN = False
				else:
					dirN = False

				if(if_7j_gte_0 and dirS):
					target_tile = self.board[i][j-k]
					if(target_tile.piece == None or target_tile.piece.is_user == False):
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
						if(target_tile.piece == None or target_tile.piece.is_user == False):
							target_tile.is_traversable = True
							if(target_tile.piece is not None and target_tile.piece.is_user == False):
								dirNE = False
						else:
							dirNE = False
					else:
						dirNE = False

					if(if_7j_gte_0 and dirSE):
						target_tile = self.board[i+k][j-k]
						if(target_tile.piece == None or target_tile.piece.is_user == False):
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
						if(target_tile.piece == None or target_tile.piece.is_user == False):
							target_tile.is_traversable = True
							if(target_tile.piece is not None and target_tile.piece.is_user == False):
								dirNW = False
						else:
							dirNW = False
					else:
						dirNW = False

					if(if_7j_gte_0 and dirSW):
						target_tile = self.board[i-k][j-k]
						if(target_tile.piece == None or target_tile.piece.is_user == False):
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
				if(target_tile.threat_level_opponent <= 0 and (target_tile.piece == None or target_tile.piece.is_user == False)):
					target_tile.is_traversable = True
				
				if(is_7j_lte_7):
					target_tile = self.board[i+1][j+1]
					if(target_tile.threat_level_opponent <= 0 and (target_tile.piece == None or target_tile.piece.is_user == False)):
						target_tile.is_traversable = True
				
				if(is_7j_gte_0):
					target_tile = self.board[i+1][j-1]
					if(target_tile.threat_level_opponent <= 0 and (target_tile.piece == None or target_tile.piece.is_user == False)):
						target_tile.is_traversable = True
				
			if(is_i_gte_0):
				target_tile = self.board[i-1][j]
				if(target_tile.threat_level_opponent <= 0 and (target_tile.piece == None or target_tile.piece.is_user == False)):
					target_tile.is_traversable = True
				
				if(is_7j_lte_7):
					target_tile = self.board[i-1][j+1]
					if(target_tile.threat_level_opponent <= 0 and (target_tile.piece == None or target_tile.piece.is_user == False)):
						target_tile.is_traversable = True
				
				if(is_7j_gte_0):
					target_tile = self.board[i-1][j-1]
					if(target_tile.threat_level_opponent <= 0 and (target_tile.piece == None or target_tile.piece.is_user == False)):
						target_tile.is_traversable = True
				
			if(is_7j_lte_7):
				target_tile = self.board[i][j+1]
				if(target_tile.threat_level_opponent <= 0 and (target_tile.piece == None or target_tile.piece.is_user == False)):
					target_tile.is_traversable = True
			
			if(is_7j_gte_0):
				target_tile = self.board[i][j-1]
				if(target_tile.threat_level_opponent <= 0 and (target_tile.piece == None or target_tile.piece.is_user == False)):
					target_tile.is_traversable = True

			# Castling
			if not piece.is_moved and self.board[i][j].threat_level_opponent <= 0:
				can_castle_kingside = True
				can_castle_queenside = True

				rank = Constants.TILE_8
				if piece.is_white:
					rank = Constants.TILE_1

				kingside_rook = not self.board[Constants.TILE_H][rank].piece.is_moved
				queenside_rook = not self.board[Constants.TILE_A][rank].piece.is_moved
				
				if kingside_rook or queenside_rook:
					for k in range(1,3):
						if can_castle_kingside and kingside_rook:
							kingside_tile = self.board[i+k][rank]
							if kingside_tile.piece is not None or kingside_tile.threat_level_opponent > 0:
								can_castle_kingside = False

						if can_castle_queenside and queenside_rook:
							queenside_tile = self.board[i-k][rank]
							if queenside_tile.piece is not None or queenside_tile.threat_level_opponent > 0:
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
				if(target_tile.piece == None):
					target_tile.is_traversable = True

				# That movement from where the pawn moves two spaces. I don't know what it's called
				start_rank = Constants.PIECE_MAPPING['2'] if self.is_player_white else Constants.PIECE_MAPPING['7']
				if(j == start_rank and self.board[i][j+factor].piece == None):
					target_tile = self.board[i][j+factor*2]
					if(target_tile.piece == None):
						target_tile.is_traversable = True

				# Pawn's doing a capture!
				if(is_i_lt_7 and is_7j_lt_7):
					target_tile = self.board[i+1][j+factor*1]
					if(target_tile.piece is not None and target_tile.piece.is_user == False):
						target_tile.is_traversable = True

				if(is_i_gt_0 and is_7j_lt_7):
					target_tile = self.board[i-1][j+factor*1]
					if(target_tile.piece is not None and target_tile.piece.is_user == False):
						target_tile.is_traversable = True
			
 
			# En Passant
			if self.en_passant != '-' :
				target_tile_x = Constants.PIECE_MAPPING[self.en_passant[0]]
				target_tile_y = Constants.PIECE_MAPPING[self.en_passant[1]]
				
				factor = 1
				if not self.is_player_white:
					factor = -1

				if j == target_tile_y - factor and (i == target_tile_x + factor or i == target_tile_x - factor):
					target_tile = self.board[target_tile_x][target_tile_y]
					target_tile.is_traversable = True

	def play(self):
		# self.move_piece("e2", "e4")
		self.build_threats()
		fen = self.convert_to_fen()
		print fen

		# self.print_board()

		has_player_moved = False
		has_opponent_moved = False

		is_turn_user = True if self.is_player_white else False
		is_turn_opponent = False if is_turn_user else True
		thread = None

		while(True):			
			self.render_board()
			
			if has_player_moved or has_opponent_moved:
				self.clear_traversable()
				self.build_threats()
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

			if self.debug_mode:
				is_turn_opponent = False
				is_turn_user = True

			# Opponent's Turn
			if not self.debug_mode and is_turn_opponent:
				fen_string = self.convert_to_fen()
				print fen_string
				thread = StockfishThread(fen_string, self.cpu_level)

				thread.start()
				is_turn_opponent = False

			if thread is not None and thread.is_thread_done is not None and thread.is_thread_done:

				thread.join()
				cpu_move = thread.cpu_move
				ponder = thread.ponder

				print cpu_move
				print ponder

				source_x = Constants.PIECE_MAPPING[cpu_move[:1]]
				source_y = Constants.PIECE_MAPPING[cpu_move[1:2]]
				destination_x = Constants.PIECE_MAPPING[cpu_move[2:3]]
				destination_y = Constants.PIECE_MAPPING[cpu_move[3:4]]

				if len(cpu_move) == 5:
					promotion = cpu_move[4:5]
					promotion_map = {
						"r": Constants.P_ROOK,
						"b": Constants.P_BISHOP,
						"n": Constants.P_KNIGHT,
						"q": Constants.P_QUEEN
					}
					self.board[destination_x][destination_y].piece.piece_type = promotion_map[promotion]

				else:
					self.move_piece(source_x, source_y, destination_x, destination_y)

				has_opponent_moved = True
				thread.is_thread_done = False

			events = pygame.event.get()
			for event in events: 
				if event.type == pygame.QUIT: 
					sys.exit(0)

				# User's turn
				elif event.type == 5 and is_turn_user:
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
					if 0 <= board_x <= 7 and 0 <= board_y <= 7 and self.is_board_clickable:
						# What did the user click? A piece? A tile? Is the tile traversable?
						tile = self.board[board_x][board_y]
						piece = tile.piece
						is_traversable = tile.is_traversable
						is_piece_clicked = piece is not None

					# The user clicked somewhere else!
					else:
						# Is the user clicking on the promotion buttons?
						for i in range(4):
							if self.is_undergoing_promotion and self.promotions[i].pressed(mouse_pos):
								promotion = self.promotions[i].piece_type

								if promotion != '':
									self.board[self.source_x][self.source_y].piece.piece_type = promotion
									self.is_board_clickable = True
									self.is_undergoing_promotion = False

								has_player_moved = True
								break

					# A piece has been clicked!
					if is_piece_clicked and self.is_board_clickable:
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
						self.move_piece(self.source_x, self.source_y, board_x, board_y)
						has_player_moved = True

						# Pawn promotion
						if board_y == self.goal_rank and self.board[board_x][board_y].piece.piece_type == Constants.P_PAWN:
							self.is_board_clickable = False
							self.is_undergoing_promotion = True
							self.source_x = board_x
							self.source_y = board_y

						# To-do: Store the move in a stack

					# User clicked on tile that is not traversable? We cool as long as user didn't click on its own piece.
					else:

						# tile = self.board[board_x][board_y]
						# piece = tile.piece

						# threat_level_user = tile.threat_level_user
						# threat_level_opponent = tile.threat_level_opponent
						# cumulative_threat = threat_level_user - threat_level_opponent

						# print "Cumulative threat of tile: ", cumulative_threat
						# print "Threat level opponent: ", threat_level_opponent
						# print "Threat level user: ", threat_level_user
						# print "---"

						if not is_piece_clicked:
							self.clear_traversable()

				# else: 
				# 	print event

if __name__ == '__main__':
	Chesselate(is_player_white=True, cpu_level=2000).play()
