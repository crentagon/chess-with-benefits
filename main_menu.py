from game_start import *
from game.menu import (
	initialize,
	play,
	render_menu
)
import random, sys

class MainMenu:

	def __init__(self):
		initialize.run(self)

	def render_menu(self):
		render_menu.run(self)

	def is_player_white(self):
		is_white = True
		if self.user_color[self.user_color_active] == 'Black':
			is_white = False
		elif self.user_color[self.user_color_active] == 'Random':
			is_white = True if random.randint(0,1) else False
		return is_white

	def start_game_ai(self):
		is_white = self.is_player_white()

		self.location = Chesselate(self.screen, is_player_white=is_white, is_two_player=False, cpu_level=self.cpu_level).play()
		print "Location:", self.location

	def setup_two_player(self):
		is_white = self.is_player_white()

		color_message = 'white' if is_white else 'black'
		self.client_speaker_thread.send_message(color_message)
		self.start_game_two_player()

	def start_game_two_player(self):
		is_white = self.is_player_white()
		color_message = 'white' if is_white else 'black'
		print "My color is:", color_message
		self.location = Chesselate(self.screen, is_player_white=is_white, is_two_player=True,
			listener=self.client_listener_thread, speaker=self.client_speaker_thread).play()

	def play(self):
		play.run(self)

if __name__ == '__main__':
	MainMenu().play()