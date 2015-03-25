from constants import *
import pygame

def run(self, font_text, font_color, font_size, x, y):
	# Prepate the fonts
	font = Constants.RESOURCES+Constants.FONT_REG
	pygame_font = pygame.font.Font(font, font_size)

	# Prepare the text
	text = font_text
	text_render = pygame_font.render(text, True, font_color)
	text_rect = text_render.get_rect()

	# Render the text for the opponent
	text_rect.centerx = x
	text_rect.centery = y
	self.screen.blit(text_render, text_rect)