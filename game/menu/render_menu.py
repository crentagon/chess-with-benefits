from pygame import gfxdraw
from constants import *
import pygame, time

def run(self):

	"""
	Menu:
		Single Player
			CPU Level: (1~20)
			Choose color: (W/B/?)
			Game Timer
			Load saved game (not yet)
			AI vs AI (choose!)
		Two-Player ooOOOOOO
			First screen: looking for players
				Send message to server: "I'm looking!"
				Server should check if there's anybody else looking and pair them up
			Second screen: paired up!
				Send message to this: "Found you a player!"
				
	"""

	# Screen fill
	self.screen.fill(Constants.BG)
	font = Constants.RESOURCES+Constants.FONT

	# Draw the left button: Single Player
	button_coords = [(100,50),(325,50),(375,100),(375,400),(325,450),(100,450),(50,400),(50,100)]
	color = Constants.SINGLE_PLAYER_BUTTON
	border_color = Constants.BLACK
	center_1 = (100,100)
	center_2 = (100,400)
	center_3 = (326,100)
	center_4 = (326,400)
	border_width = 10
	border_width_circle = int(border_width*4.0/10.0)
	radius = 50

	draw_main_menu_button(self, button_coords, color,
		border_color, center_1, center_2, center_3, center_4,
		border_width, border_width_circle, radius)

	# Draw the right button: Two-Player
	button_coords = [(700,450),(475,450),(425,400),(425,100),(475,50),(700,50),(750,100),(750,400)]
	center_1 = (700,100)
	center_2 = (700,400)
	center_3 = (476,100)
	center_4 = (476,400)
	border_width = 10
	border_width_circle = int(border_width*4.0/10.0)
	radius = 50

	draw_main_menu_button(self, button_coords, color,
		border_color, center_1, center_2, center_3, center_4,
		border_width, border_width_circle, radius)

	# Screen update
	pygame.display.flip()

def draw_main_menu_button(self, button_coords, color,
	border_color, center_1, center_2, center_3, center_4,
	border_width, border_width_circle, radius):

	# Border of the button
	pygame.draw.polygon(self.screen, border_color, button_coords, border_width)
	pygame.gfxdraw.filled_circle(self.screen, center_1[0], center_1[1], radius+border_width_circle, border_color)
	pygame.gfxdraw.filled_circle(self.screen, center_2[0], center_2[1], radius+border_width_circle, border_color)
	pygame.gfxdraw.filled_circle(self.screen, center_3[0], center_3[1], radius+border_width_circle, border_color)
	pygame.gfxdraw.filled_circle(self.screen, center_4[0], center_4[1], radius+border_width_circle, border_color)

	# Button color
	pygame.draw.polygon(self.screen, color, button_coords)
	pygame.draw.circle(self.screen, color, center_1, radius)
	pygame.draw.circle(self.screen, color, center_2, radius)
	pygame.draw.circle(self.screen, color, center_3, radius)
	pygame.draw.circle(self.screen, color, center_4, radius)