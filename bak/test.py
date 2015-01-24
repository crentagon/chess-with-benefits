# fen_string = "r4rk1/5ppp/p2p1bb1/2p5/2P5/2P2N2/PB1K1PPP/R6R b KQ-- - 0 23"
# fen_string = "r4rk1/5ppp/p2p1bb1/1pp5/2P5/1PP2N2/PB1K1PPP/R6R b KQ-- - 1 22"

fen_string = "r1b1kb1r/pppp1ppp/8/1N1n4/2P5/5N2/PP1PKPPP/R1B4R b KQkq c3 0 11"
fen = fen_string.split(" ")

# No additional processing required
active_turn = fen[1]
en_passant_info = fen[3]
halfmove_clock = int(fen[4])
fullmove_clock = int(fen[5])

# Castling information
castling_info = fen[2]
kingside_white = castling_info[0]
kingside_black = castling_info[1]
queenside_white = castling_info[2]
queenside_black = castling_info[3]

# Board information
board_info = fen[0]
rows = board_info.split("/")

# Board converter
converter = {
	"K": [0, True],
	"Q": [9, True],
	"R": [5, True],
	"B": [4, True],
	"N": [3, True],
	"P": [1, True],
	"k": [0, False],
	"q": [9, False],
	"r": [5, False],
	"b": [4, False],
	"n": [3, False],
	"p": [1, False],
}

print fen_string
print "Start board"
for row in rows:
	for element in row:
		try:
		    element = int(element)
		except ValueError:
			print converter[element][0]
	print "---"
print "End board"

halfmove_clock += 1
fullmove_clock += 1

print " "
print "Active Turn:", active_turn
print "En Passant:", en_passant_info
print "Halfmove Clock +1:", halfmove_clock
print "Fullmove Clock +1:", fullmove_clock
print " "
print "Castling, White King:", castling_info[0]
print "Castling, White Queen:", castling_info[1]
print "Castling, Black King:", castling_info[2]
print "Castling, Black Queen:", castling_info[3]