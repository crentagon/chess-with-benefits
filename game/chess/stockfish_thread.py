import threading
import os, sys, signal
import subprocess
from subprocess import *

class StockfishThread(threading.Thread):

	def __init__(self, fen_string, process_time):

		super(StockfishThread, self).__init__()
		self.fen_string = fen_string
		self.process_time = process_time
		self.is_thread_done = False
		self.is_undo_clicked = False

		self.current_move = ''
		self.cpu_move = ''
		self.ponder = ''

	def run(self):

		p = subprocess.Popen( ["stockfish_14053109_32bit.exe"], stdin=PIPE, stdout=PIPE)
		p.stdin.write("position fen "+self.fen_string+"\n")
		p.stdin.write("go movetime "+str(self.process_time)+"\n")

		# Debugging code ignore pls:
		# p.stdin.write("go depth 20\n")
		# print "<YAY>"
		# print "position fen "+self.fen_string
		# print "go movetime "+str(self.process_time)
		# print "</YAY>"
		# print "PID", p.pid
		# p.stdin.write("quit\n")
		# subprocess.call(['taskkill', '/F', '/T', '/PID', str(p.pid)])

		while p.poll() is None:
			line = p.stdout.readline()

			currmove = line.split("\r")
			currmove = line.split(" ")
			if len(currmove) > 18:
				self.current_move = currmove[17]

			if line[0] == 'b': break
			# print line

		# Retrieving the best move
		line = line.split("\r")
		line = line[0].split(" ")

		self.cpu_move = line[1]
		self.ponder = line[3]
		self.is_thread_done = True

		subprocess.Popen("taskkill /T /F /IM stockfish_14053109_32bit.exe")
		