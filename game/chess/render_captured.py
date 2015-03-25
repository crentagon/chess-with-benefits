from constants import *
import pygame

# render_captured
def run(self, x, y, cmax, side, all_captured):
	i = 0
	j = 0
	for element in all_captured:
		rect_x = x + (Constants.CAPTURED_SIZE)*i
		rect_y = y + (Constants.CAPTURED_SIZE)*j
		piece_rect = (rect_x, rect_y, side, side)

		image_file = "mini_"+ element[0] + ".png"

		image_piece = pygame.image.load(Constants.RESOURCES+image_file)
		self.screen.blit(image_piece, piece_rect)

		j = j + 1 if i == cmax else j
		i = 0 if i == cmax else i+1