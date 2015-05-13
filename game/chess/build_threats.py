from constants import *

# build_threats
def run(self, board_input, peek):
	# Clear threats
	for i in range(8):
		for j in range(8):
			board_input[i][j].threat_level_user = 0
			board_input[i][j].threat_level_opponent = 0

	# Build threats
	for i in range(8):
		for j in range(8):
			target_tiles = []
			tile = board_input[i][j]
			piece = tile.piece

			if(piece is not None):
				is_user = piece.is_user
				piece_type = piece.piece_type

				self.build_piece_stats(board_input, i, j, 'build_threats', target_tiles)

				# Checks for check
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
								self.board_status = 'opponent_check'
								is_opponent_king_detected = True

				else:
					for element in target_tiles:
						element.threat_level_opponent += 1

						is_piece_none = element.piece is None
						if not is_piece_none and peek is False:
							is_piece_king = element.piece.piece_type == Constants.P_KING
							is_piece_user = element.piece.is_user is True

							if is_piece_king and is_piece_user:
								self.board_status = 'user_check'
								is_user_king_detected = True