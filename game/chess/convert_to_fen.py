from constants import *

def run(self):
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
	return fen_string