from constants import *
import pygame

def run(self):

	# Game Window information
	pygame.init()
	pygame.display.set_caption("Chess with Benefits")
	self.clock = pygame.time.Clock()

	self.screen = pygame.display.set_mode(Constants.SCREENSIZE)
	self.screen.fill(Constants.WHITE)
	pygame.display.flip()