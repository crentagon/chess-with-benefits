import pygame, time, sys
from pygame import gfxdraw
from constants import *
from button import Button
from chess_client_listener_thread import *
from chess_client_speaker_thread import *
from inputbox import *

def manage_characters(self, height_offset = 100):

	width_offset = (Constants.SCREENSIZE[0] - (7*75))/2
	width = 65
	height = 65
	radius = 2
	color = Constants.BLACK
	border_width = 10
	screen = self.screen
	image_w = 65
	image_h = 65

	# Set up characters
	font_text = "Choose your avatar: "
	font_color = Constants.BLACK
	font_size = 35
	x = 240
	y = height_offset - 55
	self.write_text(font_text, font_color, font_size, x, y)

	font_text = self.character_names[self.image_id]
	font_color = Constants.RED
	font_size = 35
	x = 500
	y = height_offset - 55
	self.write_text(font_text, font_color, font_size, x, y)

	# Set up the character selection
	for i in range(2):
		center_y = i*(65+10) + height_offset

		for j in range(8):
			center_x = j*(65+10) + width_offset
			current_id = i*8+j
			character = "res/avatars/char-"+str(current_id)+".png"

			border_color = Constants.RED if self.image_id == current_id else Constants.BLACK
			command = "set_avatar_"+str(current_id)

			self.buttons.append(Button(center_x, center_y, width, height, radius, color, border_color,
				border_width, screen, command, image_filename=character, image_x='', image_y='', image_w=image_w, image_h=image_h))

def back_button(self, center_x=100, center_y=100):

	color = Constants.TWO_PLAYER_BUTTON
	border_color = Constants.BLACK
	border_width = 10
	width = 200
	height = 50
	radius = 10
	command = "main_menu"
	
	display_text = "Back"
	font = Constants.RESOURCES+Constants.FONT
	font_size = 50
	font_color = Constants.WHITE

	self.buttons.append(Button(center_x, center_y, width, height, radius, color,
		border_color, border_width, self.screen, command,
		display_text=display_text, font=font, font_size=font_size, font_color=font_color))

def choose_color(self, center_x=100, center_y=150):

	# Set up minus-color button
	color = Constants.SINGLE_PLAYER_BUTTON
	border_color = Constants.BLACK
	border_width = 10
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

	# Set up the textbox in the middle
	# Set up the textbox border
	color_index = self.user_color_active
	font_color = Constants.PLAY_AS_WHITE_TEXT
	bg_color = Constants.PLAY_AS_WHITE_BG
	if color_index == 1:
		font_color = Constants.PLAY_AS_BLACK_TEXT
		bg_color = Constants.PLAY_AS_BLACK_BG
	elif color_index == 2:
		font_color = Constants.PLAY_AS_RANDOM_TEXT
		bg_color = Constants.PLAY_AS_RANDOM_BG

	border_width = 9
	hp_border_rectangle = (center_x + 25, center_y - 25, 550, 50)
	pygame.draw.rect(self.screen, bg_color, hp_border_rectangle, 0)
	pygame.draw.rect(self.screen, border_color, hp_border_rectangle, border_width)

	# Set up the text
	font_text = self.user_color[color_index]
	font_color = Constants.WHITE if color_index else Constants.BLACK
	font_size = 30
	x = 400
	y = center_y
	self.write_text(font_text, font_color, font_size, x, y)

	# Set up plus-color button
	font_size = 45
	font_color = Constants.WHITE
	center_x = 700
	command = "plus_color"
	
	display_text = ">"

	self.buttons.append(Button(center_x, center_y, width, height, radius, color,
		border_color, border_width, self.screen, command,
		display_text=display_text, font=font, font_size=font_size, font_color=font_color))

