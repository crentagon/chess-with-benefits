from constants import *
from piece import *
import pygame, time

def run(self):
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

	# Game overrrr
	elif self.is_game_over:
		# Determine the winner
		color_winner = "Stalemate"
		if self.is_user_checkmate:
			color_winner = "Black" if self.is_player_white else "White"
		else:
			color_winner = "White" if self.is_player_white else "Black"

		game_over_text = "Good game."
		game_winner = color_winner+" wins by checkmate!" if not self.is_stalemate else "It's a stalemate!"

		# Options after game
		board_buffer = Constants.BOARD_BUFFER

		# Render the game over text
		rect_w = Constants.AFTERGAME_WIDTH
		rect_h = Constants.AFTERGAME_HEIGHT
		rect_x = Constants.AFTERGAME_COORD[0]

		font_text = game_over_text
		font_color = Constants.CHESSBOARD_WH
		font_size = Constants.GAMEOVER_FONT_SIZE
		font_x = Constants.AFTERGAME_COORD[0] + (rect_w/2)
		font_y = Constants.AFTERGAME_COORD[1] - (Constants.AFTERGAME_HEIGHT*2)

		self.write_text(font_text, font_color, font_size, font_x, font_y)

		# Render the winner text
		font_text = game_winner
		font_color = Constants.CHESSBOARD_WH
		font_size = Constants.GAMEOVER_FONT_SIZE
		font_x = Constants.AFTERGAME_COORD[0] + (rect_w/2)
		font_y = Constants.AFTERGAME_COORD[1] - (Constants.AFTERGAME_HEIGHT*1.5)

		self.write_text(font_text, font_color, font_size, font_x, font_y)

		if self.is_50_move_rule:
			# Render the text
			font_text = "That is, by the 50-move rule!"
			font_color = Constants.CHESSBOARD_WH
			font_size = Constants.GAMEOVER_FONT_SIZE
			font_x = Constants.AFTERGAME_COORD[0] + (rect_w/2)
			font_y = Constants.AFTERGAME_COORD[1] - (Constants.AFTERGAME_HEIGHT)

			self.write_text(font_text, font_color, font_size, font_x, font_y)

		i = 0
		for element in self.aftergame_options:
			# Render the rectangular buttons
			rect_y = Constants.AFTERGAME_COORD[1] + (rect_h + board_buffer)*i
			rect = (rect_x, rect_y, rect_w, rect_h)
			pygame.draw.rect(self.screen, Constants.SIDEBAR_BG, rect, 0)
			pygame.draw.rect(self.screen, Constants.CHESSBOARD_DK, rect, 1)

			font_text = self.aftergame_options[i][0]
			font_color = Constants.CHESSBOARD_DK
			font_size = Constants.ENDGAME_FONT_SIZE
			font_x = (rect_w/2) + rect_x
			font_y = (rect_h/2) + rect_y

			self.write_text(font_text, font_color, font_size, font_x, font_y)
			i = i + 1

		# TO-DO/NOTE: export PGN and save to Database WHEN play again/main menu/close gme clicked

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
			pygame.draw.rect(self.screen, Constants.CHESSBOARD_DK, button_rect, 1)

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
		pygame.draw.rect(self.screen, Constants.BG_CAPTURED, opp_rect, 0)
		pygame.draw.rect(self.screen, Constants.BG_BORDERS, opp_rect, border)
		pygame.draw.rect(self.screen, Constants.BG_CAPTURED, usr_rect, 0)
		pygame.draw.rect(self.screen, Constants.BG_BORDERS, usr_rect, border)

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

		# Constants for this portion: x-coordinate, width and height
		rect_x = cap_x + buff
		rect_w = cap_width
		rect_h = int(rect_w*2.0/3.0)

		# Render stalemate
		if self.is_stalemate or self.is_50_move_rule:
			image_file = "stalemate.png" if self.is_stalemate else "50moverule.png"

			rect_y = opp_y + Constants.MINIBUFFER*3

			image_piece = pygame.image.load(Constants.RESOURCES+image_file)
			image_piece = pygame.transform.scale(image_piece, (rect_w,rect_h))
			piece_rect = image_piece.get_rect()
			piece_rect = piece_rect.move((rect_x, rect_y))
			self.screen.blit(image_piece, piece_rect)

			rect_y = usr_y + Constants.MINIBUFFER*3

			image_piece = pygame.image.load(Constants.RESOURCES+image_file)
			image_piece = pygame.transform.scale(image_piece, (rect_w,rect_h))
			piece_rect = image_piece.get_rect()
			piece_rect = piece_rect.move((rect_x, rect_y))
			self.screen.blit(image_piece, piece_rect)

		else:
			# Render opponent check or checkmate
			if self.is_opponent_checkmate or self.is_opponent_check:
				rect_y = opp_y + Constants.MINIBUFFER*3
				
				image_file = "checkmate.png" if self.is_opponent_checkmate else "check.png"

				image_piece = pygame.image.load(Constants.RESOURCES+image_file)
				image_piece = pygame.transform.scale(image_piece, (rect_w,rect_h))
				piece_rect = image_piece.get_rect()
				piece_rect = piece_rect.move((rect_x, rect_y))
				self.screen.blit(image_piece, piece_rect)

			elif self.is_user_check or self.is_user_checkmate:
				rect_y = usr_y + Constants.MINIBUFFER*3

				image_file = "checkmate.png" if self.is_user_checkmate else "check.png"

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
		pygame.draw.rect(self.screen, Constants.BG_BORDERS, hp_container_opponent_rect, 0)
		pygame.draw.rect(self.screen, Constants.BG_BORDERS, hp_container_opponent_rect, border)
		
		# Render the user's HP text board
		usr_y = usr_y - hp_container_height
		hp_container_user_rect = (cap_x + buff, usr_y + buff, hp_container_width, hp_container_height - border)
		pygame.draw.rect(self.screen, Constants.BG_BORDERS, hp_container_user_rect, 0)
		pygame.draw.rect(self.screen, Constants.BG_BORDERS, hp_container_user_rect, border)

		# Render the text, "HP"
		font_hp = Constants.RESOURCES+Constants.FONT_HP
		basic_font = pygame.font.Font(font_hp, Constants.HP_TEXT_FONT_SIZE)
		hp_text = "HP"
		hp_text_render = basic_font.render(hp_text, True, Constants.WHITE)
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
		pygame.draw.rect(self.screen, Constants.BG_BORDERS, hp_opponent_rect, hp_border_width)
		pygame.draw.rect(self.screen, hp_color_user, hp_user_rect_curr, 0)
		pygame.draw.rect(self.screen, Constants.BG_BORDERS, hp_user_rect, hp_border_width)

		# Rendering "32/40" for the HP
		hp_text_user = str(self.user_hp_current_before)+"/"+str(self.user_hp_max)
		hp_text_opponent = str(self.opponent_hp_current_before)+"/"+str(self.opponent_hp_max)

		font_size = Constants.HP_TEXT_FONT_SIZE
		basic_font = pygame.font.Font(font_hp, font_size)
		hp_user = basic_font.render(hp_text_user, True, Constants.BG_BORDERS)
		hp_opponent = basic_font.render(hp_text_opponent, True, Constants.BG_BORDERS)

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
		pygame.draw.rect(self.screen, Constants.BG_BORDERS, opp_avatar_border_rect, avatar_border_width)
		pygame.draw.rect(self.screen, Constants.BG_BORDERS, user_avatar_border_rect, avatar_border_width)

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

		pygame.draw.rect(self.screen, Constants.BG_BORDERS, name_opp_rect)
		pygame.draw.rect(self.screen, Constants.BG_BORDERS, name_user_rect)
		pygame.draw.rect(self.screen, Constants.BG_BORDERS, name_opp_rect_border, avatar_border_width)
		pygame.draw.rect(self.screen, Constants.BG_BORDERS, name_user_rect_border, avatar_border_width)

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