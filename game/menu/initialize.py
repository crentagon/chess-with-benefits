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
	self.active_textbox_index = -1
	self.location = 'title_screen'

	# Single player info
	self.cpu_level = 5
	self.user_color = ['White', 'Black', 'Random']
	self.user_color_active = 0
	self.image_id = 0
	self.opponent_image_id = 99

	# Socket
	# self.host = "127.0.0.1"
	self.host = "192.168.1.20"
	self.port = 8888
	self.bufsize = 1024
	self.client_socket = None
	self.client_speaker_thread = None
	self.client_listener_thread = None
	self.is_connection_error = False

	self.character_names = {
		0: "Layton",
		1: "Mario",
		2: "Luigi",
		3: "Bowser",
		4: "Yoshi",
		5: "Kirby",
		6: "MetaKnight",
		7: "Sonic",
		8: "Pikachu",
		9: "Charizard",
		10: "Lucario",
		11: "Mewtwo",
		12: "Greninja",
		13: "Fox",
		14: "Falco",
		15: "Blastoise"
	}

	pygame.display.flip()