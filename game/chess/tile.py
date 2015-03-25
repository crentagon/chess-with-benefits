class Tile:

	def __init__(self, piece = None, threat_level_user = 0, threat_level_opponent = 0):
		self.piece = piece
		self.threat_level_user = threat_level_user
		self.threat_level_opponent = threat_level_opponent
		self.is_traversable = False
		self.is_last_movement = False
		self.is_current_movement = False

	def get_piece(self):
		return self.piece

	def set_piece(self, piece):
		self.piece = piece

	def remove_piece(self):
		self.piece = None