from constants import *
import pygame
import sys

#play
def run(self):

	self.is_display_changed = True

	while(True):		
		if self.is_display_changed:
			self.render_menu()
			self.is_display_changed = False
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT: 
				sys.exit(0)

			elif event.type == 5:
				self.is_display_changed = True
				mouse_pos = pygame.mouse.get_pos()
				x_coord = mouse_pos[0]
				y_coord = mouse_pos[1]

				active_command = ''
				for button in self.buttons:
					if button.is_button_pressed(x_coord, y_coord):
						active_command = button.get_command()

				if active_command == 'toggle_server':
					self.is_server_running = not self.is_server_running
					self.start_server()

		if self.server_thread is not None:
			if self.is_server_running:
				if self.server_thread.is_new_message:
					self.is_display_changed = True
					self.last_message = self.server_thread.get_message()
					print "Here:", self.last_message
			else:
				self.server_thread.stop_thread()




