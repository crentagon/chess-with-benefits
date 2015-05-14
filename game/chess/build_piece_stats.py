from constants import *
import copy

def piece_build(self, board_input, i, j, mode='build_threats',
	target_tiles=[], old_i=None, old_j=None, change_bool=None, is_pawn_capture=False):

	is_build_threats = mode == 'build_threats'
	is_show_traversable = mode == 'show_traversable'

	if is_build_threats:
		target_tile = board_input[i][j]
		target_tiles.append(target_tile)

		origin_piece = board_input[old_i][old_j].piece

		if target_tile.piece is not None:
			target_piece = target_tile.piece

			# If it is attacking an enemy piece
			if origin_piece.is_white != target_piece.is_white:
				origin_piece.offensive_power.append(target_piece.piece_type)
				target_piece.attackers.append(origin_piece.piece_type)

			# If it is defending a friendly piece
			else:
				# if origin_piece.is_white and origin_piece.piece_type == 5 and target_piece.piece_type == 1:
				# 	print "Defending!"
				origin_piece.defensive_power.append(target_piece.piece_type)
				target_piece.defenders.append(origin_piece.piece_type)

			if change_bool is not None:
				change_bool[0] = False

		else:
			origin_piece.tiles_controlled += 1

	elif is_show_traversable:
		target_tile = board_input[i][j]

		temp_board = copy.deepcopy(board_input)
		temp_board[i][j].set_piece(temp_board[old_i][old_j].get_piece())
		temp_board[old_i][old_j].remove_piece()
		is_check_after_move = self.is_check(temp_board)

		if not is_pawn_capture:
			if (target_tile.piece == None or target_tile.piece.is_user == False) and not is_check_after_move:
				self.traversable.append(target_tile)
				if change_bool is not None and target_tile.piece is not None and target_tile.piece.is_user == False:
					change_bool[0] = False
			elif change_bool is not None:
				change_bool[0] = False
		else:
			if (target_tile.piece is not None and target_tile.piece.is_user == False) and not is_check_after_move:
				self.traversable.append(target_tile)

