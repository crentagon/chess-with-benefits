import threading
from socket import *
from time import ctime
import time
import sys
import re

class ServerThread(threading.Thread):

	def __init__(self, addr, bufsize):
		super(ServerThread, self).__init__()
		self.is_server_running = True
		self.is_new_message = False
		self.bufsize = bufsize
		self.message = ''
		self.addr = addr

		self.server_socket = None
		self.client_socket_a = None
		self.client_socket_b = None

	def run(self):
		bufsize = self.bufsize

		self.server_socket = socket(AF_INET,SOCK_STREAM)
		self.server_socket.bind(self.addr)
		self.server_socket.listen(2)

		self.broadcast_message("Waiting for the first connection...")
		self.client_socket_a, addr_a = self.server_socket.accept()
		self.broadcast_message("Conntected! Address:" + str(addr_a))

		self.broadcast_message("Waiting for the second connection...")
		self.client_socket_b, addr_b = self.server_socket.accept()
		self.broadcast_message("Conntected! Address:" + str(addr_b))

		self.broadcast_message("Connections: " + str(self.client_socket_a.getsockname()) + str(self.client_socket_b.getsockname()))
		self.client_socket_a.send("ready-first")
		self.client_socket_b.send("ready")

		# First player says "READY!"
		color_a = self.client_socket_a.recv(bufsize)
		self.broadcast_message("Sending to socket_b:" + str(color_a))
		if self.is_message_game_over(color_a, self.client_socket_b):
			return
		self.client_socket_b.send(color_a)

		# Second player says "READY!"
		ready_b = self.client_socket_b.recv(bufsize)
		if self.is_message_game_over(ready_b, self.client_socket_a):
			return
		self.client_socket_a.send(ready_b)

		# Check color
		is_white = re.compile('white_(.*)')
		is_white = is_white.match(color_a)

		white_client = self.client_socket_a if is_white else self.client_socket_b
		black_client = self.client_socket_a if not is_white else self.client_socket_b

		while self.is_server_running:
			# White's move
			self.broadcast_message("Waiting for white's move...")
			white_move = white_client.recv(bufsize)
			
			self.broadcast_message("Received white's move: "+white_move)
			black_client.send(white_move)
			if white_move == 'GAME_OVER' or not self.is_server_running:
				break

			# Black's move
			self.broadcast_message("Waiting for black's move...")
			black_move = black_client.recv(bufsize)
			self.broadcast_message("Received black's move: "+black_move)
			white_client.send(black_move)
			if black_move == 'GAME_OVER' or not self.is_server_running:
				break

		time.sleep(1)
		white_client.send("GAME_OVER")
		black_client.send("GAME_OVER")
		time.sleep(1)
		print "---Closing shop."
		self.client_socket_a.close()
		self.client_socket_b.close()
		self.server_socket.close()

	def is_message_game_over(self, message, target_client):
		if message == 'GAME_OVER':
			target_client.send(message)
			self.server_socket.close()
			self.stop_thread()
			return True
		return False

	def broadcast_message(self, message):
		self.is_new_message = True
		self.message = message

	def get_message(self):
		self.is_new_message = False
		return self.message

	def stop_thread(self):
		self.is_server_running = False
		