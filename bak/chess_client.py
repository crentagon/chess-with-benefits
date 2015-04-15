from socket import *

class ChessClientThread(threading.Thread):

	def __init__(self, host='localhost', port=28888, bufsize=1024):
		super(ChessClientThread, self).__init__()
		self.host = host
		self.port = port
		self.bufsize = bufsize
		self.addr = (self.host, self.port)

		self.client_socket = ''
		self.is_connected = False
		self.is_polling = False

	def connect(self):
		self.client_socket = socket(AF_INET, SOCK_STREAM)
		self.client_socket.connect(self.addr)
		self.is_connected = True
		return True

	def receive_data(self):
		return self.client_socket.recv(self.bufsize)

	def send_data(self, message):
		self.client_socket.send(message)
		return True

	# def start(self):
	# 	# Wait for the server to tell us that both players are ready.
	# 	client_socket = socket(AF_INET, SOCK_STREAM)
	# 	client_socket.connect(self.addr)
	# 	bufsize = self.bufsize

	# 	if client_socket.recv(bufsize) == 'ready':
	# 		# Ask for the color to play as, which will determine the order.
	# 		color = raw_input('Color: ')
	# 		client_socket.send(color)

	# 		while True:
	# 			if color == 'white':
	# 				move = raw_input('')
	# 				client_socket.send(move)
	# 				print client_socket.recv(bufsize)
	# 			else:
	# 				print client_socket.recv(bufsize)
	# 				move = raw_input('')
	# 				client_socket.send(move)

	# 	else:
	# 		print "[ChessClient]: Something went horribly wrong. D:"

if __name__ == '__main__':
	ChessClient().start()