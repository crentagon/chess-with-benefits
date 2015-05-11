from constants import *
import copy

def run(self, i, j):
	self.traversable = []
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
		if(is_i_gt_0):
			if(is_7j_lt_6):
				target_tile = self.board[i-1][j+2]

				temp_board = copy.deepcopy(self.board)
				temp_board[i-1][j+2].set_piece(temp_board[i][j].get_piece())
				temp_board[i][j].remove_piece()
				is_check_after_move = self.is_check(temp_board)

				if (target_tile.piece == None or target_tile.piece.is_user == False) and not is_check_after_move:
					self.traversable.append(target_tile)

			if(is_7j_gt_1):
				target_tile = self.board[i-1][j-2]

				temp_board = copy.deepcopy(self.board)
				temp_board[i-1][j-2].set_piece(temp_board[i][j].get_piece())
				temp_board[i][j].remove_piece()
				is_check_after_move = self.is_check(temp_board)

				if (target_tile.piece == None or target_tile.piece.is_user == False) and not is_check_after_move:
					self.traversable.append(target_tile)
										
		if(is_i_lt_7):
			if(is_7j_lt_6):
				target_tile = self.board[i+1][j+2]

				temp_board = copy.deepcopy(self.board)
				temp_board[i+1][j+2].set_piece(temp_board[i][j].get_piece())
				temp_board[i][j].remove_piece()
				is_check_after_move = self.is_check(temp_board)

				if (target_tile.piece == None or target_tile.piece.is_user == False) and not is_check_after_move:
					self.traversable.append(target_tile)
					
			if(is_7j_gt_1):
				target_tile = self.board[i+1][j-2]						

				temp_board = copy.deepcopy(self.board)
				temp_board[i+1][j-2].set_piece(temp_board[i][j].get_piece())
				temp_board[i][j].remove_piece()
				is_check_after_move = self.is_check(temp_board)

				if (target_tile.piece == None or target_tile.piece.is_user == False) and not is_check_after_move:
					self.traversable.append(target_tile)

		if(is_i_gt_1):
			if(is_7j_lt_7):
				target_tile = self.board[i-2][j+1]

				temp_board = copy.deepcopy(self.board)
				temp_board[i-2][j+1].set_piece(temp_board[i][j].get_piece())
				temp_board[i][j].remove_piece()
				is_check_after_move = self.is_check(temp_board)

				if (target_tile.piece == None or target_tile.piece.is_user == False) and not is_check_after_move:
					self.traversable.append(target_tile)
					
			if(is_7j_gt_0):
				target_tile = self.board[i-2][j-1]

				temp_board = copy.deepcopy(self.board)
				temp_board[i-2][j-1].set_piece(temp_board[i][j].get_piece())
				temp_board[i][j].remove_piece()
				is_check_after_move = self.is_check(temp_board)

				if (target_tile.piece == None or target_tile.piece.is_user == False) and not is_check_after_move:
					self.traversable.append(target_tile)
					

		if(is_i_lt_6):
			if(is_7j_lt_7):
				target_tile = self.board[i+2][j+1]

				temp_board = copy.deepcopy(self.board)
				temp_board[i+2][j+1].set_piece(temp_board[i][j].get_piece())
				temp_board[i][j].remove_piece()
				is_check_after_move = self.is_check(temp_board)

				if (target_tile.piece == None or target_tile.piece.is_user == False) and not is_check_after_move:
					self.traversable.append(target_tile)
					
			if(is_7j_gt_0):
				target_tile = self.board[i+2][j-1]

				temp_board = copy.deepcopy(self.board)
				temp_board[i+2][j-1].set_piece(temp_board[i][j].get_piece())
				temp_board[i][j].remove_piece()
				is_check_after_move = self.is_check(temp_board)

				if (target_tile.piece == None or target_tile.piece.is_user == False) and not is_check_after_move:
					self.traversable.append(target_tile)
						
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

					temp_board = copy.deepcopy(self.board)
					temp_board[i+k][j+k].set_piece(temp_board[i][j].get_piece())
					temp_board[i][j].remove_piece()
					is_check_after_move = self.is_check(temp_board)

					if (target_tile.piece == None or target_tile.piece.is_user == False):
						if not is_check_after_move:
							self.traversable.append(target_tile)
						if(target_tile.piece is not None and target_tile.piece.is_user == False):
							dirNE = False
					else:
						dirNE = False
				else:
					dirNE = False

				if(if_7j_gte_0 and dirSE):
					target_tile = self.board[i+k][j-k]

					temp_board = copy.deepcopy(self.board)
					temp_board[i+k][j-k].set_piece(temp_board[i][j].get_piece())
					temp_board[i][j].remove_piece()
					is_check_after_move = self.is_check(temp_board)

					if (target_tile.piece == None or target_tile.piece.is_user == False):
						if not is_check_after_move:
							self.traversable.append(target_tile)
						if(target_tile.piece is not None and target_tile.piece.is_user == False):
							dirSE = False
					else:
						dirSE = False
				else:
					dirSE = False

			if(is_ik_gte_0):
				if(if_7j_lte_7 and dirNW):
					target_tile = self.board[i-k][j+k]

					temp_board = copy.deepcopy(self.board)
					temp_board[i-k][j+k].set_piece(temp_board[i][j].get_piece())
					temp_board[i][j].remove_piece()
					is_check_after_move = self.is_check(temp_board)

					if (target_tile.piece == None or target_tile.piece.is_user == False):
						if not is_check_after_move:
							self.traversable.append(target_tile)
						if(target_tile.piece is not None and target_tile.piece.is_user == False):
							dirNW = False
					else:
						dirNW = False
				else:
					dirNW = False

				if(if_7j_gte_0 and dirSW):
					target_tile = self.board[i-k][j-k]

					temp_board = copy.deepcopy(self.board)
					temp_board[i-k][j-k].set_piece(temp_board[i][j].get_piece())
					temp_board[i][j].remove_piece()
					is_check_after_move = self.is_check(temp_board)

					if (target_tile.piece == None or target_tile.piece.is_user == False):
						if not is_check_after_move:
							self.traversable.append(target_tile)
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

				temp_board = copy.deepcopy(self.board)
				temp_board[i+k][j].set_piece(temp_board[i][j].get_piece())
				temp_board[i][j].remove_piece()
				is_check_after_move = self.is_check(temp_board)

				if (target_tile.piece == None or target_tile.piece.is_user == False):
					if not is_check_after_move:
						self.traversable.append(target_tile)
					if(target_tile.piece is not None and target_tile.piece.is_user == False):
						dirE = False
				else:
					dirE = False
			else:
				dirE = False

			if(is_ik_gte_0 and dirW):
				target_tile = self.board[i-k][j]

				temp_board = copy.deepcopy(self.board)
				temp_board[i-k][j].set_piece(temp_board[i][j].get_piece())
				temp_board[i][j].remove_piece()
				is_check_after_move = self.is_check(temp_board)

				if (target_tile.piece == None or target_tile.piece.is_user == False):
					if not is_check_after_move:
						self.traversable.append(target_tile)
					if(target_tile.piece is not None and target_tile.piece.is_user == False):
						dirW = False
				else:
					dirW = False
			else:
				dirW = False

			if(if_7j_lte_7 and dirN):
				target_tile = self.board[i][j+k]

				temp_board = copy.deepcopy(self.board)
				temp_board[i][j+k].set_piece(temp_board[i][j].get_piece())
				temp_board[i][j].remove_piece()
				is_check_after_move = self.is_check(temp_board)

				if (target_tile.piece == None or target_tile.piece.is_user == False):
					if not is_check_after_move:
						self.traversable.append(target_tile)
					if(target_tile.piece is not None and target_tile.piece.is_user == False):
						dirN = False
				else:
					dirN = False
			else:
				dirN = False

			if(if_7j_gte_0 and dirS):
				target_tile = self.board[i][j-k]

				temp_board = copy.deepcopy(self.board)
				temp_board[i][j-k].set_piece(temp_board[i][j].get_piece())
				temp_board[i][j].remove_piece()
				is_check_after_move = self.is_check(temp_board)

				if (target_tile.piece == None or target_tile.piece.is_user == False):
					if not is_check_after_move:
						self.traversable.append(target_tile)
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

				temp_board = copy.deepcopy(self.board)
				temp_board[i+k][j].set_piece(temp_board[i][j].get_piece())
				temp_board[i][j].remove_piece()
				is_check_after_move = self.is_check(temp_board)

				if (target_tile.piece == None or target_tile.piece.is_user == False):
					if not is_check_after_move:
						self.traversable.append(target_tile)
					if(target_tile.piece is not None and target_tile.piece.is_user == False):
						dirE = False
				else:
					dirE = False
			else:
				dirE = False

			if(is_ik_gte_0 and dirW):
				target_tile = self.board[i-k][j]

				temp_board = copy.deepcopy(self.board)
				temp_board[i-k][j].set_piece(temp_board[i][j].get_piece())
				temp_board[i][j].remove_piece()
				is_check_after_move = self.is_check(temp_board)

				if (target_tile.piece == None or target_tile.piece.is_user == False):
					if not is_check_after_move:
						self.traversable.append(target_tile)
					if(target_tile.piece is not None and target_tile.piece.is_user == False):
						dirW = False
				else:
					dirW = False
			else:
				dirW = False

			if(if_7j_lte_7 and dirN):
				target_tile = self.board[i][j+k]

				temp_board = copy.deepcopy(self.board)
				temp_board[i][j+k].set_piece(temp_board[i][j].get_piece())
				temp_board[i][j].remove_piece()
				is_check_after_move = self.is_check(temp_board)

				if (target_tile.piece == None or target_tile.piece.is_user == False):
					if not is_check_after_move:
						self.traversable.append(target_tile)
					if(target_tile.piece is not None and target_tile.piece.is_user == False):
						dirN = False
				else:
					dirN = False
			else:
				dirN = False

			if(if_7j_gte_0 and dirS):
				target_tile = self.board[i][j-k]

				temp_board = copy.deepcopy(self.board)
				temp_board[i][j-k].set_piece(temp_board[i][j].get_piece())
				temp_board[i][j].remove_piece()
				is_check_after_move = self.is_check(temp_board)

				if (target_tile.piece == None or target_tile.piece.is_user == False):
					if not is_check_after_move:
						self.traversable.append(target_tile)
					if(target_tile.piece is not None and target_tile.piece.is_user == False):
						dirS = False
				else:
					dirS = False
			else:
				dirS = False

			if(is_ik_lte_7):
				if(if_7j_lte_7 and dirNE):
					target_tile = self.board[i+k][j+k]

					temp_board = copy.deepcopy(self.board)
					temp_board[i+k][j+k].set_piece(temp_board[i][j].get_piece())
					temp_board[i][j].remove_piece()
					is_check_after_move = self.is_check(temp_board)

					if (target_tile.piece == None or target_tile.piece.is_user == False):
						if not is_check_after_move:
							self.traversable.append(target_tile)
						if(target_tile.piece is not None and target_tile.piece.is_user == False):
							dirNE = False
					else:
						dirNE = False
				else:
					dirNE = False

				if(if_7j_gte_0 and dirSE):
					target_tile = self.board[i+k][j-k]

					temp_board = copy.deepcopy(self.board)
					temp_board[i+k][j-k].set_piece(temp_board[i][j].get_piece())
					temp_board[i][j].remove_piece()
					is_check_after_move = self.is_check(temp_board)

					if (target_tile.piece == None or target_tile.piece.is_user == False):
						if not is_check_after_move:
							self.traversable.append(target_tile)
						if(target_tile.piece is not None and target_tile.piece.is_user == False):
							dirSE = False
					else:
						dirSE = False
				else:
					dirSE = False

			if(is_ik_gte_0):
				if(if_7j_lte_7 and dirNW):
					target_tile = self.board[i-k][j+k]

					temp_board = copy.deepcopy(self.board)
					temp_board[i-k][j+k].set_piece(temp_board[i][j].get_piece())
					temp_board[i][j].remove_piece()
					is_check_after_move = self.is_check(temp_board)

					if (target_tile.piece == None or target_tile.piece.is_user == False):
						if not is_check_after_move:
							self.traversable.append(target_tile)
						if(target_tile.piece is not None and target_tile.piece.is_user == False):
							dirNW = False
					else:
						dirNW = False
				else:
					dirNW = False

				if(if_7j_gte_0 and dirSW):
					target_tile = self.board[i-k][j-k]

					temp_board = copy.deepcopy(self.board)
					temp_board[i-k][j-k].set_piece(temp_board[i][j].get_piece())
					temp_board[i][j].remove_piece()
					is_check_after_move = self.is_check(temp_board)

					if (target_tile.piece == None or target_tile.piece.is_user == False):
						if not is_check_after_move:
							self.traversable.append(target_tile)
						if(target_tile.piece is not None and target_tile.piece.is_user == False):
							dirSW = False
					else:
						dirSW = False
				else:
					dirSW = False

	elif piece.piece_type == Constants.P_KING:
		if(is_i_lte_7):
			target_tile = self.board[i+1][j]

			temp_board = copy.deepcopy(self.board)
			temp_board[i+1][j].set_piece(temp_board[i][j].get_piece())
			temp_board[i][j].remove_piece()
			is_check_after_move = self.is_check(temp_board)

			if(target_tile.threat_level_opponent <= 0 and (target_tile.piece == None or target_tile.piece.is_user == False)) and not is_check_after_move:
				self.traversable.append(target_tile)
			
			if(is_7j_lte_7):
				target_tile = self.board[i+1][j+1]

				temp_board = copy.deepcopy(self.board)
				temp_board[i+1][j+1].set_piece(temp_board[i][j].get_piece())
				temp_board[i][j].remove_piece()
				is_check_after_move = self.is_check(temp_board)

				if(target_tile.threat_level_opponent <= 0 and (target_tile.piece == None or target_tile.piece.is_user == False)) and not is_check_after_move:
					self.traversable.append(target_tile)
			
			if(is_7j_gte_0):
				target_tile = self.board[i+1][j-1]

				temp_board = copy.deepcopy(self.board)
				temp_board[i+1][j-1].set_piece(temp_board[i][j].get_piece())
				temp_board[i][j].remove_piece()
				is_check_after_move = self.is_check(temp_board)

				if(target_tile.threat_level_opponent <= 0 and (target_tile.piece == None or target_tile.piece.is_user == False)) and not is_check_after_move:
					self.traversable.append(target_tile)
			
		if(is_i_gte_0):
			target_tile = self.board[i-1][j]

			temp_board = copy.deepcopy(self.board)
			temp_board[i-1][j].set_piece(temp_board[i][j].get_piece())
			temp_board[i][j].remove_piece()
			is_check_after_move = self.is_check(temp_board)

			if(target_tile.threat_level_opponent <= 0 and (target_tile.piece == None or target_tile.piece.is_user == False)) and not is_check_after_move:
				self.traversable.append(target_tile)
			
			if(is_7j_lte_7):
				target_tile = self.board[i-1][j+1]

				temp_board = copy.deepcopy(self.board)
				temp_board[i-1][j+1].set_piece(temp_board[i][j].get_piece())
				temp_board[i][j].remove_piece()
				is_check_after_move = self.is_check(temp_board)

				if(target_tile.threat_level_opponent <= 0 and (target_tile.piece == None or target_tile.piece.is_user == False)) and not is_check_after_move:
					self.traversable.append(target_tile)
			
			if(is_7j_gte_0):
				target_tile = self.board[i-1][j-1]

				temp_board = copy.deepcopy(self.board)
				temp_board[i-1][j-1].set_piece(temp_board[i][j].get_piece())
				temp_board[i][j].remove_piece()
				is_check_after_move = self.is_check(temp_board)

				if(target_tile.threat_level_opponent <= 0 and (target_tile.piece == None or target_tile.piece.is_user == False)) and not is_check_after_move:
					self.traversable.append(target_tile)
			
		if(is_7j_lte_7):
			target_tile = self.board[i][j+1]

			temp_board = copy.deepcopy(self.board)
			temp_board[i][j+1].set_piece(temp_board[i][j].get_piece())
			temp_board[i][j].remove_piece()
			is_check_after_move = self.is_check(temp_board)

			if(target_tile.threat_level_opponent <= 0 and (target_tile.piece == None or target_tile.piece.is_user == False)) and not is_check_after_move:
				self.traversable.append(target_tile)
		
		if(is_7j_gte_0):
			target_tile = self.board[i][j-1]

			temp_board = copy.deepcopy(self.board)
			temp_board[i][j-1].set_piece(temp_board[i][j].get_piece())
			temp_board[i][j].remove_piece()
			is_check_after_move = self.is_check(temp_board)

			if(target_tile.threat_level_opponent <= 0 and (target_tile.piece == None or target_tile.piece.is_user == False)) and not is_check_after_move:
				self.traversable.append(target_tile)

		# Castling
		if not piece.is_moved and self.board[i][j].threat_level_opponent <= 0:
			can_castle_kingside = True
			can_castle_queenside = True

			rank = Constants.TILE_1 if piece.is_white else Constants.TILE_8

			kingside_rook = self.board[Constants.TILE_H][rank].piece is not None and not self.board[Constants.TILE_H][rank].piece.is_moved and self.board[Constants.TILE_H][rank].piece.piece_type == Constants.P_ROOK
			queenside_rook = self.board[Constants.TILE_A][rank].piece is not None and not self.board[Constants.TILE_A][rank].piece.is_moved and self.board[Constants.TILE_A][rank].piece.piece_type == Constants.P_ROOK
			
			if kingside_rook or queenside_rook:
				for k in range(1,3):
					if can_castle_kingside and kingside_rook:
						kingside_tile = self.board[i+k][rank]
						if kingside_tile.piece is not None or kingside_tile.threat_level_opponent > 0:
							can_castle_kingside = False
					else:
						can_castle_kingside = False

					if can_castle_queenside and queenside_rook:
						queenside_tile = self.board[i-k][rank]
						if queenside_tile.piece is not None or queenside_tile.threat_level_opponent > 0:
							can_castle_queenside = False
					else:
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

			temp_board = copy.deepcopy(self.board)
			temp_board[i][j+factor*1].set_piece(temp_board[i][j].get_piece())
			temp_board[i][j].remove_piece()
			is_check_after_move = self.is_check(temp_board)

			if target_tile.piece == None and not is_check_after_move:
				self.traversable.append(target_tile)

			# That movement from where the pawn moves two spaces. I don't know what it's called
			start_rank = Constants.PIECE_MAPPING['2'] if self.is_player_white else Constants.PIECE_MAPPING['7']
			if(j == start_rank and self.board[i][j+factor].piece == None):
				target_tile = self.board[i][j+factor*2]

				temp_board = copy.deepcopy(self.board)
				temp_board[i][j+factor*2].set_piece(temp_board[i][j].get_piece())
				temp_board[i][j].remove_piece()
				is_check_after_move = self.is_check(temp_board)

				if(target_tile.piece == None) and not is_check_after_move:
					self.traversable.append(target_tile)

			# Pawn's doing a capture!
			if(is_i_lt_7 and is_7j_lt_7):
				target_tile = self.board[i+1][j+factor*1]

				temp_board = copy.deepcopy(self.board)
				temp_board[i+1][j+factor*1].set_piece(temp_board[i][j].get_piece())
				temp_board[i][j].remove_piece()
				is_check_after_move = self.is_check(temp_board)

				if(target_tile.piece is not None and target_tile.piece.is_user == False) and not is_check_after_move:
					self.traversable.append(target_tile)

			if(is_i_gt_0 and is_7j_lt_7):
				target_tile = self.board[i-1][j+factor*1]

				temp_board = copy.deepcopy(self.board)
				temp_board[i-1][j+factor*1].set_piece(temp_board[i][j].get_piece())
				temp_board[i][j].remove_piece()
				is_check_after_move = self.is_check(temp_board)

				if(target_tile.piece is not None and target_tile.piece.is_user == False)  and not is_check_after_move:
					self.traversable.append(target_tile)
		

		# En Passant
		if self.en_passant != '-' :
			target_tile_x = Constants.PIECE_MAPPING[self.en_passant[0]]
			target_tile_y = Constants.PIECE_MAPPING[self.en_passant[1]]
			
			factor = 1 if self.is_player_white else -1

			if j == target_tile_y - factor and (i == target_tile_x + factor or i == target_tile_x - factor):
				target_tile = self.board[target_tile_x][target_tile_y]
				self.traversable.append(target_tile)

	for element in self.traversable:
		element.is_traversable = True