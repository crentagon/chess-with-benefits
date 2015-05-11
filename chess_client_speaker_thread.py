from socket import *
import threading

class ChessClientSpeakerThread(threading.Thread):

	def __init__(self, client_speaker_socket, bufsize=1024):
		super(ChessClientSpeakerThread, self).__init__()
		self.client_speaker_socket = client_speaker_socket
		self.is_running = True
		self.bufsize = bufsize
		self.message = ''

	def send_message(self, message):
		self.message = message

	def run(self):
		while self.is_running:
			if self.message != '' and self.is_running:
				# print "> Sending the following message:", self.message
				self.client_speaker_socket.send(self.message)
				# print "> Sent the following message:", self.message
				self.message = ''

	def close(self):
		self.client_speaker_socket.send("GAME_OVER")
		self.client_speaker_socket.close()
		self.is_running = False