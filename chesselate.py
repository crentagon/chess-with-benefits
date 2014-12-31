import sys, string, os
import math
import pygame
from pygame import gfxdraw
import Buttons
import time
from subprocess import *
from pieces import *

class Chesselate:

	def __init__(self, is_player_white = True, cpu_level = 2000):
		self.is_player_white = is_player_white
		self.initialize_board()

		# Active turn for the FEN notation
		self.active_turn = 'w'

		# Castling availability for the FEN notation
		self.kingside_white = 'K'
		self.kingside_black = 'k'
		self.queenside_white = 'Q'
		self.queenside_black = 'q'

		# En Passant for the FEN notation
		self.en_passant = '-'

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

		self.cpu_level = cpu_level

		self.screen = pygame.display.set_mode(Constants.SCREENSIZE)
		self.screen.fill(Constants.WHITE)
		pygame.display.flip()

	def initialize_board(self):
		# Board information
		self.board = [[Tile() for i in range(8)] for i in range(8)]

		# self.board[Constants.TILE_E][Constants.TILE_5].set_piece(Piece(Constants.P_ROOK, self.is_player_white, is_user = True))

		for i in range(8):
			# Set the pawns
			self.board[i][Constants.TILE_7].set_piece(Piece(Constants.P_PAWN, not self.is_player_white, is_user = False))
			self.board[i][Constants.TILE_2].set_piece(Piece(Constants.P_PAWN, self.is_player_white, is_user = True))

			# Set the rooks
			if(i == 0 or i == 7):
				self.board[i][Constants.TILE_8].set_piece(Piece(Constants.P_ROOK, not self.is_player_white, is_user = False))
				self.board[i][Constants.TILE_1].set_piece(Piece(Constants.P_ROOK, self.is_player_white, is_user = True))

			# Set the knights
			elif(i == 1 or i == 6):
				self.board[i][Constants.TILE_8].set_piece(Piece(Constants.P_KNIGHT, not self.is_player_white, is_user = False))
				self.board[i][Constants.TILE_1].set_piece(Piece(Constants.P_KNIGHT, self.is_player_white, is_user = True))

			# Set the bishops
			elif(i == 2 or i == 5):
				self.board[i][Constants.TILE_8].set_piece(Piece(Constants.P_BISHOP, not self.is_player_white, is_user = False))
				self.board[i][Constants.TILE_1].set_piece(Piece(Constants.P_BISHOP, self.is_player_white, is_user = True))

			elif(i == 3):
				if(self.is_player_white):
					self.board[i][Constants.TILE_8].set_piece(Piece(Constants.P_QUEEN, not self.is_player_white, is_user = False))
					self.board[i][Constants.TILE_1].set_piece(Piece(Constants.P_QUEEN, self.is_player_white, is_user = True))
				else:
					self.board[i][Constants.TILE_8].set_piece(Piece(Constants.P_KING, not self.is_player_white, is_user = False))
					self.board[i][Constants.TILE_1].set_piece(Piece(Constants.P_KING, self.is_player_white, is_user = True))

			else:
				if(self.is_player_white):
					self.board[i][Constants.TILE_8].set_piece(Piece(Constants.P_KING, not self.is_player_white, is_user = False))
					self.board[i][Constants.TILE_1].set_piece(Piece(Constants.P_KING, self.is_player_white, is_user = True))
				else:
					self.board[i][Constants.TILE_8].set_piece(Piece(Constants.P_QUEEN, not self.is_player_white, is_user = False))
					self.board[i][Constants.TILE_1].set_piece(Piece(Constants.P_QUEEN, self.is_player_white, is_user = True))

	def print_board(self):
		print "==piece_types=="
		for i in range(8):
			for j in range(8):
				if self.board[i][j].get_piece() is not None:
					sys.stdout.write(str(self.board[i][j].get_piece().get_piece_type()))
				else:
					sys.stdout.write("0")
			print ""

		print "==is_user=="
		for i in range(8):
			for j in range(8):
				if self.board[i][j].get_piece() is not None:
					sys.stdout.write("A") if self.board[i][j].get_piece().get_is_user() else sys.stdout.write("E")
				else:
					sys.stdout.write("0")
			print ""

		print "==colors=="
		for i in range(8):
			for j in range(8):
				if self.board[i][j].get_piece() is not None:
					sys.stdout.write("W") if self.board[i][j].get_piece().get_is_white() else sys.stdout.write("B")
				else:
					sys.stdout.write("0")
			print ""

		print "==threat_levels=="
		for i in range(8):
			for j in range(8):
				if self.board[i][j] is not None:
					sys.stdout.write("["+str(self.board[i][j].get_threat_level())+"]")
				else:
					sys.stdout.write("0")
			print ""

	def build_threats(self):
		# Clear threats
		for i in range(8):
			for j in range(8):
				self.board[i][j].set_threat_level(0)

		# Build threats
		for i in range(8):
			for j in range(8):
				tile = self.board[i][7-j]
				piece = tile.get_piece()

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

					if(piece.get_piece_type() == Constants.P_KNIGHT):
						if(is_i_gt_0):
							if(is_7j_lt_6):
								target_tile = self.board[i-1][7-j+2]
								target_tile.set_threat_level(target_tile.get_threat_level() + 1 if piece.get_is_user() else target_tile.get_threat_level() - 1)
							if(is_7j_gt_1):
								target_tile = self.board[i-1][7-j-2]
								target_tile.set_threat_level(target_tile.get_threat_level() + 1 if piece.get_is_user() else target_tile.get_threat_level() - 1)
							
						if(is_i_lt_7):
							if(is_7j_lt_6):
								target_tile = self.board[i+1][7-j+2]
								target_tile.set_threat_level(target_tile.get_threat_level() + 1 if piece.get_is_user() else target_tile.get_threat_level() - 1)
							if(is_7j_gt_1):
								target_tile = self.board[i+1][7-j-2]
								target_tile.set_threat_level(target_tile.get_threat_level() + 1 if piece.get_is_user() else target_tile.get_threat_level() - 1)

							
						if(is_i_gt_1):
							if(is_7j_lt_7):
								target_tile = self.board[i-2][7-j+1]
								target_tile.set_threat_level(target_tile.get_threat_level() + 1 if piece.get_is_user() else target_tile.get_threat_level() - 1)
							if(is_7j_gt_0):
								target_tile = self.board[i-2][7-j-1]
								target_tile.set_threat_level(target_tile.get_threat_level() + 1 if piece.get_is_user() else target_tile.get_threat_level() - 1)

						if(is_i_lt_6):
							if(is_7j_lt_7):
								target_tile = self.board[i+2][7-j+1]
								target_tile.set_threat_level(target_tile.get_threat_level() + 1 if piece.get_is_user() else target_tile.get_threat_level() - 1)
							if(is_7j_gt_0):
								target_tile = self.board[i+2][7-j-1]
								target_tile.set_threat_level(target_tile.get_threat_level() + 1 if piece.get_is_user() else target_tile.get_threat_level() - 1)


					elif(piece.get_piece_type() == Constants.P_BISHOP):
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
									target_tile.set_threat_level(target_tile.get_threat_level() + 1 if piece.get_is_user() else target_tile.get_threat_level() - 1)
									if(target_tile.get_piece() is not None):
										dirNE = False
								else:
									dirNE = False

								if(if_7j_gte_0 and dirSE):
									target_tile = self.board[i+k][7-j-k]
									target_tile.set_threat_level(target_tile.get_threat_level() + 1 if piece.get_is_user() else target_tile.get_threat_level() - 1)
									if(target_tile.get_piece() is not None):
										dirSE = False
								else:
									dirSE = False

							if(is_ik_gte_0):
								if(if_7j_lte_7 and dirNW):
									target_tile = self.board[i-k][7-j+k]
									target_tile.set_threat_level(target_tile.get_threat_level() + 1 if piece.get_is_user() else target_tile.get_threat_level() - 1)
									if(target_tile.get_piece() is not None):
										dirNW = False
								else:
									dirNW = False

								if(if_7j_gte_0 and dirSW):
									target_tile = self.board[i-k][7-j-k]
									target_tile.set_threat_level(target_tile.get_threat_level() + 1 if piece.get_is_user() else target_tile.get_threat_level() - 1)
									if(target_tile.get_piece() is not None):
										dirSW = False
								else:
									dirSW = False

					elif(piece.get_piece_type() == Constants.P_ROOK):
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
								target_tile.set_threat_level(target_tile.get_threat_level() + 1 if piece.get_is_user() else target_tile.get_threat_level() - 1)
								if(target_tile.get_piece() is not None):
									dirE = False
							else:
								dirE = False

							if(is_ik_gte_0 and dirW):
								target_tile = self.board[i-k][7-j]
								target_tile.set_threat_level(target_tile.get_threat_level() + 1 if piece.get_is_user() else target_tile.get_threat_level() - 1)
								if(target_tile.get_piece() is not None):
									dirW = False
							else:
								dirW = False

							if(if_7j_lte_7 and dirN):
								target_tile = self.board[i][7-j+k]
								target_tile.set_threat_level(target_tile.get_threat_level() + 1 if piece.get_is_user() else target_tile.get_threat_level() - 1)
								if(target_tile.get_piece() is not None):
									dirN = False
							else:
								dirN = False

							if(if_7j_gte_0 and dirS):
								target_tile = self.board[i][7-j-k]
								target_tile.set_threat_level(target_tile.get_threat_level() + 1 if piece.get_is_user() else target_tile.get_threat_level() - 1)
								if(target_tile.get_piece() is not None):
									dirS = False
							else:
								dirS = False


					elif(piece.get_piece_type() == Constants.P_QUEEN):
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
								target_tile.set_threat_level(target_tile.get_threat_level() + 1 if piece.get_is_user() else target_tile.get_threat_level() - 1)
								if(target_tile.get_piece() is not None):
									dirE = False
							else:
								dirE = False

							if(is_ik_gte_0 and dirW):
								target_tile = self.board[i-k][7-j]
								target_tile.set_threat_level(target_tile.get_threat_level() + 1 if piece.get_is_user() else target_tile.get_threat_level() - 1)
								if(target_tile.get_piece() is not None):
									dirW = False
							else:
								dirW = False

							if(if_7j_lte_7 and dirN):
								target_tile = self.board[i][7-j+k]
								target_tile.set_threat_level(target_tile.get_threat_level() + 1 if piece.get_is_user() else target_tile.get_threat_level() - 1)
								if(target_tile.get_piece() is not None):
									dirN = False
							else:
								dirN = False

							if(if_7j_gte_0 and dirS):
								target_tile = self.board[i][7-j-k]
								target_tile.set_threat_level(target_tile.get_threat_level() + 1 if piece.get_is_user() else target_tile.get_threat_level() - 1)
								if(target_tile.get_piece() is not None):
									dirS = False
							else:
								dirS = False

							if(is_ik_lte_7):
								if(if_7j_lte_7 and dirNE):
									target_tile = self.board[i+k][7-j+k]
									target_tile.set_threat_level(target_tile.get_threat_level() + 1 if piece.get_is_user() else target_tile.get_threat_level() - 1)
									if(target_tile.get_piece() is not None):
										dirNE = False
								else:
									dirNE = False

								if(if_7j_gte_0 and dirSE):
									target_tile = self.board[i+k][7-j-k]
									target_tile.set_threat_level(target_tile.get_threat_level() + 1 if piece.get_is_user() else target_tile.get_threat_level() - 1)
									if(target_tile.get_piece() is not None):
										dirSE = False
								else:
									dirSE = False

							if(is_ik_gte_0):
								if(if_7j_lte_7 and dirNW):
									target_tile = self.board[i-k][7-j+k]
									target_tile.set_threat_level(target_tile.get_threat_level() + 1 if piece.get_is_user() else target_tile.get_threat_level() - 1)
									if(target_tile.get_piece() is not None):
										dirNW = False
								else:
									dirNW = False

								if(if_7j_gte_0 and dirSW):
									target_tile = self.board[i-k][7-j-k]
									target_tile.set_threat_level(target_tile.get_threat_level() + 1 if piece.get_is_user() else target_tile.get_threat_level() - 1)
									if(target_tile.get_piece() is not None):
										dirSW = False
								else:
									dirSW = False

					elif(piece.get_piece_type() == Constants.P_KING):
						is_i_lte_7 = i+1 <= 7
						is_i_gte_0 = i-1 >= 0
						is_7j_lte_7 = 7-j+1 <= 7
						is_7j_gte_0 = 7-j-1 >= 0

						if(is_i_lte_7):
							target_tile = self.board[i+1][7-j]
							target_tile.set_threat_level(target_tile.get_threat_level() + 1 if piece.get_is_user() else target_tile.get_threat_level() - 1)
							
							if(is_7j_lte_7):
								target_tile = self.board[i+1][7-j+1]
								target_tile.set_threat_level(target_tile.get_threat_level() + 1 if piece.get_is_user() else target_tile.get_threat_level() - 1)
							
							if(is_7j_gte_0):
								target_tile = self.board[i+1][7-j-1]
								target_tile.set_threat_level(target_tile.get_threat_level() + 1 if piece.get_is_user() else target_tile.get_threat_level() - 1)
							
						if(is_i_gte_0):
							target_tile = self.board[i-1][7-j]
							target_tile.set_threat_level(target_tile.get_threat_level() + 1 if piece.get_is_user() else target_tile.get_threat_level() - 1)
							
							if(is_7j_lte_7):
								target_tile = self.board[i-1][7-j+1]
								target_tile.set_threat_level(target_tile.get_threat_level() + 1 if piece.get_is_user() else target_tile.get_threat_level() - 1)
							
							if(is_7j_gte_0):
								target_tile = self.board[i-1][7-j-1]
								target_tile.set_threat_level(target_tile.get_threat_level() + 1 if piece.get_is_user() else target_tile.get_threat_level() - 1)
							
						if(is_7j_lte_7):
							target_tile = self.board[i][7-j+1]
							target_tile.set_threat_level(target_tile.get_threat_level() + 1 if piece.get_is_user() else target_tile.get_threat_level() - 1)
						
						if(is_7j_gte_0):
							target_tile = self.board[i][7-j-1]
							target_tile.set_threat_level(target_tile.get_threat_level() + 1 if piece.get_is_user() else target_tile.get_threat_level() - 1)
							
					elif(piece.get_piece_type() == Constants.P_PAWN):
						is_user = piece.get_is_user()
						if(is_i_lt_7):
							if(is_user and is_7j_lt_7):
								target_tile = self.board[i+1][7-j+1]
								target_tile.set_threat_level(target_tile.get_threat_level() + 1)
							if(not is_user and is_7j_gt_0):
								target_tile = self.board[i+1][7-j-1]
								target_tile.set_threat_level(target_tile.get_threat_level() - 1)

						if(is_i_gt_0):
							if(is_user and is_7j_lt_7):
								target_tile = self.board[i-1][7-j+1]
								target_tile.set_threat_level(target_tile.get_threat_level() + 1)
							if(not is_user and is_7j_gt_0):
								target_tile = self.board[i-1][7-j-1]
								target_tile.set_threat_level(target_tile.get_threat_level() - 1)

	def render_board(self):
		self.screen.fill(Constants.WHITE)

		# Render the board
		pygame.draw.rect(self.screen, Constants.CHESSBOARD_BG, (0, 0, Constants.OUTERBOARD_HEIGHT, Constants.OUTERBOARD_WIDTH), 0)
				
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
				if(j % 2 == 0):
					tile_color = leading_color
				else:
					tile_color = lagging_color

				pygame.draw.rect(self.screen, tile_color, (Constants.BOARD_BUFFER+Constants.TILE_LENGTH*i, Constants.BOARD_BUFFER+Constants.TILE_LENGTH*j, Constants.TILE_LENGTH, Constants.TILE_LENGTH), 0)

				tile = self.board[i][7-j]
				piece = tile.get_piece()

				if(piece is not None):
					# Render the threatened pieces

					# Render the pieces
					piece_rect = (Constants.BOARD_BUFFER+Constants.TILE_LENGTH*i, Constants.BOARD_BUFFER+Constants.TILE_LENGTH*j, Constants.TILE_LENGTH, Constants.TILE_LENGTH)
					piece_type = piece.get_piece_type()
					piece.set_piece_position(piece_rect)

					color = "w" if piece.get_is_white() else "b"
					image_file = color + str(piece_type) + ".png"

					image_piece = pygame.image.load(Constants.RESOURCES+image_file)
					self.screen.blit(image_piece, piece_rect)

				# Render the empty tile threats
				else:
					difference = 15
					threat_level = tile.get_threat_level()
					alpha = 255.0*abs(threat_level)/12.0
					alpha_text = 255.0*abs(threat_level)/10.0

					s = pygame.Surface((Constants.TILE_LENGTH-difference, Constants.TILE_LENGTH-difference))
					s.set_alpha(alpha)

					if(threat_level >= 0):
						color = Constants.BLUE
					else:
						color = Constants.RED

					if(alpha != 0):
						s.fill(color)
						basic_font = pygame.font.SysFont(None, 25)

						threat_text = basic_font.render(str(abs(threat_level)), True, color, tile_color)

						text_rect = threat_text.get_rect()
						text_rect.centerx = Constants.BOARD_BUFFER+(difference/2)+Constants.TILE_LENGTH*i + 5
						text_rect.centery = Constants.BOARD_BUFFER+(difference/2)+Constants.TILE_LENGTH*j + 8

						threat_text.set_alpha(alpha_text)
						self.screen.blit(threat_text, text_rect)

					self.screen.blit(s, (Constants.BOARD_BUFFER+(difference/2)+Constants.TILE_LENGTH*i, Constants.BOARD_BUFFER+(difference/2)+Constants.TILE_LENGTH*j))

				# Render traversibility
				if tile.get_is_traversable():
					circle_x = Constants.BOARD_BUFFER+Constants.TILE_LENGTH*i+Constants.TILE_LENGTH/2
					circle_y = Constants.BOARD_BUFFER+Constants.TILE_LENGTH*j+Constants.TILE_LENGTH/2

					pygame.gfxdraw.filled_circle(self.screen, circle_x, circle_y, Constants.TRAVERSABLE_SEMIRADIUS, Constants.TRAVERSABLE_SEMI)
					pygame.gfxdraw.filled_circle(self.screen, circle_x, circle_y, Constants.TRAVERSABLE_MINIRADIUS, Constants.TRAVERSABLE_MINI)
					# pygame.gfxdraw.filled_circle(self.screen, circle_x, circle_y, Constants.TRAVERSABLE_RADIUS, Constants.TRAVERSABLE_COLOR)
					# pygame.gfxdraw.aacircle(self.screen, circle_x, circle_y, Constants.TRAVERSABLE_SEMIRADIUS, Constants.TRAVERSABLE_BORDER)


		pygame.display.flip()

	def move_piece(self, source_x, source_y, destination_x, destination_y):
		self.board[destination_x][destination_y].set_piece(self.board[source_x][source_y].get_piece())
		self.board[source_x][source_y].remove_piece()

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
				if(self.is_player_white):
					piece = self.board[j][7-i].get_piece()
				else:
					piece = self.board[7-j][i].get_piece()

				if piece is not None:
					if blank is not 0:
						fen_string += str(blank)
						blank = 0
					fen_string += fen_piece[piece.get_piece_type()].upper() if piece.get_is_white() else fen_piece[piece.get_piece_type()]
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
				self.board[x][y].set_is_traversable(False)

	def show_traversable(self, i, j):
		self.clear_traversable()

		piece = self.board[i][j].get_piece()

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

		# Build traversibility:
		# if piece.get_piece_type() == Constants.P_PAWN:
		# 	self.board[i][j+1].set_is_traversable(True)
		# 	if j == Constants.PIECE_MAPPING['2']:
		# 		self.board[i][j+2].set_is_traversable(True)
		
		if piece.get_piece_type() == Constants.P_KNIGHT:
			# This is to prevent the index-out-of-range errors
			if(piece.get_piece_type() == Constants.P_KNIGHT):
				if(is_i_gt_0):
					if(is_7j_lt_6):
						target_tile = self.board[i-1][j+2]
						if(target_tile.get_piece() == None or target_tile.get_piece().get_is_user() == False):
							target_tile.set_is_traversable(True)
					if(is_7j_gt_1):
						target_tile = self.board[i-1][j-2]
						if(target_tile.get_piece() == None or target_tile.get_piece().get_is_user() == False):
							target_tile.set_is_traversable(True)
					
				if(is_i_lt_7):
					if(is_7j_lt_6):
						target_tile = self.board[i+1][j+2]
						if(target_tile.get_piece() == None or target_tile.get_piece().get_is_user() == False):
							target_tile.set_is_traversable(True)
					if(is_7j_gt_1):
						target_tile = self.board[i+1][j-2]
						if(target_tile.get_piece() == None or target_tile.get_piece().get_is_user() == False):
							target_tile.set_is_traversable(True)

					
				if(is_i_gt_1):
					if(is_7j_lt_7):
						target_tile = self.board[i-2][j+1]
						if(target_tile.get_piece() == None or target_tile.get_piece().get_is_user() == False):
							target_tile.set_is_traversable(True)
					if(is_7j_gt_0):
						target_tile = self.board[i-2][j-1]
						if(target_tile.get_piece() == None or target_tile.get_piece().get_is_user() == False):
							target_tile.set_is_traversable(True)

				if(is_i_lt_6):
					if(is_7j_lt_7):
						target_tile = self.board[i+2][j+1]
						if(target_tile.get_piece() == None or target_tile.get_piece().get_is_user() == False):
							target_tile.set_is_traversable(True)
					if(is_7j_gt_0):
						target_tile = self.board[i+2][j-1]
						if(target_tile.get_piece() == None or target_tile.get_piece().get_is_user() == False):
							target_tile.set_is_traversable(True)
		
		elif piece.get_piece_type() == Constants.P_BISHOP:
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
						if(target_tile.get_piece() == None or target_tile.get_piece().get_is_user() == False):
							target_tile.set_is_traversable(True)
							if(target_tile.get_piece() is not None and target_tile.get_piece().get_is_user() == False):
								dirNE = False
						else:
							dirNE = False
					else:
						dirNE = False

					if(if_7j_gte_0 and dirSE):
						target_tile = self.board[i+k][j-k]
						if(target_tile.get_piece() == None or target_tile.get_piece().get_is_user() == False):
							target_tile.set_is_traversable(True)
							if(target_tile.get_piece() is not None and target_tile.get_piece().get_is_user() == False):
								dirSE = False
						else:
							dirSE = False
					else:
						dirSE = False

				if(is_ik_gte_0):
					if(if_7j_lte_7 and dirNW):
						target_tile = self.board[i-k][j+k]
						if(target_tile.get_piece() == None or target_tile.get_piece().get_is_user() == False):
							target_tile.set_is_traversable(True)
							if(target_tile.get_piece() is not None and target_tile.get_piece().get_is_user() == False):
								dirNW = False
						else:
							dirNW = False
					else:
						dirNW = False

					if(if_7j_gte_0 and dirSW):
						target_tile = self.board[i-k][j-k]
						if(target_tile.get_piece() == None or target_tile.get_piece().get_is_user() == False):
							target_tile.set_is_traversable(True)
							if(target_tile.get_piece() is not None and target_tile.get_piece().get_is_user() == False):
								dirSW = False
						else:
							dirSW = False
					else:
						dirSW = False
		
		elif piece.get_piece_type() == Constants.P_ROOK:
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
					if(target_tile.get_piece() == None or target_tile.get_piece().get_is_user() == False):
						target_tile.set_is_traversable(True)
						if(target_tile.get_piece() is not None and target_tile.get_piece().get_is_user() == False):
							dirE = False
					else:
						dirE = False
				else:
					dirE = False

				if(is_ik_gte_0 and dirW):
					target_tile = self.board[i-k][j]
					if(target_tile.get_piece() == None or target_tile.get_piece().get_is_user() == False):
						target_tile.set_is_traversable(True)
						if(target_tile.get_piece() is not None and target_tile.get_piece().get_is_user() == False):
							dirW = False
					else:
						dirW = False
				else:
					dirW = False

				if(if_7j_lte_7 and dirN):
					target_tile = self.board[i][j+k]
					if(target_tile.get_piece() == None or target_tile.get_piece().get_is_user() == False):
						target_tile.set_is_traversable(True)
						if(target_tile.get_piece() is not None and target_tile.get_piece().get_is_user() == False):
							dirN = False
					else:
						dirN = False
				else:
					dirN = False

				if(if_7j_gte_0 and dirS):
					target_tile = self.board[i][j-k]
					if(target_tile.get_piece() == None or target_tile.get_piece().get_is_user() == False):
						target_tile.set_is_traversable(True)
						if(target_tile.get_piece() is not None and target_tile.get_piece().get_is_user() == False):
							dirS = False
					else:
						dirS = False
				else:
					dirS = False
		
		elif piece.get_piece_type() == Constants.P_QUEEN:
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
					if(target_tile.get_piece() == None or target_tile.get_piece().get_is_user() == False):
						target_tile.set_is_traversable(True)
						if(target_tile.get_piece() is not None and target_tile.get_piece().get_is_user() == False):
							dirE = False
					else:
						dirE = False
				else:
					dirE = False

				if(is_ik_gte_0 and dirW):
					target_tile = self.board[i-k][j]
					if(target_tile.get_piece() == None or target_tile.get_piece().get_is_user() == False):
						target_tile.set_is_traversable(True)
						if(target_tile.get_piece() is not None and target_tile.get_piece().get_is_user() == False):
							dirW = False
					else:
						dirW = False
				else:
					dirW = False

				if(if_7j_lte_7 and dirN):
					target_tile = self.board[i][j+k]
					if(target_tile.get_piece() == None or target_tile.get_piece().get_is_user() == False):
						target_tile.set_is_traversable(True)
						if(target_tile.get_piece() is not None and target_tile.get_piece().get_is_user() == False):
							dirN = False
					else:
						dirN = False
				else:
					dirN = False

				if(if_7j_gte_0 and dirS):
					target_tile = self.board[i][j-k]
					if(target_tile.get_piece() == None or target_tile.get_piece().get_is_user() == False):
						target_tile.set_is_traversable(True)
						if(target_tile.get_piece() is not None and target_tile.get_piece().get_is_user() == False):
							dirS = False
					else:
						dirS = False
				else:
					dirS = False

				if(is_ik_lte_7):
					if(if_7j_lte_7 and dirNE):
						target_tile = self.board[i+k][j+k]
						if(target_tile.get_piece() == None or target_tile.get_piece().get_is_user() == False):
							target_tile.set_is_traversable(True)
							if(target_tile.get_piece() is not None and target_tile.get_piece().get_is_user() == False):
								dirNE = False
						else:
							dirNE = False
					else:
						dirNE = False

					if(if_7j_gte_0 and dirSE):
						target_tile = self.board[i+k][j-k]
						if(target_tile.get_piece() == None or target_tile.get_piece().get_is_user() == False):
							target_tile.set_is_traversable(True)
							if(target_tile.get_piece() is not None and target_tile.get_piece().get_is_user() == False):
								dirSE = False
						else:
							dirSE = False
					else:
						dirSE = False

				if(is_ik_gte_0):
					if(if_7j_lte_7 and dirNW):
						target_tile = self.board[i-k][j+k]
						if(target_tile.get_piece() == None or target_tile.get_piece().get_is_user() == False):
							target_tile.set_is_traversable(True)
							if(target_tile.get_piece() is not None and target_tile.get_piece().get_is_user() == False):
								dirNW = False
						else:
							dirNW = False
					else:
						dirNW = False

					if(if_7j_gte_0 and dirSW):
						target_tile = self.board[i-k][j-k]
						if(target_tile.get_piece() == None or target_tile.get_piece().get_is_user() == False):
							target_tile.set_is_traversable(True)
							if(target_tile.get_piece() is not None and target_tile.get_piece().get_is_user() == False):
								dirSW = False
						else:
							dirSW = False
					else:
						dirSW = False
		
		elif piece.get_piece_type() == Constants.P_KING:
			if(is_i_lte_7):
				target_tile = self.board[i+1][j]
				if(target_tile.get_piece() == None or target_tile.get_piece().get_is_user() == False):
					target_tile.set_is_traversable(True)
				
				if(is_7j_lte_7):
					target_tile = self.board[i+1][j+1]
					if(target_tile.get_piece() == None or target_tile.get_piece().get_is_user() == False):
						target_tile.set_is_traversable(True)
				
				if(is_7j_gte_0):
					target_tile = self.board[i+1][j-1]
					if(target_tile.get_piece() == None or target_tile.get_piece().get_is_user() == False):
						target_tile.set_is_traversable(True)
				
			if(is_i_gte_0):
				target_tile = self.board[i-1][j]
				if(target_tile.get_piece() == None or target_tile.get_piece().get_is_user() == False):
					target_tile.set_is_traversable(True)
				
				if(is_7j_lte_7):
					target_tile = self.board[i-1][j+1]
					if(target_tile.get_piece() == None or target_tile.get_piece().get_is_user() == False):
						target_tile.set_is_traversable(True)
				
				if(is_7j_gte_0):
					target_tile = self.board[i-1][j-1]
					if(target_tile.get_piece() == None or target_tile.get_piece().get_is_user() == False):
						target_tile.set_is_traversable(True)
				
			if(is_7j_lte_7):
				target_tile = self.board[i][j+1]
				if(target_tile.get_piece() == None or target_tile.get_piece().get_is_user() == False):
					target_tile.set_is_traversable(True)
			
			if(is_7j_gte_0):
				target_tile = self.board[i][j-1]
				if(target_tile.get_piece() == None or target_tile.get_piece().get_is_user() == False):
					target_tile.set_is_traversable(True)

		elif piece.get_piece_type() == Constants.P_PAWN:
			if(is_7j_lte_7):
				target_tile = self.board[i][j+1]
				if(target_tile.get_piece() == None):
					target_tile.set_is_traversable(True)

			if(j == Constants.PIECE_MAPPING['2']):
				target_tile = self.board[i][j+2]
				if(target_tile.get_piece() == None):
					target_tile.set_is_traversable(True)

			if(is_i_lt_7 and is_7j_lt_7):
				target_tile = self.board[i+1][j+1]
				if(target_tile.get_piece() is not None and target_tile.get_piece().get_is_user() == False):
					target_tile.set_is_traversable(True)

			if(is_i_gt_0 and is_7j_lt_7):
				target_tile = self.board[i-1][j+1]
				if(target_tile.get_piece() is not None and target_tile.get_piece().get_is_user() == False):
					target_tile.set_is_traversable(True)		

	def play(self):
		# self.move_piece("e2", "e4")
		self.build_threats()
		fen = self.convert_to_fen()
		print fen

		# self.print_board()

		has_player_moved = False

		is_turn_user = True if self.is_player_white else False
		is_turn_opponent = False if is_turn_user else True

		while(True):
			self.render_board()

			if has_player_moved:
				self.clear_traversable()
				self.build_threats()
				self.render_board()
				self.active_turn = 'b' if self.is_player_white else 'w'
				has_player_moved = False

				is_turn_user = False
				is_turn_opponent = True

			if is_turn_opponent:
				fen = self.convert_to_fen()
				print fen
				p = Popen( ["stockfish_14053109_32bit.exe"], stdin=PIPE, stdout=PIPE )
				p.stdin.write("position fen " + fen + "\n")
				p.stdin.write("go movetime "+str(self.cpu_level)+"\n")
				time.sleep(self.cpu_level/1000)
				p.stdin.write("quit\n")

				# Retrieving the best move
				x = p.stdout.read().split("\n")
				move_string = x[-2].split(' ')

				cpu_move = move_string[1]
				ponder = move_string[3]

				source_x = Constants.PIECE_MAPPING[cpu_move[:1]]
				source_y = Constants.PIECE_MAPPING[cpu_move[1:2]]
				destination_x = Constants.PIECE_MAPPING[cpu_move[2:3]]
				destination_y = Constants.PIECE_MAPPING[cpu_move[3:4]]

				if not self.is_player_white:
					source_x = 7 - source_x
					source_y = 7 - source_y
					destination_x = 7 - destination_x
					destination_y = 7 - destination_y

				self.move_piece(source_x, source_y, destination_x, destination_y)

				print cpu_move
				print ponder

				is_turn_opponent = False
				is_turn_user = True

				# sys.exit(0)


			events = pygame.event.get()

			for event in events: 
				if event.type == pygame.QUIT: 
					sys.exit(0)

				# User's turn
				elif event.type == 5 and is_turn_user:
					mouse_pos = pygame.mouse.get_pos()
					board_x = (mouse_pos[0] - Constants.BOARD_BUFFER)/Constants.TILE_LENGTH
					board_y = 7-((mouse_pos[1] - Constants.BOARD_BUFFER)/Constants.TILE_LENGTH)

					if 0 <= board_x <= 7 and 0 <= board_y <= 7:
						tile = self.board[board_x][board_y]
						piece = tile.get_piece()

					if piece is not None:
						if piece.pressed(mouse_pos):
							self.source_x = board_x
							self.source_y = board_y
							self.show_traversable(board_x, board_y)

					if tile.get_is_traversable():
						self.move_piece(self.source_x, self.source_y, board_x, board_y)
						has_player_moved = True
						# Store the move in a stack

				# else: 
				# 	print event

if __name__ == '__main__':
	Chesselate(is_player_white=False).play()
