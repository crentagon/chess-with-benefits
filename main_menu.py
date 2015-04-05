# from game_start import *
from game.menu import (
	initialize,
	play,
	render_menu
)

class MainMenu:

	def __init__(self):
		initialize.run(self)

	def render_menu(self):
		render_menu.run(self)

	def play(self):
		play.run(self)

if __name__ == '__main__':
	MainMenu().play()