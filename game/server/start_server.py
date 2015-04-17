from server_thread import *

def run(self):
	if self.is_server_running:
		self.server_thread = ServerThread(self.addr, self.bufsize)
		self.server_thread.start()