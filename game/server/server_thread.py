import threading
from socket import *
from time import ctime
import time
import sys

class ServerThread(threading.Thread):

	def __init__(self, addr, bufsize):
		super(ServerThread, self).__init__()
		self.is_server_running = True
		self.is_new_message = False
		self.bufsize = bufsize
		self.message = ''
		self.addr = addr

	def run(self):
		bufsize = self.bufsize

		server_socket = socket(AF_INET,SOCK_STREAM)
		server_socket.bind(self.addr)
		server_socket.listen(2)

		self.broadcast_message("Waiting for the first connection...")
		client_socket_a, addr_a = server_socket.accept()
		self.broadcast_message("Conntected! Address:" + str(addr_a))

		self.broadcast_message("Waiting for the second connection...")
		client_socket_b, addr_b = server_socket.accept()
		self.broadcast_message("Conntected! Address:" + str(addr_b))

		self.broadcast_message("Connections: " + str(client_socket_a.getsockname()) + str(client_socket_b.getsockname()))
		client_socket_a.send("ready-first")
		client_socket_b.send("ready")

		color_a = client_socket_a.recv(bufsize)
		self.broadcast_message("Sending to socket_b:" + str(color_a))
		client_socket_b.send(color_a)

		white_client = client_socket_a if color_a == 'white' else client_socket_b
		black_client = client_socket_a if color_a == 'black' else client_socket_b

		while self.is_server_running:
			# White's move
			self.broadcast_message("Waiting for white's move...")
			white_move = white_client.recv(bufsize)
			
			self.broadcast_message("Received white's move: "+white_move)
			if white_move == 'GAME_OVER' or not self.is_server_running:
				black_client.send('GAME_OVER')
				break
			black_client.send(white_move)

			# Black's move
			self.broadcast_message("Waiting for black's move...")
			black_move = black_client.recv(bufsize)
			self.broadcast_message("Received black's move: "+black_move)
			if black_move == 'GAME_OVER' or not self.is_server_running:
				black_client.send('GAME_OVER')
				break
			white_client.send(black_move)

		client_socket_a.close()
		client_socket_b.close()
		server_socket.close()

	def broadcast_message(self, message):
		self.is_new_message = True
		self.message = message

	def get_message(self):
		self.is_new_message = False
		return self.message

	def stop_thread(self):
		self.is_server_running = False
		