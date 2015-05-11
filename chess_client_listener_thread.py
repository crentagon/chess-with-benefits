from socket import *
import threading

class ChessClientListenerThread(threading.Thread):

	def __init__(self, client_listener_socket, bufsize=1024):
		super(ChessClientListenerThread, self).__init__()
		self.client_listener_socket = client_listener_socket
		self.is_running = True
		self.is_new_message = False
		self.bufsize = bufsize
		self.message = ''

	def get_message(self):
		if self.is_new_message:
			self.is_new_message = False
			return self.message
		return False

	def run(self):
		while self.is_running:
			# print "Listening..."
			self.message = self.client_listener_socket.recv(self.bufsize)
			self.is_new_message = True

	def close(self):
		self.client_listener_socket.close()
		self.is_running = False
		
if __name__ == '__main__':
	ChessClient().start()