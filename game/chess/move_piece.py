from constants import *
import pygame, math

def run(self, source_x, source_y, destination_x, destination_y, promotion):
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

		# Update FEN Notation for castling if captured piece is a rook
		if captured_piece.piece_type == Constants.P_ROOK:
			if destination_x == Constants.TILE_H:
				if captured_piece.is_white:
					self.kingside_white = '-'
				else:
					self.kingside_black = '-'
			elif destination_x == Constants.TILE_A:
				if captured_piece.is_white:
					self.queenside_white = '-'
				else:
					self.queenside_black = '-'


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

		# print "(", source_coord_x, source_coord_y, ")-->(", destination_coord_x, destination_coord_y, ")"

		is_vertical = destination_coord_x - source_coord_x == 0
		is_horizontal = destination_coord_y - source_coord_y == 0

		m = 0
		b = 0
		if not (is_vertical or is_horizontal):
			m = (destination_coord_y - source_coord_y)*1.0/(destination_coord_x - source_coord_x)
			b = destination_coord_y*1.0 - (m*1.0 * destination_coord_x)

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
				j_after2 = j_before - multiplier

				if i >= 0 and i <= 7:
					if j_before >= 0 and j_before <= 7:
						self.render_tile(i, j_before)
					if j_after >= 0 and j_after <= 7:
						self.render_tile(i, j_after)
					if j_after2 >= 0 and j_after2 <= 7:
						self.render_tile(i, j_after2)

				if multiplier*y < multiplier*destination_coord_y:
					break
			elif is_horizontal:

				x -= multiplier*(increment)

				i_before = int((x - Constants.BOARD_BUFFER)/Constants.TILE_LENGTH)
				i_after = int(i_before + multiplier)
				i_after2 = int(i_before - multiplier)
				j = int((y - Constants.BOARD_BUFFER)/Constants.TILE_LENGTH)
				
				if j >= 0 and j <= 7:
					if i_before >= 0 and i_before <= 7:
						self.render_tile(i_before, j)
						# self.board[i_before][j].is_current_movement = True
					if i_after >= 0 and i_after <= 7:
						self.render_tile(i_after, j)
						# self.board[i_after][j].is_current_movement = True
					if i_after2 >= 0 and i_after2 <= 7:
						self.render_tile(i_after2, j)
						# self.board[i_after][j].is_current_movement = True

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

	self.last_source_x = source_x
	self.last_source_y = source_y
	self.last_destination_x = destination_x
	self.last_destination_y = destination_y

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

	# If it's a king movement, update FEN notation
	if piece.piece_type == Constants.P_KING:
		if piece.is_white:
			self.kingside_white = '-'
			self.queenside_white = '-'
		else:
			self.kingside_black = '-'
			self.queenside_black = '-'

	# If it's a rook movement, update FEN notation
	if piece.piece_type == Constants.P_ROOK:
		if source_x == Constants.TILE_H:
			if piece.is_white:
				self.kingside_white = '-'
			else:
				self.kingside_black = '-'
		elif source_x == Constants.TILE_A:
			if piece.is_white:
				self.queenside_white = '-'
			else:
				self.queenside_black = '-'

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