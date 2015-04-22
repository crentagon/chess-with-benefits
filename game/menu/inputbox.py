import pygame, pygame.event, sys
from pygame.locals import *


class InputBox():

	def __init__(self, screen, center_x, center_y, width=200, height=20, length=20, font=None,
		font_size=10, font_color=(0,0,0), textbox_bg=(0,0,0), border_color=(255,255,255),
		border_width=1, message=''):

		# Textbox information
		self.border_color = border_color
		self.border_width = border_width
		self.textbox_bg = textbox_bg
		self.is_active = False
		self.screen = screen
		self.message = message
		self.height = height
		self.width = width
		self.length = length

		# Font information
		self.font_color = font_color
		self.font_size = font_size
		self.center_x = center_x
		self.center_y = center_y
		self.font = font

	def get_key(self):
		while True:
			for event in pygame.event.get():
				if event.type == KEYDOWN:
					return event.key
				elif event.type == 5:
					mouse_pos = pygame.mouse.get_pos()
					x_coord = mouse_pos[0]
					y_coord = mouse_pos[1]
					self.is_textbox_active(x_coord, y_coord)
					return False
				elif event.type == pygame.QUIT:
					sys.exit(0)

	def draw_textbox(self):
		x = self.center_x
		y = self.center_y
		w = self.width
		h = self.height
		rect = (x, y, w, h)

		border_color = self.border_color if not self.is_active else (255,0,0)
		border_width = self.border_width if not self.is_active else int(self.border_width*2)

		pygame.draw.rect(self.screen, self.textbox_bg, rect, 0)
		pygame.draw.rect(self.screen, border_color, rect, border_width)

		message = self.message

		if len(message) != 0:
			basic_font = pygame.font.Font(self.font, self.font_size)
			text_char = basic_font.render(message, True, (0,0,0))
			char_rect = text_char.get_rect()
			char_rect.centerx = x + (char_rect.width)/2
			char_rect.centery = y + (char_rect.height)/2
			self.screen.blit(text_char, char_rect)

	def ask(self, question=''):
		self.draw_textbox()
		pygame.display.update()

		while self.is_active:
			inkey = self.get_key()
			if inkey:
				if inkey == K_BACKSPACE:
					self.message = self.message[0:-1]
				elif inkey == K_RETURN:
					self.is_active = False
				elif inkey <= 127 and len(self.message)<self.length:
					self.message = self.message + chr(inkey)

			self.draw_textbox()
			pygame.display.update()

	def get_message(self):
		return self.message

	def is_textbox_active(self, x, y):
		self.is_active = False

		# X-coordinates
		right_x = self.center_x + self.width
		left_x = self.center_x

		# Y-coordinates
		bottom_y = self.center_y + self.height
		top_y = self.center_y

		# Checker for is button pressed
		is_x_coord = x <= right_x and x >= left_x
		is_y_coord = y >= top_y and y <= bottom_y

		if is_x_coord and is_y_coord:
			print "Got in line 100 of inputbox.py, message:", self.message
			self.is_active = True
			return True

		return False


"""

def ask(screen, question):
  "ask(screen, question) -> answer"
  pygame.font.init()
  message = []
  draw_textbox(screen, question + ": " + string.join(message,""))
  while 1:
    inkey = get_key()
    if inkey == K_BACKSPACE:
      message = message[0:-1]
    elif inkey == K_RETURN:
      break
    elif inkey == K_MINUS:
      message.append("_")
    elif inkey <= 127:
      message.append(chr(inkey))
    draw_textbox(screen, question + ": " + string.join(message,""))
  return string.join(message,"")


def draw_textbox(screen, message):
  "Print a message in a box in the middle of the screen"
  fontobject = pygame.font.Font(None,18)
  pygame.draw.rect(screen, (0,0,0),
                   ((screen.get_width() / 2) - 100,
                    (screen.get_height() / 2) - 10,
                    200,20), 0)
  pygame.draw.rect(screen, (255,255,255),
                   ((screen.get_width() / 2) - 102,
                    (screen.get_height() / 2) - 12,
                    204,24), 1)
  if len(message) != 0:
    screen.blit(fontobject.render(message, 1, (255,255,255)),
                ((screen.get_width() / 2) - 100, (screen.get_height() / 2) - 10))
  pygame.display.flip()

def main():
  screen = pygame.display.set_mode((320,240))
  print ask(screen, "Name") + " was entered"

if __name__ == '__main__': main()
"""