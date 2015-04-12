# populate_sidebar
def run(self):
	self.sidebar_buttons.append(["sidebar_undo.png", "Undo Move", "undo"])
	self.sidebar_buttons.append(["sidebar_undo.png", "Undo Move2", "undo"])

	self.aftergame_options.append(["Undo Last Move", "undo"])
	self.aftergame_options.append(["Review Game", "undo"])
	self.aftergame_options.append(["Play Again", "play_again"])
	self.aftergame_options.append(["Main Menu", "main_menu"])