
class Piece:

	#####################
	#    Piece Types    #
	# ----------------- #
	#	1 - Pawn		#
	#	3 - Knight		#
	#	4 - Bishop		#
	#	5 - Rook		#
	#	9 - Queen		#
	#	100 - King 		#
	#####################

	def __init__(self, piece_type, is_white = True, is_user = True):
		self.is_user = is_user
		self.is_white = is_white 
		self.piece_type = piece_type
		self.threat_level = 0
		self.piece_position = (0,0,0,0)
		self.is_moved = False
		self.reset_stats()

	def reset_stats(self):
		self.status = ''
		self.tiles_controlled = 0
		self.defenders = [] 			# The pieces defending it
		self.attackers = [] 			# The pieces attacking it
		self.defensive_power = []		# The pieces it is defending
		self.offensive_power = [] 		# The pieces it is attacking

	def pressed(self, mouse):
		rect = self.piece_position
		if self.is_user:
			if mouse[0] > rect[0]:
				if mouse[1] > rect[1]:
					if mouse[0] < rect[0] + rect[2]:
						if mouse[1] < rect[1] + rect[3]:
							return True
						else: return False
					else: return False
				else: return False
			else: return False
