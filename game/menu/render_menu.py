import pygame, time
from pygame import gfxdraw
from constants import *
from button import Button

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
	# All buttons
	buttons = []

	# Screen fill
	self.screen.fill(Constants.BG)
	font = Constants.RESOURCES+Constants.FONT

	# Set up the left button: Single Player
	color = Constants.SINGLE_PLAYER_BUTTON
	border_color = Constants.BLACK
	border_width = 10
	center_x = 213
	center_y = 250
	width = 326
	height = 400
	radius = 20
	command = "main_single"
	
	display_text = "Single Player"
	font = Constants.RESOURCES+Constants.FONT
	font_size = 30
	font_color = Constants.WHITE

	buttons.append(Button(center_x, center_y, width, height, radius, color,
		border_color, border_width, self.screen, command,
		display_text=display_text, font=font, font_size=font_size, font_color=font_color))
	
	# Set up the right-button: Two Player
	center_x = 577
	command = "main_multi"
	buttons.append(Button(center_x, center_y, width, height, radius, color,
		border_color, border_width, self.screen, command))

	# Draw all the possible buttons
	for button in buttons:
		button.draw_button()
	
	# Screen update
	pygame.display.flip()
