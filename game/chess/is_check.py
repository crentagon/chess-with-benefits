from constants import *

# is_check
def run(self, board_input):
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