from game_start import *
from game.menu import (
	initialize,
	play,
	render_menu
)
import random

class MainMenu:

	def __init__(self):
		initialize.run(self)

	def render_menu(self):
		render_menu.run(self)

	def start_game_ai(self):
		is_white = True
		if self.user_color[self.user_color_active] == 'Black':
			is_white = False
		elif self.user_color[self.user_color_active] == 'Random':
			is_white = True if random.randint(0,1) else False

		self.location = Chesselate(self.screen, is_player_white=is_white, cpu_level=self.cpu_level).play()
		print "Location:", self.location

	def play(self):
		play.run(self)

if __name__ == '__main__':
	MainMenu().play()