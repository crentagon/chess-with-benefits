from constants import *
import pygame

def run(self):

	# Game Window information
	pygame.init()
	pygame.display.set_caption("Chess with Benefits")
	self.clock = pygame.time.Clock()

	# Screen
	self.screen = pygame.display.set_mode(Constants.SCREENSIZE)
	self.screen.fill(Constants.WHITE)
	self.buttons = []
	self.textboxes = []
	self.active_textbox_index = 0
	self.location = 'main_menu'

	# Single player info
	self.cpu_level = 5
	self.user_color = ['White', 'Black', 'Random']
	self.user_color_active = 0

	# Socket
	self.host = "127.0.0.1"
	self.port = 28888
	self.bufsize = 1024
	self.client_socket = None
	self.client_speaker_thread = None
	self.client_listener_thread = None

	pygame.display.flip()