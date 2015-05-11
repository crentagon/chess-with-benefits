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
				self.board_status = 'stalemate'			
				return

			elif thread.is_checkmate:
				if self.active_turn == 'w':
					self.board_status = 'user_checkmate' if self.is_player_white else 'opponent_checkmate'

				elif self.active_turn == 'b':
					self.board_status = 'opponent_checkmate' if self.is_player_white else 'user_checkmate'

				return

			elif self.halfmove_clock >= 100:
				self.board_status = '50_move_rule'
				return
				
			return