from constants import *
import pygame

def run(self, host, port, bufsize):

	# Game Window information
	pygame.init()
	pygame.display.set_caption("Chess with Benefits -- Server")
	self.clock = pygame.time.Clock()

	# Screen
	self.screen = pygame.display.set_mode(Constants.SCREENSIZE)
	self.screen.fill(Constants.WHITE)
	self.buttons = []
	self.location = 'main_menu'
	self.is_display_changed = False

	# Host information
	self.host = host
	self.port = port
	self.bufsize = bufsize
	self.addr = (self.host, self.port)
	self.last_message = 'Idle'
	self.is_server_running = False
	self.server_thread = None

	pygame.display.flip()