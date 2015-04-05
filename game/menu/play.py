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