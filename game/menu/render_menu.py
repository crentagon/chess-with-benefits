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
	color = Constants.SINGLE_PLAYER_BUTTON
	border_color = Constants.BLACK
	border_width = 10
	center_x = 213
	center_y = 250
	width = 326
	height = 400
	radius = 20

	draw_button(self, center_x, center_y, width, height, radius, color, border_color, border_width)

	# Draw the right button: Two-Player
	center_x = 577
	draw_button(self, center_x, center_y, width, height, radius, color, border_color, border_width)

	# Screen update
	pygame.display.flip()

def draw_button(self, center_x, center_y, width, height, radius, color, border_color, border_width):
	half_width = width/2
	half_height = height/2

	# Octagon points: x-coordinates
	midright_x = center_x + half_width - radius
	midleft_x = center_x - half_width + radius
	right_x = center_x + half_width
	left_x = center_x - half_width

	# Octagon points: y-coordinates
	midbottom_y = center_y + half_height - radius
	midtop_y = center_y - half_height + radius
	bottom_y = center_y + half_height
	top_y = center_y - half_height

	# Octagon points
	point_1 = (midleft_x, top_y)
	point_2 = (midright_x, top_y)
	point_3 = (right_x, midtop_y)
	point_4 = (right_x, midbottom_y)
	point_5 = (midright_x, bottom_y)
	point_6 = (midleft_x, bottom_y)
	point_7 = (left_x, midbottom_y)
	point_8 = (left_x, midtop_y)
	button_coords = [point_1, point_2, point_3, point_4, point_5, point_6, point_7, point_8] 

	border_width_circle = int(border_width*2.0/5.0)

	# Border of the button
	pygame.draw.polygon(self.screen, border_color, button_coords, border_width)
	pygame.gfxdraw.filled_circle(self.screen, midleft_x, midtop_y, radius+border_width_circle, border_color)
	pygame.gfxdraw.filled_circle(self.screen, midright_x, midtop_y, radius+border_width_circle, border_color)
	pygame.gfxdraw.filled_circle(self.screen, midleft_x, midbottom_y, radius+border_width_circle, border_color)
	pygame.gfxdraw.filled_circle(self.screen, midright_x, midbottom_y, radius+border_width_circle, border_color)

	# Button color
	pygame.draw.polygon(self.screen, color, button_coords)
	pygame.draw.circle(self.screen, color, (midleft_x, midtop_y), radius)
	pygame.draw.circle(self.screen, color, (midright_x, midtop_y), radius)
	pygame.draw.circle(self.screen, color, (midleft_x, midbottom_y), radius)
	pygame.draw.circle(self.screen, color, (midright_x, midbottom_y), radius)
