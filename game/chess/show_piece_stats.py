
def run(self, board_input, i, j):
	origin_piece = board_input[i][j].piece

	max_control = {
		1: 2,
		3: 8,
		4: 13,
		5: 14,
		9: 27,
		0: 8
	}

	origin_piece.status = 'Healthy'

	is_threatened_undefended = len(origin_piece.attackers) > len(origin_piece.defenders)
	is_threatened_by_lower_rank = [x for x in origin_piece.attackers if x < origin_piece.piece_type]
	is_ample_activity = origin_piece.tiles_controlled > 0.6*max_control[origin_piece.piece_type]
	offensive_power = len(origin_piece.offensive_power)
	defensive_power = len(origin_piece.defensive_power)

	# Threatened (being attacked by a piece without being defended OR being attacked by a piece of lower rank)
	if is_threatened_by_lower_rank or is_threatened_undefended:
		origin_piece.status = 'Threatened'

	# Warrior (attacking at least one piece OR in a valuable position OR at 60% maximum activity)
	elif offensive_power >= 2 or is_ample_activity:
		origin_piece.status = 'Warrior'

	# Defender (defending at least two pieces)
	elif defensive_power >= 2:
		origin_piece.status = 'Defender'
	
	self.piece_stats = {
		'is_piece_white': origin_piece.is_white,
		'piece_type': origin_piece.piece_type,
		'tile_control_count': origin_piece.tiles_controlled,
		'defenders': origin_piece.defenders,
		'attackers': origin_piece.attackers,
		'defensive_power': origin_piece.defensive_power,
		'offensive_power': origin_piece.offensive_power,
		'status': origin_piece.status
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