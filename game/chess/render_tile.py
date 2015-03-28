from pygame import gfxdraw
from constants import *
import pygame

def run(self, i, j):
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

	if tile.is_current_movement:
		thickness = Constants.LAST_MOVEMENT_BORDER_THICKNESS
		decrease = Constants.LAST_MOVEMENT_DECREASE_FACTOR
		coord_buffer = side*(1-decrease)/2
		pygame.draw.rect(self.screen, Constants.CURR_MOVEMENT, (rect_x+coord_buffer, rect_y+coord_buffer, side*decrease, side*decrease), thickness)

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

		pygame.gfxdraw.filled_circle(self.screen, circle_x, circle_y, Constants.TRAVERSABLE_RADIUS, Constants.TRAVERSABLE_BORDER)
		pygame.gfxdraw.filled_circle(self.screen, circle_x, circle_y, Constants.TRAVERSABLE_SEMIRADIUS, Constants.TRAVERSABLE_SEMI)
		pygame.gfxdraw.filled_circle(self.screen, circle_x, circle_y, Constants.TRAVERSABLE_MINIRADIUS, Constants.TRAVERSABLE_MINI)
