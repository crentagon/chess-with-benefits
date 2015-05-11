# populate_lists
def run(self):
	# Single player menu
	if not self.is_two_player:
		# Sidebar buttons
		self.sidebar_buttons.append(["sidebar_undo.png", "Undo Move", "undo"])
		self.sidebar_buttons.append(["sidebar_undo.png", "Undo Move2", "undo"])

		# After game options
		self.aftergame_options.append(["Undo Last Move", "undo"])
		self.aftergame_options.append(["Play Again", "play_again"])

	self.aftergame_options.append(["Review Game", "undo"])
	self.aftergame_options.append(["Main Menu", "main_menu"])

	# Game over
	self.is_game_over = {
		'in_game': False,
		'promoting': False,
		'user_check': False,
		'opponent_check': False,
		'forfeit': True,
		'stalemate': True,
		'50_move_rule': True,
		'user_checkmate': True,
		'opponent_checkmate': True,
	}