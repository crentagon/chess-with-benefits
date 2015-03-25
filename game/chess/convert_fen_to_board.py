from constants import *
from piece import *

def run(self, fen_string, is_init):
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