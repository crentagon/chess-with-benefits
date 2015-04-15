from socket import *
from time import ctime
import time
import sys

class ChessServer:

	def __init__(self, host='localhost', port=28888, bufsize=1024):
		self.host = host
		self.port = port
		self.bufsize = bufsize
		self.addr = (self.host, self.port)

	# Starts the server
	def start(self):
		bufsize = self.bufsize

		server_socket = socket(AF_INET,SOCK_STREAM)
		server_socket.bind(self.addr)
		server_socket.listen(2)

		print "[ChessServer]: Waiting for the first connection..."
		client_socket_a, addr_a = server_socket.accept()
		print "[ChessServer]: Conntected! Address:", addr_a

		print "[ChessServer]: Waiting for the second connection..."
		client_socket_b, addr_b = server_socket.accept()
		print "[ChessServer]: Conntected! Address:", addr_b

		print "[ChessServer]: Connections: ", client_socket_a.getsockname(), client_socket_b.getsockname()
		client_socket_a.send("ready-first")
		client_socket_b.send("ready")

		color_a = client_socket_a.recv(bufsize)
		print "[ChessServer]: Sending to socket_b:", color_a
		client_socket_b.send(color_a)

		white_client = client_socket_a if color_a == 'white' else client_socket_b
		black_client = client_socket_a if color_a == 'black' else client_socket_b

		while True:
			print "[ChessServer]: Waiting for white's move..."
			white_move = white_client.recv(bufsize)
			if white_move == 'GAME_OVER':
				break
			black_client.send(white_move)
			print "[ChessServer]: Waiting for black's move..."
			black_move = black_client.recv(bufsize)
			if black_move == 'GAME_OVER':
				break
			print "[ChessServer]: Sending move to white:", black_move
			white_client.send(black_move)

		client_socket_a.close()
		client_socket_b.close()
		server_socket.close()
		sys.exit(0)		

if __name__ == '__main__':
	ChessServer().start()
	# pass