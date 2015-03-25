import threading
import os, sys, signal
import subprocess
from subprocess import *

class StalemateThread(threading.Thread):

	def __init__(self, fen_string):

		super(StalemateThread, self).__init__()
		self.fen_string = fen_string
		self.is_thread_done = False
		self.is_undo_clicked = False
		self.is_stalemate = False
		self.is_checkmate = False

		self.cpu_move = ''
		self.ponder = ''

	def run(self):

		p = Popen( ["stockfish_14053109_32bit.exe"], stdin=PIPE, stdout=PIPE)
		p.stdin.write("position fen "+self.fen_string+"\n")
		p.stdin.write("go depth 1\n")
		line_count = 0

		while p.poll() is None:
			line = p.stdout.readline()
			line_count += 1

			if line_count == 2: break

		line = line.split("\r")
		line = line[0].split(" ")

		if line[2] == '0':
			if line[4] == 'cp':
				self.is_stalemate = True
			elif line[4] == 'mate':
				self.is_checkmate = True

		self.is_thread_done = True