def run(self):
	self.screen.fill(Constants.BG)
	image_piece = pygame.image.load(Constants.RESOURCES+"bg_rest.png")
	piece_rect = (0,0,800,500)
	self.screen.blit(image_piece, piece_rect)

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
	font = Constants.RESOURCES+Constants.FONT
	self.buttons = []
	self.textboxes = []

	if self.location == 'title_screen':
		center_x = 400
		center_y = 250
		width = 800
		height = 500
		radius = 0
		color = Constants.BLACK
		border_color = Constants.BLACK
		border_width = 0
		screen = self.screen
		command = "main_menu"
		image_filename = "res/title_screen.png"
		image_w = 800
		image_h = 500

		self.buttons.append(Button(center_x, center_y, width, height, radius, color, border_color,
			border_width, screen, command, image_filename=image_filename, image_x='', image_y='', image_w=image_w, image_h=image_h))


	elif self.location == 'main_menu':
		image_piece = pygame.image.load(Constants.RESOURCES+"main_menu_background.png")
		piece_rect = (0,0,800,500)
		self.screen.blit(image_piece, piece_rect)

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
		y = 90
		font_size = 30
		font_color = Constants.BLACK

		for i in range(0, len(text)):
			font_text = text[i]
			x = (120 + (550/(2*len(text)))) + i*(550/len(text))

			self.write_text(font_text, font_color, font_size, x, y)

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

		font_text = "Lv "+str(1+(cpu_level-1)*0.5)+": "+flavor_text
		font_color = Constants.WHITE
		x = 400
		y = 52

		self.write_text(font_text, font_color, font_size, x, y)

		# Set up the color-choosing:
		choose_color(self)

		# Choose color
		manage_characters(self, 260)

		# Start game button
		color = Constants.SINGLE_PLAYER_BUTTON
		border_color = Constants.BLACK
		border_width = 10
		center_x = 575
		center_y = 435
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
		back_button(self, 150, 435)

	# Ask for the IP address to connect to
	elif self.location == 'two_player_menu_screen_ip':
		# Set up the form:
		font_text = "IP Address:"
		font_color = Constants.BLACK
		font_size = 40
		x = 245
		y = 75
		self.write_text(font_text, font_color, font_size, x, y)

		font_text = "Port:"
		font_color = Constants.BLACK
		x = 190
		y = 225
		self.write_text(font_text, font_color, font_size, x, y)

		# Unable to connect to the server
		if self.is_connection_error:
			font_size = 30
			font_text = "Unfortunately, the server isn't noticing you..."
			font_color = Constants.RED
			x = 400
			y = 350
			self.write_text(font_text, font_color, font_size, x, y)

		# Set up the top textboxs:
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

		center_y = 250
		length = 5

		self.textboxes.append(InputBox(self.screen, center_x, center_y, width, height, length=length, font=font,
		font_size=font_size, font_color=font_color, textbox_bg=textbox_bg, border_color=border_color,
		border_width=1, message=str(self.port)))

		# Set up the connect button
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

		# Set up the back button
		back_button(self, 200, 425)

	elif self.location == 'two_player_menu_screen_connecting':

		host = self.host
		port = self.port
		addr = (host, port)
		
		font_color = Constants.BLACK
		font_text = "Connecting..."
		font_size = 40
		x = 400
		y = 60
		self.write_text(font_text, font_color, font_size, x, y)
		pygame.display.update()
		# time.sleep(2)

		# TO-DO: Conenct to the server.
		try:
			self.is_connection_error = False
			self.client_socket = socket(AF_INET, SOCK_STREAM)
			self.client_socket.connect(addr)
			self.is_connected = True
			print "Connection successful."
		except:
			print "Exception!"
			self.is_connection_error = True
			self.location = 'two_player_menu_screen_ip'
			return

		# Run the listener thread
		self.client_listener_thread = ChessClientListenerThread(self.client_socket)
		self.client_listener_thread.start()

		# Run the speaker thread
		self.client_speaker_thread = ChessClientSpeakerThread(self.client_socket)
		self.client_speaker_thread.start()

		font_color = Constants.BLUE
		font_text = "Connected!"
		font_size = 50
		x = 400
		y = 200
		self.write_text(font_text, font_color, font_size, x, y)
		self.location = 'two_player_menu_screen_waiting'

	# Waiting for the other player
	elif self.location == 'two_player_menu_screen_waiting':

		font_color = Constants.WAIT_COLOR[int(time.time()*4)%4]
		font_text = "Waiting for opponent to connect..."
		font_size = 40
		x = 400
		y = 60
		self.write_text(font_text, font_color, font_size, x, y)

		message = self.client_listener_thread.get_message()
		if message == 'ready-first':	
			self.location = 'two_player_menu_screen_choose_color'
		elif message == 'ready':
			self.location = 'two_player_menu_screen_waiting_color'

	# The first person to connect gets to set the rules of the game
	elif self.location == 'two_player_menu_screen_choose_color' or self.location == 'two_player_menu_screen_waiting_color':
		
		next_action = "start_game_player_b"
		
		if self.location == 'two_player_menu_screen_choose_color':
			
			next_action = "start_game_player_a"

			# Set up the color-choosing:
			choose_color(self, 100, 250)

		manage_characters(self, 75)

		# Start game button
		color = Constants.SINGLE_PLAYER_BUTTON
		border_color = Constants.BLACK
		border_width = 10
		center_x = 575
		center_y = 425
		width = 300
		height = 50
		radius = 10
		command = next_action
		
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
		# textbox.is_active = False
		# if self.active_textbox_index >= 0:
			# textbox.is_active = True if index == self.active_textbox_index else False
		textbox.draw_textbox()
	
	# Screen update
	pygame.display.update()
