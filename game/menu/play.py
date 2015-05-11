from pygame.locals import *
from constants import *
import pygame
import sys
import re

#play
def run(self):

	while(True):		

		self.render_menu()
		events = pygame.event.get()
		
		for event in events:
			if event.type == pygame.QUIT: 
				sys.exit(0)

			elif event.type == 5:
				mouse_pos = pygame.mouse.get_pos()
				x_coord = mouse_pos[0]
				y_coord = mouse_pos[1]

				active_command = ''
				for button in self.buttons:
					if button.is_button_pressed(x_coord, y_coord):
						active_command = button.get_command()

				self.active_textbox_index = -1
				for index, textbox in enumerate(self.textboxes):
					if textbox.is_textbox_active(x_coord, y_coord):
						print "Textbox is being clicked! is_active:", textbox.is_active
						self.active_textbox_index = index
						textbox.ask()

						if index == 0:
							self.host = textbox.get_message()
						elif index == 1:
							self.port = textbox.get_message()

						break
					else:
						print "Textbox NOT being clicked! is_active:", textbox.is_active

				p = re.compile('set_avatar_(.*)')

				if active_command == 'main_menu':
					self.location = 'main_menu'

				elif active_command == 'main_single':
					self.location = 'single_player_menu'

				elif active_command == 'main_two_player':
					self.location = 'two_player_menu_screen_ip'

				elif active_command == 'two_player_connect':
					self.location = 'two_player_menu_screen_connecting'

				elif active_command == 'plus_difficulty' and self.cpu_level < 12:
					self.cpu_level += 1

				elif active_command == 'minus_difficulty' and self.cpu_level > 1:
					self.cpu_level -= 1

				elif active_command == 'plus_color' and self.user_color_active < 2:
					self.user_color_active += 1

				elif active_command == 'minus_color' and self.user_color_active > 0:
					self.user_color_active -= 1

				elif active_command == 'start_game_ai':
					self.start_game_ai()

				elif active_command == 'start_game_player_a':
					self.start_game_player_a()

				elif active_command == 'start_game_player_b':
					self.start_game_player_b()

				elif p.match(active_command):
					self.image_id = int(active_command[11:])
