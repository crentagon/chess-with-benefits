import threading
import os, sys, signal
import subprocess
from subprocess import *

class StockfishThread(threading.Thread):

	def __init__(self, fen_string, cpu_level):

		super(StockfishThread, self).__init__()
		self.fen_string = fen_string
		self.cpu_level = cpu_level
		self.is_thread_done = False
		self.is_undo_clicked = False

		self.current_move = ''
		self.cpu_move = ''
		self.ponder = ''

	def run(self):

		p = subprocess.Popen( ["stockfish_14053109_32bit.exe"], stdin=PIPE, stdout=PIPE)
		p.stdin.write("position fen "+self.fen_string+"\n")

		cpu_level = self.cpu_level
		quad_factor = (cpu_level - 1)/4
		octa_factor = quad_factor/2

		depth = cpu_level if cpu_level < 5 else (cpu_level - ((2 + (3*octa_factor))))*(2*quad_factor)
		uci_level = cpu_level*3 - ((cpu_level-1)/3) if cpu_level < 8 else 20
		move_time = cpu_level*50 if cpu_level <= 8 else (2**(cpu_level - 9))*1000

		p.stdin.write("setoption name Skill Level value "+str(uci_level)+"\n")
		p.stdin.write("go depth "+str(depth)+" movetime "+str(move_time)+"\n")

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
		