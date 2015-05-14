
def run(self, board_input, i, j):
	origin_piece = board_input[i][j].piece
	self.piece_stats = {
		'is_piece_white': origin_piece.is_white,
		'piece_type': origin_piece.piece_type,
		'tile_control_count': origin_piece.tiles_controlled,
		'defenders': origin_piece.defenders,
		'attackers': origin_piece.attackers,
		'defensive_power': origin_piece.defensive_power,
		'offensive_power': origin_piece.offensive_power
	}
	
	# "Status":
		# Defender/Royal Defender (defending at least two pieces/Defending the King)
		# Warrior (attacking at least one piece OR in a valuable position OR at 60% maximum activity)
		# Healthy (default)
		# Threatened (being attacked by a piece without being defended OR being attacked by a piece of lower rank)
		# Note: place its value right next to it

	# Number of tiles controlled: "Tile Control Count: " // add counter at the bottom
	# Number of pieces attacking it: "Attackers: "
	# Number of pieces defending it: "Supporters: "
	# Number of pieces it is attacking: "Offensive power: "
	# Number of pieces it is defending: "Defensive power: "