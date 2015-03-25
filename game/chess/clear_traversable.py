# clear_traversable
def clear_traversable(self):
	for x in range(8):
		for y in range(8):
			self.board[x][y].is_traversable = False

# clear_board
def clear_board(self):
	for i in range(8):
		for j in range(8):
			self.board[i][j].piece = None

# clear_last_movement
def clear_last_movement(self):
	self.board[self.last_source_x][self.last_source_y].is_last_movement = False
	self.board[self.last_destination_x][self.last_destination_y].is_last_movement = False

# clear_current_movement
def clear_current_movement(self):
		self.board[self.currmove_source_x][self.currmove_source_y].is_current_movement = False
		self.board[self.currmove_destination_x][self.currmove_destination_y].is_current_movement = False