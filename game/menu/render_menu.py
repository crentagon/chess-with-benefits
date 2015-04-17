import pygame, time, sys
from pygame import gfxdraw
from constants import *
from button import Button
from chess_client_listener_thread import *
from chess_client_speaker_thread import *
from inputbox import *

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
	self.textboxes = []

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

		# Set up the color-choosing:
		# Set up minus-color button
		color = Constants.SINGLE_PLAYER_BUTTON
		border_color = Constants.BLACK
		border_width = 10
		center_x = 100
		center_y = 175
		width = 50
		height = 50
		radius = 2
		command = "minus_color"
		
		display_text = "<"
		font = Constants.RESOURCES+Constants.FONT
		font_size = 45
		font_color = Constants.WHITE

		self.buttons.append(Button(center_x, center_y, width, height, radius, color,
			border_color, border_width, self.screen, command,
			display_text=display_text, font=font, font_size=font_size, font_color=font_color))

		# Set up plus-color button
		center_x = 700
		center_y = 175
		command = "plus_color"
		
		display_text = ">"

		self.buttons.append(Button(center_x, center_y, width, height, radius, color,
			border_color, border_width, self.screen, command,
			display_text=display_text, font=font, font_size=font_size, font_color=font_color))

		# Set up the textbox in the middle
		# Set up the textbox border
		color_index = self.user_color_active
		text_color = Constants.PLAY_AS_WHITE_TEXT
		bg_color = Constants.PLAY_AS_WHITE_BG
		if color_index == 1:
			text_color = Constants.PLAY_AS_BLACK_TEXT
			bg_color = Constants.PLAY_AS_BLACK_BG
		elif color_index == 2:
			text_color = Constants.PLAY_AS_RANDOM_TEXT
			bg_color = Constants.PLAY_AS_RANDOM_BG

		border_width = 9
		hp_border_rectangle = (125, 151, 550, 50)
		pygame.draw.rect(self.screen, bg_color, hp_border_rectangle, 0)
		pygame.draw.rect(self.screen, border_color, hp_border_rectangle, border_width)

		# Set up the text
		text_char = basic_font.render(self.user_color[color_index], True, text_color)
		char_rect = text_char.get_rect()
		char_rect.centerx = 400
		char_rect.centery = 175
		self.screen.blit(text_char, char_rect)

		# Start game button
		color = Constants.SINGLE_PLAYER_BUTTON
		border_color = Constants.BLACK
		border_width = 10
		center_x = 575
		center_y = 425
		width = 300
		height = 50
		radius = 10
		command = "start_game_ai"
		
		display_text = "Start Game"
		font = Constants.RESOURCES+Constants.FONT
		font_size = 50
		font_color = Constants.WHITE

		self.buttons.append(Button(center_x, center_y, width, height, radius, color,
			border_color, border_width, self.screen, command,
			display_text=display_text, font=font, font_size=font_size, font_color=font_color))

		# Set up the back button

	# TO-DO: Ask for the IP address to connect to MARKER
	elif self.location == 'two_player_menu_screen_ip':
		# Set up the top textbox: IP Address
		color = Constants.SINGLE_PLAYER_BUTTON
		border_color = Constants.BLACK
		border_width = 10
		center_x = 150
		center_y = 100
		width = 500
		height = 70
		font_size = 70
		
		font = Constants.RESOURCES+Constants.FONT
		length = 15
		font_color = Constants.BLACK
		textbox_bg = Constants.BG

		self.textboxes.append(InputBox(self.screen, center_x, center_y, width, height, length=length, font=font,
		font_size=font_size, font_color=font_color, textbox_bg=textbox_bg, border_color=border_color,
		border_width=1, message=self.host))

		display_text = "IP Address:"
		font_color = Constants.BLACK
		basic_font = pygame.font.Font(font, 40)

		text_char = basic_font.render(display_text, True, font_color)
		char_rect = text_char.get_rect()
		char_rect.centerx = 245
		char_rect.centery = 75
		self.screen.blit(text_char, char_rect)

		center_y = 250
		length = 5

		self.textboxes.append(InputBox(self.screen, center_x, center_y, width, height, length=length, font=font,
		font_size=font_size, font_color=font_color, textbox_bg=textbox_bg, border_color=border_color,
		border_width=1, message=str(self.port)))

		display_text = "Port:"
		font_color = Constants.BLACK
		basic_font = pygame.font.Font(font, 40)

		text_char = basic_font.render(display_text, True, font_color)
		char_rect = text_char.get_rect()
		char_rect.centerx = 190
		char_rect.centery = 225
		self.screen.blit(text_char, char_rect)

		# Set up the right-button: Two Player
		color = Constants.SINGLE_PLAYER_BUTTON
		border_color = Constants.BLACK
		border_width = 10
		center_x = 575
		center_y = 425
		width = 300
		height = 50
		radius = 10
		command = "two_player_connect"
		
		display_text = "Connect"
		font = Constants.RESOURCES+Constants.FONT
		font_size = 50
		font_color = Constants.WHITE

		self.buttons.append(Button(center_x, center_y, width, height, radius, color,
			border_color, border_width, self.screen, command,
			display_text=display_text, font=font, font_size=font_size, font_color=font_color))

	elif self.location == 'two_player_menu_screen_connecting':
		host = self.host
		port = self.port
		addr = (host, port)
		
		font_color = Constants.WAIT_COLOR[int(time.time())%2]
		wait_text = "Connecting..."

		basic_font = pygame.font.Font(font, 40)
		text_char = basic_font.render(wait_text, True, font_color)
		char_rect = text_char.get_rect()
		char_rect.centerx = 400
		char_rect.centery = 60
		self.screen.blit(text_char, char_rect)

		# Connect to the server
		self.client_socket = socket(AF_INET, SOCK_STREAM)
		self.client_socket.connect(addr)
		self.is_connected = True
		print "Connection successful."

		# TO-DO: Unable to connect to the server
		# try:
		# except:
		# 	print "Exception!"
		# 	self.location = 'main_menu'

		# Run the listener thread
		self.client_listener_thread = ChessClientListenerThread(self.client_socket)
		self.client_listener_thread.start()

		# Run the speaker thread
		self.client_speaker_thread = ChessClientSpeakerThread(self.client_socket)
		self.client_speaker_thread.start()

		display_text = "Connected!"
		font_color = Constants.BLUE
		basic_font = pygame.font.Font(font, 50)

		text_char = basic_font.render(display_text, True, font_color)
		char_rect = text_char.get_rect()
		char_rect.centerx = 400
		char_rect.centery = 200
		self.screen.blit(text_char, char_rect)

		self.location = 'two_player_menu_screen_waiting'

	# Waiting for the other player
	elif self.location == 'two_player_menu_screen_waiting':

		font_color = Constants.WAIT_COLOR[int(time.time()*4)%4]
		wait_text = "Waiting for opponent to connect..."

		basic_font = pygame.font.Font(font, 40)
		text_char = basic_font.render(wait_text, True, font_color)
		char_rect = text_char.get_rect()
		char_rect.centerx = 400
		char_rect.centery = 60
		self.screen.blit(text_char, char_rect)

		message = self.client_listener_thread.get_message()
		if message == 'ready-first':	
			self.location = 'two_player_menu_screen_choose_color'
		elif message == 'ready':
			self.location = 'two_player_menu_screen_waiting_color'

	# The second person to connect waits for the first player to choose the settings
	elif self.location == 'two_player_menu_screen_waiting_color':
		font_color = Constants.WAIT_COLOR[int(time.time()*3)%3]
		wait_text = "Waiting for opponent to set the color and rules..."

		basic_font = pygame.font.Font(font, 30)
		text_char = basic_font.render(wait_text, True, font_color)
		char_rect = text_char.get_rect()
		char_rect.centerx = 400
		char_rect.centery = 60
		self.screen.blit(text_char, char_rect)

		message = self.client_listener_thread.get_message()
		if message:
			self.is_two_player = True
			self.user_color_active = 0 if message == 'black' else 1
			self.start_game_two_player()

	# The first person to connect gets to set the rules of the game
	elif self.location == 'two_player_menu_screen_choose_color':
		# Set up the color-choosing:
		# Set up minus-color button
		basic_font = pygame.font.Font(font, 30)
		
		color = Constants.SINGLE_PLAYER_BUTTON
		border_color = Constants.BLACK
		border_width = 10
		center_x = 100
		center_y = 50
		width = 50
		height = 50
		radius = 2
		command = "minus_color"
		
		display_text = "<"
		font = Constants.RESOURCES+Constants.FONT
		font_size = 45
		font_color = Constants.WHITE

		self.buttons.append(Button(center_x, center_y, width, height, radius, color,
			border_color, border_width, self.screen, command,
			display_text=display_text, font=font, font_size=font_size, font_color=font_color))

		# Set up plus-color button
		center_x = 700
		center_y = 50
		command = "plus_color"
		
		display_text = ">"

		self.buttons.append(Button(center_x, center_y, width, height, radius, color,
			border_color, border_width, self.screen, command,
			display_text=display_text, font=font, font_size=font_size, font_color=font_color))

		# Set up the textbox in the middle
		# Set up the textbox border
		color_index = self.user_color_active
		text_color = Constants.PLAY_AS_WHITE_TEXT
		bg_color = Constants.PLAY_AS_WHITE_BG
		if color_index == 1:
			text_color = Constants.PLAY_AS_BLACK_TEXT
			bg_color = Constants.PLAY_AS_BLACK_BG
		elif color_index == 2:
			text_color = Constants.PLAY_AS_RANDOM_TEXT
			bg_color = Constants.PLAY_AS_RANDOM_BG

		border_width = 9
		hp_border_rectangle = (125, 26, 550, 50)
		pygame.draw.rect(self.screen, bg_color, hp_border_rectangle, 0)
		pygame.draw.rect(self.screen, border_color, hp_border_rectangle, border_width)

		# Set up the text
		text_char = basic_font.render(self.user_color[color_index], True, text_color)
		char_rect = text_char.get_rect()
		char_rect.centerx = 400
		char_rect.centery = 50
		self.screen.blit(text_char, char_rect)

		# Start game button
		color = Constants.SINGLE_PLAYER_BUTTON
		border_color = Constants.BLACK
		border_width = 10
		center_x = 575
		center_y = 425
		width = 300
		height = 50
		radius = 10
		command = "start_game_two_player"
		
		display_text = "Start Game"
		font = Constants.RESOURCES+Constants.FONT
		font_size = 50
		font_color = Constants.WHITE

		self.buttons.append(Button(center_x, center_y, width, height, radius, color,
			border_color, border_width, self.screen, command,
			display_text=display_text, font=font, font_size=font_size, font_color=font_color))

	# Draw all the buttons
	for button in self.buttons:
		button.draw_button()

	# Draw all the textboxes
	for index, textbox in enumerate(self.textboxes):
		textbox.is_active = True if index == self.active_textbox_index else False
		textbox.draw_textbox()
	
	# Screen update
	pygame.display.update()
