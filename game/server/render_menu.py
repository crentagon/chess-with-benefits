import pygame, time, sys
from pygame import gfxdraw
from constants import *
from button import Button
from chess_client_listener_thread import *
from chess_client_speaker_thread import *

def run(self):

	# Screen fill
	self.screen.fill(Constants.BG)
	font = Constants.RESOURCES+Constants.FONT
	self.buttons = []

	color = Constants.SINGLE_PLAYER_BUTTON
	border_color = Constants.BLACK
	border_width = 10
	center_x = 200
	center_y = 250
	width = 200
	height = 50
	radius = 5
	command = "toggle_server"

	# Last message and print to text file "show logs"

	# The big red button
	display_text = "Stop Server" if self.is_server_running else "Start Server"
	font_size = 30
	font_color = Constants.WHITE

	self.buttons.append(Button(center_x, center_y, width, height, radius, color,
		border_color, border_width, self.screen, command,
		display_text=display_text, font=font, font_size=font_size, font_color=font_color))

	# Display the IP Address
	display_text = "IP Address: "+str(self.host)
	x = 200
	y = 50
	write_text(self, display_text, font_size, Constants.BLACK, x, y)

	# Display the port
	display_text = "Port: "+str(self.port)
	x = 200
	y = 100
	write_text(self, display_text, font_size, Constants.BLACK, x, y)

	# Display the last message
	display_text = "Message: "+str(self.last_message)
	font_size = 20
	x = 200
	y = 150
	write_text(self, display_text, font_size, Constants.BLACK, x, y)

	# Draw all the possible buttons
	for button in self.buttons:
		button.draw_button()
	
	# Screen update
	pygame.display.flip()

def write_text(self, message, font_size, color, x, y):
	font = Constants.RESOURCES+Constants.FONT
	basic_font = pygame.font.Font(font, font_size)
	
	text_char = basic_font.render(message, True, color)
	char_rect = text_char.get_rect()
	char_rect.centerx = x
	char_rect.centery = y
	self.screen.blit(text_char, char_rect)