from game_start import *
from game.menu import (
	initialize,
	play,
	render_menu,
	write_text
)
import random, sys, re

class MainMenu:

	def __init__(self):
		initialize.run(self)

	def render_menu(self):
		render_menu.run(self)

	def write_text(self, font_text, font_color, font_size, x, y):
		write_text.run(self, font_text, font_color, font_size, x, y)

	def is_player_white(self):
		is_white = True
		if self.user_color[self.user_color_active] == 'Black':
			is_white = False
		elif self.user_color[self.user_color_active] == 'Random':
			is_white = True if random.randint(0,1) else False
		return is_white

	def start_game_ai(self):
		is_white = self.is_player_white()

		self.location = Chesselate(self.screen, is_player_white=is_white, is_two_player=False,
			img_user=self.image_id, name_user=self.character_names[self.image_id],
			name_opponent="Stockfish", cpu_level=self.cpu_level).play()

		print "Location:", self.location

	def start_game_player_a(self):
		is_white = self.is_player_white()
		color_message = 'white' if is_white else 'black'
		self.client_speaker_thread.send_message(color_message+"_"+str(self.image_id))
		
		# Wait for the other player to say "ready_XX"
		while True:
			message = self.client_listener_thread.get_message()
			if message:
				if message != 'GAME_OVER':
					self.opponent_image_id = int(message[6:])
					break
				else:
					self.location = 'main_menu'
					return

		self.start_game_two_player()

	def start_game_player_b(self):
		message = "ready_"+str(self.image_id)
		self.client_speaker_thread.send_message(message)

		# Wait for the other player to say "COLOR_XX"
		while True:
			message = self.client_listener_thread.get_message()
			if message:
				print "Recevied message:", message
				if message != 'GAME_OVER':
					is_white = re.compile('white_(.*)')
					self.user_color_active = 1 if is_white.match(message) is not None else 0
					self.opponent_image_id = int(message[6:])
					break
				else:
					self.location = 'main_menu'
					return

		self.start_game_two_player()

	def start_game_two_player(self):
		is_white = self.is_player_white()
		color_message = 'white' if is_white else 'black'
		print "My color is:", color_message
		
		self.location = Chesselate(self.screen, is_player_white=is_white, is_two_player=True,
			img_user=self.image_id, img_opponent=self.opponent_image_id, name_user=self.character_names[self.image_id],
			name_opponent=self.character_names[self.opponent_image_id], listener=self.client_listener_thread,
			speaker=self.client_speaker_thread).play()

	def play(self):
		play.run(self)

if __name__ == '__main__':
	MainMenu().play()