import pygame, time
from pygame import gfxdraw
from constants import *
from button import Button

def run(self):

	"""
	Menu:
		Load saved game (not yet)
		Single Player
			CPU Level: (1~20)
			Choose color: (W/B/?)
			Game Timer
			AI vs AI (choose!)
		Two-Player ooOOOOOO
			First screen: looking for players
				Send message to server: "I'm looking!"
				Server should check if there's anybody else looking and pair them up
			Second screen: paired up!
				Send message to this: "Found you a player!"
		Records
				
	"""
	# Screen fill
	self.screen.fill(Constants.BG)
	font = Constants.RESOURCES+Constants.FONT
	self.buttons = []

	if self.location == 'main_menu':

		# Set up the left button: Single Player
		color = Constants.SINGLE_PLAYER_BUTTON
		border_color = Constants.BLACK
		border_width = 10
		center_x = 300
		center_y = 125
		width = 500
		height = 150
		radius = 20
		command = "main_single"
		
		display_text = "Single Player"
		font = Constants.RESOURCES+Constants.FONT
		font_size = 70
		font_color = Constants.WHITE

		self.buttons.append(Button(center_x, center_y, width, height, radius, color,
			border_color, border_width, self.screen, command,
			display_text=display_text, font=font, font_size=font_size, font_color=font_color))
		
		# Set up the right-button: Two Player
		center_x = 500
		center_y = 350
		command = "main_two_player"
		display_text = "Two-Player"
		color = Constants.TWO_PLAYER_BUTTON
		self.buttons.append(Button(center_x, center_y, width, height, radius, color,
			border_color, border_width, self.screen, command,
			display_text=display_text, font=font, font_size=font_size, font_color=font_color))

	elif self.location == 'single_player_menu':

		# Difficulty level
		# Set up minus button
		color = Constants.SINGLE_PLAYER_BUTTON
		border_color = Constants.BLACK
		border_width = 10
		center_x = 100
		center_y = 50
		width = 50
		height = 50
		radius = 2
		command = "minus_difficulty"
		
		display_text = "<"
		font = Constants.RESOURCES+Constants.FONT
		font_size = 45
		font_color = Constants.WHITE

		self.buttons.append(Button(center_x, center_y, width, height, radius, color,
			border_color, border_width, self.screen, command,
			display_text=display_text, font=font, font_size=font_size, font_color=font_color))

		# Set up plus button
		center_x = 700
		center_y = 50
		command = "plus_difficulty"
		
		display_text = ">"

		self.buttons.append(Button(center_x, center_y, width, height, radius, color,
			border_color, border_width, self.screen, command,
			display_text=display_text, font=font, font_size=font_size, font_color=font_color))

		# Set up the difficulty border
		border_width = 9
		hp_border_rectangle = (125, 26, 550, 50)
		pygame.draw.rect(self.screen, Constants.CPU_LEVEL_BG, hp_border_rectangle, 0)
		pygame.draw.rect(self.screen, border_color, hp_border_rectangle, border_width)

		# Set up the difficulty level
		width = int(550*(self.cpu_level*1.0/12.0))
		hp_border_rectangle = (125, 31, width, 40)
		color = Constants.LEVEL_COLORS[((self.cpu_level-1)/2)]

		pygame.draw.rect(self.screen, color, hp_border_rectangle, 0)

		# Set up the numbers
		basic_font = pygame.font.Font(font, 30)
		text = ["1", "2", "3", "4", "5", "6"]

		for i in range(0, len(text)):
			text_char = basic_font.render(text[i], True, Constants.BLACK)
			char_rect = text_char.get_rect()
			char_rect.centerx = (120 + (550/(2*len(text)))) + i*(550/len(text))
			char_rect.centery = 90
			self.screen.blit(text_char, char_rect)

		# Set up the text: 1-2: Elementary, 3-4: Easy, 5-6: Standard, 7-8: Challenging, 9-11: Brain Freeze, 12: Mind Breaker
		cpu_level = self.cpu_level

		flavor_text = 'Mind Breaker'
		if cpu_level <= 2:
			flavor_text = 'Elementary'
		elif cpu_level <= 4:
			flavor_text = 'Easy'
		elif cpu_level <= 6:
			flavor_text = 'Standard'
		elif cpu_level <= 8:
			flavor_text = 'Challenging'
		elif cpu_level <= 11:
			flavor_text = 'Extreme'

		display_text = "Lv "+str(1+(cpu_level-1)*0.5)+": "+flavor_text

		text_char = basic_font.render(display_text, True, Constants.WHITE)
		char_rect = text_char.get_rect()
		char_rect.centerx = 400
		char_rect.centery = 52
		self.screen.blit(text_char, char_rect)

		# Set up the white button

		# Set up the black button

		# Set up the half-white half-black button

		# Start game button

		# Set up the back button


	# Draw all the possible buttons
	for button in self.buttons:
		button.draw_button()
	
	# Screen update
	pygame.display.flip()
