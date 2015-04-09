from constants import *
import pygame
import sys

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

				if active_command == 'main_single':
					self.location = 'single_player_menu'

				elif active_command == 'main_two_player':
					self.location = 'two_player_search_menu'

				elif active_command == 'plus_difficulty' and self.cpu_level < 12:
					self.cpu_level += 1

				elif active_command == 'minus_difficulty' and self.cpu_level > 1:
					self.cpu_level -= 1

				elif active_command == 'start_game_ai':
					self.start_game_ai()
