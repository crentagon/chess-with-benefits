from socket import *
from time import ctime
import time
import sys
from game.server import (
	start_server,
	render_menu,
	initialize,
	play
)

class ChessServer:

	def __init__(self, host='192.168.1.20', port=8888, bufsize=1024):
		# To-do: Check for external IP address
		initialize.run(self, host, port, bufsize)

	def render_menu(self):
		render_menu.run(self)

	def play(self):
		play.run(self)

	def start_server(self):
		start_server.run(self)

if __name__ == '__main__':
	ChessServer().play()
	# pass