def run(self, board_input, i, j, mode='build_threats', target_tiles=[]):

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

	tile = board_input[i][j]
	piece = tile.piece
	piece_type = piece.piece_type

	if piece_type == Constants.P_KNIGHT:
		if is_i_gt_0:
			if is_7j_lt_6:
				piece_build(self, board_input, i-1, j+2, mode, target_tiles, i, j)
			if is_7j_gt_1:
				piece_build(self, board_input, i-1, j-2, mode, target_tiles, i, j)
			
		if is_i_lt_7:
			if is_7j_lt_6:
				piece_build(self, board_input, i+1, j+2, mode, target_tiles, i, j)
			if is_7j_gt_1:
				piece_build(self, board_input, i+1, j-2, mode, target_tiles, i, j)
			
		if is_i_gt_1:
			if is_7j_lt_7:
				piece_build(self, board_input, i-2, j+1, mode, target_tiles, i, j)
			if is_7j_gt_0:
				piece_build(self, board_input, i-2, j-1, mode, target_tiles, i, j)

		if is_i_lt_6:
			if is_7j_lt_7:
				piece_build(self, board_input, i+2, j+1, mode, target_tiles, i, j)
			if is_7j_gt_0:
				piece_build(self, board_input, i+2, j-1, mode, target_tiles, i, j)

	elif piece_type == Constants.P_KING:

		if(is_i_lte_7):
			piece_build(self, board_input, i+1, j, mode, target_tiles, i, j)

			if(is_7j_lte_7):
				piece_build(self, board_input, i+1, j+1, mode, target_tiles, i, j)
			
			if(is_7j_gte_0):
				piece_build(self, board_input, i+1, j-1, mode, target_tiles, i, j)
			
		if(is_i_gte_0):
			piece_build(self, board_input, i-1, j, mode, target_tiles, i, j)
			
			if(is_7j_lte_7):
				piece_build(self, board_input, i-1, j+1, mode, target_tiles, i, j)
			
			if(is_7j_gte_0):
				piece_build(self, board_input, i-1, j-1, mode, target_tiles, i, j)
			
		if(is_7j_lte_7):
			piece_build(self, board_input, i, j+1, mode, target_tiles, i, j)
		
		if(is_7j_gte_0):
			piece_build(self, board_input, i, j-1, mode, target_tiles, i, j)

	elif piece_type == Constants.P_PAWN:
		is_user = piece.is_user
		is_white = piece.is_white
		factor = 1 if is_user else -1

		if mode == 'show_traversable' and is_7j_lte_7:
			# Normal movement: moving one square up (or below) a rank -- only if there's no one up front!
			if board_input[i][j+factor].piece is None:
				piece_build(self, board_input, i, j+factor, mode, target_tiles, i, j)

			# That movement from where the pawn moves two spaces. I don't know what it's called
			start_rank = Constants.PIECE_MAPPING['2'] if self.is_player_white else Constants.PIECE_MAPPING['7']
			
			if(j == start_rank and self.board[i][j+factor*2].piece == None):
				piece_build(self, board_input, i, j+factor*2, mode, target_tiles, i, j)

		if is_white:
			if(is_i_lt_7 and is_7j_lt_7):
				piece_build(self, board_input, i+1, j+1, mode, target_tiles, i, j, is_pawn_capture=True)

			if(is_i_gt_0 and is_7j_lt_7):
				piece_build(self, board_input, i-1, j+1, mode, target_tiles, i, j, is_pawn_capture=True)

		else:
			if(is_i_lt_7 and is_7j_gt_0):
				piece_build(self, board_input, i+1, j-1, mode, target_tiles, i, j, is_pawn_capture=True)

			if(is_i_gt_0 and is_7j_gt_0):
				piece_build(self, board_input, i-1, j-1, mode, target_tiles, i, j, is_pawn_capture=True)

	else:

		if piece_type == Constants.P_BISHOP or piece_type == Constants.P_QUEEN:
			dirNE = [True] # needed to turn this into a mutable object
			dirSE = [True] # so that python can pass this by reference
			dirNW = [True]
			dirSW = [True]
			for k in range(1, 8):
				is_ik_lte_7 = i+k <= 7
				is_ik_gte_0 = i-k >= 0
				if_7j_lte_7 = j+k <= 7
				if_7j_gte_0 = j-k >= 0

				if is_ik_lte_7:
					if if_7j_lte_7 and dirNE[0]:
						piece_build(self, board_input, i+k, j+k, mode, target_tiles, i, j, change_bool=dirNE)
					else:
						dirNE[0] = False

					if if_7j_gte_0 and dirSE[0]:
						piece_build(self, board_input, i+k, j-k, mode, target_tiles, i, j, change_bool=dirSE)
					else:
						dirSE[0] = False

				if is_ik_gte_0:
					if if_7j_lte_7 and dirNW[0]:
						piece_build(self, board_input, i-k, j+k, mode, target_tiles, i, j, change_bool=dirNW)
					else:
						dirNW[0] = False

					if if_7j_gte_0 and dirSW[0]:
						piece_build(self, board_input, i-k, j-k, mode, target_tiles, i, j, change_bool=dirSW)
					else:
						dirSW[0] = False

		if piece_type == Constants.P_ROOK or piece_type == Constants.P_QUEEN:
			dirN = [True]
			dirS = [True]
			dirE = [True]
			dirW = [True]
			for k in range(1, 8):
				is_ik_lte_7 = i+k <= 7
				is_ik_gte_0 = i-k >= 0
				if_7j_lte_7 = j+k <= 7
				if_7j_gte_0 = j-k >= 0

				if(is_ik_lte_7 and dirE[0]):
					piece_build(self, board_input, i+k, j, mode, target_tiles, i, j, change_bool=dirE)
				else:
					dirE[0] = False

				if(is_ik_gte_0 and dirW[0]):
					piece_build(self, board_input, i-k, j, mode, target_tiles, i, j, change_bool=dirW)
				else:
					dirW[0] = False

				if(if_7j_lte_7 and dirN[0]):
					piece_build(self, board_input, i, j+k, mode, target_tiles, i, j, change_bool=dirN)
				else:
					dirN[0] = False

				if(if_7j_gte_0 and dirS[0]):
					piece_build(self, board_input, i, j-k, mode, target_tiles, i, j, change_bool=dirS)
				else:
					dirS[0] = False

