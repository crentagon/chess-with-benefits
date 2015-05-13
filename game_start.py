from game.chess import (
	build_piece_stats,
	build_threats,
	clear,
	convert_fen_to_board,
	convert_to_fen,
	endgame_check,
	initialize,
	is_check,
	move_piece,
	play,
	populate_lists,
	render_board,
	render_captured,
	render_tile,
	show_traversable,
	write_text
)

class Chesselate:

	def __init__(self, screen, is_player_white = True, is_two_player = False, cpu_level = 5, img_user = 1, img_opponent = 99,
		name_user="Player", name_opponent="Opponent", fen_string = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
		listener=None, speaker=None):
		
		# fen_string = "1n2k1n1/pppppppp/8/8/8/8/PPPPPPPP/1N2K1N1 w KQkq - 0 1"
		initialize.run(self, screen, is_player_white, is_two_player, cpu_level, img_user, img_opponent,
			name_user, name_opponent, fen_string, listener, speaker)

	def populate_lists(self):
		populate_lists.run(self)

	def build_threats(self, board_input, peek=False):
		build_threats.run(self, board_input, peek)

	def build_piece_stats(self, board_input, i, j, mode='build_threats', target_tiles=[]):
		build_piece_stats.run(self, board_input, i, j, mode, target_tiles)

	def render_captured(self, x, y, cmax, side, all_captured):
		render_captured.run(self, x, y, cmax, side, all_captured)

	def clear_traversable(self):
		clear.clear_traversable(self)

	def clear_board(self):
		clear.clear_board(self)

	def clear_last_movement(self):
		clear.clear_last_movement(self)

	def clear_current_movement(self):
		clear.clear_current_movement(self)

	def endgame_check(self, fen_string):
		endgame_check.run(self, fen_string)

	def move_piece(self, source_x, source_y, destination_x, destination_y, promotion = False):
		move_piece.run(self, source_x, source_y, destination_x, destination_y, promotion)

	def convert_to_fen(self):
		return convert_to_fen.run(self)

	def is_check(self, board_input):
		return is_check.run(self, board_input)

	def show_traversable(self, i, j):
		show_traversable.run(self, i, j)

	def convert_fen_to_board(self, fen_string, is_init = False):
		convert_fen_to_board.run(self, fen_string, is_init)

	def render_tile(self, i, j):
		return render_tile.run(self, i, j)

	def write_text(self, font_text, font_color, font_size, x, y):
		write_text.run(self, font_text, font_color, font_size, x, y)

	def render_board(self):
		render_board.run(self)

	def play(self):
		return play.run(self)

# if __name__ == '__main__':
	# pass
	# test = "rnb1kbnr/p1p1pppp/1p6/3q4/3P4/2N5/PPP2PPP/R1BQKBNR b KQkq - 1 4" #castling bug
	# test = "1kR5/1r4pp/3Rpn2/pP2p3/P3P3/5P1N/4N1PP/1K6 b ---- - 0 26" #castling bug 2.0
	# test = "7k/5R2/8/6R1/5B2/8/8/7K w ---- - 0 1" #stalemate for black
	# test = "7k/5R2/8/6R1/8/8/8/2B4K w ---- - 0 1" #stalemate for black (bug! must be checkmate, not check.)
	# test = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1" #gamestart
	# test = "7R/7P/5p2/2p3k1/8/7K/1pr5/8 b ---- - 0 65" #promotion test!
	# test = "6RQ/8/5p2/2p2k2/7K/8/6r1/5q2 b ---- - 7 69" #one move away from checkmate
	# test = "r5k1/R7/1P4p1/5p1p/2P5/1P6/3p1PPP/3K4 w ---- - 1 33" #temp test!
	# test = "rnbqkb1r/pppppppp/5n2/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 1 1" # knightbug
	# Chesselate(is_player_white=False, cpu_level=5, fen_string=test).play()
	# Chesselate(is_player_white=False, cpu_level=12).play()

