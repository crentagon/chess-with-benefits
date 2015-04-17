from socket import *
import threading

class ChessClientListenerThread(threading.Thread):

	def __init__(self, client_listener_socket, bufsize):
		super(ChessClientListenerThread, self).__init__()
		self.client_listener_socket = client_listener_socket
		self.is_new_message = False
		self.bufsize = bufsize
		self.message = ''

	def get_message(self):
		return self.message

	def start(self):
		while self.message != 'QUIT':
			self.message = self.client_listener_socket.recv(self.bufsize)
			self.is_new_message = True
		
	"""
	def connect(self):
		if not self.is_connected:
			self.client_socket = socket(AF_INET, SOCK_STREAM)
			self.client_socket.connect(self.addr)
			self.is_connected = True
			print "Connection successful."
			return True
		return False

	def receive_data(self):
		self.is_polling = True
		self.return_message = self.client_socket.recv(self.bufsize)
		self.is_polling = False

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
	"""
if __name__ == '__main__':
	ChessClient().start()