from stalemate_thread import *

#endgame_check
def run(self, fen_string):
	is_started = False
	
	while True:
		if not is_started:
			thread = StalemateThread(fen_string)
			thread.start()
			is_started = True

		if thread is not None and thread.is_thread_done is not None and thread.is_thread_done:
			thread.join()

			if thread.is_stalemate:
				self.is_stalemate = True
				self.is_game_over = True
				print "Stalemate!"					
				return

			elif thread.is_checkmate:
				if self.active_turn == 'w':
					if self.is_player_white:
						self.is_user_checkmate = True
					else:
						self.is_opponent_checkmate = True

				elif self.active_turn == 'b':
					if self.is_player_white:
						self.is_opponent_checkmate = True
					else:
						self.is_user_checkmate = True

				self.is_game_over = True
				print "Checkmate!"
				return

			elif self.halfmove_clock >= 100:
				self.is_50_move_rule = True
				self.is_game_over = True
				print "50-move rule!"
				return
			return