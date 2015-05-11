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

				# This also checks if the King is in checkmate
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