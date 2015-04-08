from pygame import gfxdraw
import pygame

class Button:

	def __init__(self, center_x, center_y, width, height, radius, color, border_color,
		border_width, screen, command, display_text='', font='', font_size='', font_color='',
		font_x='', font_y='', image_filename='', image_x='', image_y='', image_w='', image_h=''):

		# Button properties
		self.center_x = center_x 			# x-coordinate of the center of the button
		self.center_y = center_y			# y-coordinate of the center of the button
		self.width = width 					# button width
		self.height = height 				# button height
		self.radius = radius 				# google "border-radius"
		self.color = color 					# button color
		self.border_color = border_color 	# border color
		self.border_width = border_width 	# border width

		# Pygame screen
		self.screen = screen

		# Text information
		self.display_text = display_text
		self.font_color = font_color
		self.font_size = font_size
		self.font_x = font_x
		self.font_y = font_y
		self.font = font

		# Image information
		self.image_filename = image_filename

	def draw_button(self):
		# Set the half-width and half-height
		half_width = self.width/2
		half_height = self.height/2

		# Octagon points: x-coordinates
		midright_x = self.center_x + half_width - self.radius
		midleft_x = self.center_x - half_width + self.radius
		right_x = self.center_x + half_width
		left_x = self.center_x - half_width

		# Octagon points: y-coordinates
		midbottom_y = self.center_y + half_height - self.radius
		midtop_y = self.center_y - half_height + self.radius
		bottom_y = self.center_y + half_height
		top_y = self.center_y - half_height

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

		border_width_circle = int(self.border_width*2.0/5.0)

		# Border of the button
		pygame.draw.polygon(self.screen, self.border_color, button_coords, self.border_width)
		pygame.gfxdraw.filled_circle(self.screen, midleft_x, midtop_y, self.radius+border_width_circle, self.border_color)
		pygame.gfxdraw.filled_circle(self.screen, midright_x, midtop_y, self.radius+border_width_circle, self.border_color)
		pygame.gfxdraw.filled_circle(self.screen, midleft_x, midbottom_y, self.radius+border_width_circle, self.border_color)
		pygame.gfxdraw.filled_circle(self.screen, midright_x, midbottom_y, self.radius+border_width_circle, self.border_color)

		# Button color
		pygame.draw.polygon(self.screen, self.color, button_coords)
		pygame.draw.circle(self.screen, self.color, (midleft_x, midtop_y), self.radius)
		pygame.draw.circle(self.screen, self.color, (midright_x, midtop_y), self.radius)
		pygame.draw.circle(self.screen, self.color, (midleft_x, midbottom_y), self.radius)
		pygame.draw.circle(self.screen, self.color, (midright_x, midbottom_y), self.radius)

		# Draw the text
		if self.display_text!='' and self.font!='' and self.font_size!='' and self.font_color!='':
			# Prepate the fonts
			pygame_font = pygame.font.Font(self.font, self.font_size)

			# Prepare the text
			text = self.display_text
			text_render = pygame_font.render(text, True, self.font_color)
			text_rect = text_render.get_rect()

			# Render the button text
			text_rect.centerx = self.center_x if self.font_x=='' else self.font_x
			text_rect.centery = self.center_y if self.font_y=='' else self.font_y

			# Render text
			self.screen.blit(text_render, text_rect)

		# Draw the image (will take precedence over text)
		if self.image_filename!='':
			# Load image file
			image_piece = pygame.image.load(self.image_filename)

			# Transform height and width, if specified
			if self.image_w!='' and self.image_h!='':
				image_piece = pygame.transform.scale(image_piece, (self.image_w,self.image_h))

			# Position the center
			piece_rect = image_piece.get_rect()
			rect_x = self.center_x if self.image_x=='' else self.image_x
			rect_y = self.center_y if self.image_y=='' else self.image_y
			piece_rect = piece_rect.move((rect_x, rect_y))

			# Render image
			self.screen.blit(image_piece, piece_rect)


	def is_button_pressed(self, x, y):
		pass
