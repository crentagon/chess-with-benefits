from constants import *
import copy

def run(self, i, j):
	self.traversable = []
	self.clear_traversable()
	piece = self.board[i][j].piece

	self.build_piece_stats(self.board, i, j, 'show_traversable')

	if piece.piece_type == Constants.P_KING:
		# Special case: Castling
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
		# Special case: En Passant
		if self.en_passant != '-' :
			target_tile_x = Constants.PIECE_MAPPING[self.en_passant[0]]
			target_tile_y = Constants.PIECE_MAPPING[self.en_passant[1]]
			
			factor = 1 if self.is_player_white else -1

			if j == target_tile_y - factor and (i == target_tile_x + factor or i == target_tile_x - factor):
				target_tile = self.board[target_tile_x][target_tile_y]
				self.traversable.append(target_tile)

	for element in self.traversable:
		element.is_traversable = True