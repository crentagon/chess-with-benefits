from constants import *
from stockfish_thread import *
import pygame

#play
def run(self):
	self.build_threats(self.board)

	fen_string = self.convert_to_fen()
	current_move = ''
	self.stack.push([fen_string, current_move])
	# print "Pushed:", fen_string

	has_player_moved = False
	has_opponent_moved = False

	if fen_string == "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1":
		is_turn_user = True if self.is_player_white else False
		is_turn_opponent = False if is_turn_user else True
	else:
		is_active_turn_white = self.active_turn == 'w'
		is_turn_user = self.is_player_white == is_active_turn_white
		is_turn_opponent = False if is_turn_user else True

	thread = None
	self.is_board_changed = True

	while(True):			
		if self.is_board_changed or self.is_animating:
			self.render_board()
			self.is_board_changed = False

		if has_player_moved or has_opponent_moved:
			self.board_status = 'in_game'
			self.clear_traversable()				
			self.build_threats(self.board)
			self.is_board_changed = True

			if has_player_moved:
				self.active_turn = 'b' if self.is_player_white else 'w'
				has_player_moved = False
				is_turn_opponent = True
				is_turn_user = False

			elif has_opponent_moved:
				self.active_turn = 'w' if self.is_player_white else 'b'
				has_opponent_moved = False
				is_turn_opponent = False
				is_turn_user = True

			if not (self.board_status == 'promoting' or self.is_game_over[self.board_status]):
				fen_string = self.convert_to_fen()
				self.stack.push([fen_string, current_move])
				self.endgame_check(fen_string) # Check if there is a stalemate or checkmate
				print "After:", fen_string

		if self.debug_mode:
			is_turn_opponent = False
			is_turn_user = True

		# CPU Opponent's Turn
		if not self.is_two_player:
			if not self.debug_mode and is_turn_opponent and not (self.board_status == 'promoting' or self.is_game_over[self.board_status]):
				print fen_string
				thread = StockfishThread(fen_string, self.cpu_level)

				thread.start()
				is_turn_opponent = False

			if thread is not None:

				if thread.current_move is not None:
					cpu_current_move = thread.current_move

					# Current move
					if len(cpu_current_move) == 4:
						currmove_source_x = Constants.PIECE_MAPPING[cpu_current_move[:1]]
						currmove_source_y = Constants.PIECE_MAPPING[cpu_current_move[1:2]]
						currmove_destination_x = Constants.PIECE_MAPPING[cpu_current_move[2:3]]
						currmove_destination_y = Constants.PIECE_MAPPING[cpu_current_move[3:4]]

						is_source_x_equal = currmove_source_x == self.currmove_source_x
						is_source_y_equal = currmove_source_y == self.currmove_source_y
						is_destination_x_equal = currmove_destination_x == self.currmove_destination_x
						is_destination_y_equal = currmove_destination_y == self.currmove_destination_y

						if not (is_source_y_equal and is_source_x_equal and is_destination_y_equal and is_destination_x_equal):
							self.clear_current_movement()

							self.currmove_source_x = currmove_source_x 
							self.currmove_source_y = currmove_source_y
							self.currmove_destination_x = currmove_destination_x
							self.currmove_destination_y = currmove_destination_y

							self.board[currmove_source_x][currmove_source_y].is_current_movement = True
							self.board[currmove_destination_x][currmove_destination_y].is_current_movement = True

				if thread.is_thread_done is not None and thread.is_thread_done:

					thread.join()
					self.clear_current_movement()

					if not thread.is_undo_clicked:
						cpu_move = thread.cpu_move
						current_move = cpu_move
						ponder = thread.ponder

						print cpu_move
						print ponder

						source_x = Constants.PIECE_MAPPING[cpu_move[:1]]
						source_y = Constants.PIECE_MAPPING[cpu_move[1:2]]
						destination_x = Constants.PIECE_MAPPING[cpu_move[2:3]]
						destination_y = Constants.PIECE_MAPPING[cpu_move[3:4]]
						promotion = False

						if len(cpu_move) == 5:
							promotion = cpu_move[4:5]
							promotion_map = {
								"r": Constants.P_ROOK,
								"b": Constants.P_BISHOP,
								"n": Constants.P_KNIGHT,
								"q": Constants.P_QUEEN
							}
							promotion = promotion_map[promotion]

						self.move_piece(source_x, source_y, destination_x, destination_y, promotion)

						has_opponent_moved = True
						thread.is_thread_done = False

					thread = None

		# Wait for the human opponent's turn
		else:
			message = self.listener.get_message()
			if message:
				if message != 'GAME_OVER':
					source_x = Constants.PIECE_MAPPING[message[:1]]
					source_y = Constants.PIECE_MAPPING[message[1:2]]
					destination_x = Constants.PIECE_MAPPING[message[2:3]]
					destination_y = Constants.PIECE_MAPPING[message[3:4]]
					promotion = False

					if len(message) == 5:
						promotion = message[4:5]
						promotion_map = {
							"r": Constants.P_ROOK,
							"b": Constants.P_BISHOP,
							"n": Constants.P_KNIGHT,
							"q": Constants.P_QUEEN
						}
						promotion = promotion_map[promotion]

					self.move_piece(source_x, source_y, destination_x, destination_y, promotion)
					has_opponent_moved = True
				else:
					print "Got message", message
					return "main_menu"

		for event in pygame.event.get(): 
			self.is_board_changed = True
			
			if event.type == pygame.QUIT:
				if self.is_two_player:
					print "Sending GAME_OVER"
					self.speaker.send_message("GAME_OVER")
					self.listener.close()
				print "Exiting."
				sys.exit(0)

			# User's turn
			elif event.type == 5:
				mouse_pos = pygame.mouse.get_pos()

				if self.is_player_white:
					board_x = (mouse_pos[0] - Constants.BOARD_BUFFER)/Constants.TILE_LENGTH
					board_y = 7-((mouse_pos[1] - Constants.BOARD_BUFFER)/Constants.TILE_LENGTH)
				else:
					board_x = 7-((mouse_pos[0] - Constants.BOARD_BUFFER)/Constants.TILE_LENGTH)
					board_y = (mouse_pos[1] - Constants.BOARD_BUFFER)/Constants.TILE_LENGTH

				is_piece_clicked = False
				is_traversable = False
				promotion = ''

				# Did the user click on the board?
				if 0 <= board_x <= 7 and 0 <= board_y <= 7 and self.is_board_clickable and is_turn_user:
					# What did the user click? A piece? A tile? Is the tile traversable?
					tile = self.board[board_x][board_y]
					piece = tile.piece
					is_traversable = tile.is_traversable
					is_piece_clicked = piece is not None

				# The user clicked somewhere else!
				else:
					# Is the user clicking on the sidebar?
					action = ''
					if mouse_pos[0] >= (Constants.SCREENSIZE[0] - Constants.SIDEBAR_WIDTH):
						index = 65536
						if mouse_pos[1] % (Constants.SIDEBAR_BUTTON) >= Constants.BOARD_BUFFER:
							index = (mouse_pos[1]/Constants.SIDEBAR_BUTTON)

						if index < len(self.sidebar_buttons):
							action = self.sidebar_buttons[index][2]
						

					# Is the game over and the user is clicking on the game over options?
					elif self.is_game_over[self.board_status]:
						# Check if mouse_x is within range
						lower_bound = Constants.AFTERGAME_COORD[0]
						upper_bound = Constants.AFTERGAME_COORD[0] + Constants.AFTERGAME_WIDTH
						if mouse_pos[0] >= lower_bound and mouse_pos[0] <= upper_bound:
							# Check where mouse_y is clicking
							index = 65536
							if mouse_pos[1] >= Constants.AFTERGAME_COORD[1]:
								neutralized = mouse_pos[1]-Constants.AFTERGAME_COORD[1]
								index = (neutralized/(Constants.AFTERGAME_HEIGHT+Constants.BOARD_BUFFER))

							if index < len(self.aftergame_options):
								self.is_game_over = False
								action = self.aftergame_options[index][1]

					if action == 'undo':
						# Cannot undo if stack only has one element
						if self.stack.size() > 1:
							# After an undo, it'll always be your turn unless it's the first move
							self.active_turn = 'w' if self.is_player_white else 'b'

							# print has_player_moved
							# sys.exit(0)

							# If the player has just moved, we pop twice
							if not is_turn_user:
								self.stack.pop()
								element = self.stack.pop()
								fen = element[0]

								if thread is not None:
									thread.is_undo_clicked = True

								self.stack.push(element)
								
								is_turn_opponent = False
								is_turn_user = True

							# If the opponent has just moved...
							else:
								# If it's the very first move, we push it again.
								if self.stack.size() == 2:
									self.stack.pop()
									element = self.stack.pop()
									fen = element[0]
									# print "Popped thrice?", fen

									is_turn_opponent = False
									is_turn_user = True

									self.stack.push(element)
									# print "Pushed*:", fen

									if not self.is_player_white:
										self.active_turn = 'w'
										is_turn_opponent = True
										is_turn_user = False
									elif thread is not None:
										thread.is_undo_clicked = True

								else:
									# ...we pop thrice.
									self.stack.pop()
									self.stack.pop()
									element = self.stack.pop()
									fen = element[0]
									# print "Popped thrice?", fen

									is_turn_opponent = False
									is_turn_user = True

									self.stack.push(element)
									# print "Pushed*:", fen

							fen_string = fen
							self.convert_fen_to_board(fen)

							self.board_status = 'in_game'

							index = self.fullmove_clock #if self.is_player_white else self.fullmove_clock - 1
							opp_index = self.fullmove_clock if self.is_player_white else self.fullmove_clock + 1
							self.opponent_captured.search_and_pop(opp_index)
							self.user_captured.search_and_pop(index)

							self.clear_current_movement()
							self.clear_traversable()
							self.build_threats(self.board)
							self.clear_last_movement()
							self.is_board_changed = True

					elif action == 'main_menu':
						# TO-DO/NOTE: export PGN and save to Database WHEN play again/main menu/close game clicked
						return 'main_menu'

					elif action == 'play_again':
						# TO-DO/NOTE: export PGN and save to Database WHEN play again/main menu/close game clicked
						return 'single_player_menu' # Return 'two_player_search_menu' instead if two-player

					# Is the user clicking on the promotion buttons?
					for i in range(4):
						if self.board_status == 'promoting' and self.promotions[i].pressed(mouse_pos):
							promotion = self.promotions[i].piece_type

							if promotion != '':
								self.board[self.source_x][self.source_y].piece.piece_type = promotion
								hp_converter = {
									0: 1,
									9: 9,
									5: 5,
									3: 3,
									4: 3,
									1: 1,
								}
								self.user_hp_current += (hp_converter[promotion] - 1)
								self.is_board_clickable = True
								self.board_status = 'in_game'

								if self.is_two_player:
									letter_converter = {
										9: 'q',
										5: 'r',
										4: 'b',
										3: 'n'
									}
									self.move_string += letter_converter[promotion]
									self.speaker.send_message(self.move_string)

							has_player_moved = True
							break

				# A piece has been clicked!
				if is_piece_clicked and self.is_board_clickable and is_turn_user:
					# Let's check if it's a friendly piece
					if piece.pressed(mouse_pos):
						self.source_x = board_x
						self.source_y = board_y
						self.show_traversable(board_x, board_y)

					# It clicked on a traversable piece? User's gonna do a capture! Good for you, user.
					elif tile.is_traversable:
						is_traversable = True

					# User clicked on an enemy, uncapturable piece. Not this time!
					else:
						self.clear_traversable()

				# Looks like user clicked on a traversable tile
				if is_traversable:						
					self.clear_traversable()
					self.move_piece(self.source_x, self.source_y, board_x, board_y)
					has_player_moved = True

					if self.is_two_player:
						source_move_x = Constants.CHAR_MAPPING[self.source_x]
						source_move_y = Constants.NUM_MAPPING[self.source_y]
						destination_move_x = Constants.CHAR_MAPPING[board_x]
						destination_move_y = Constants.NUM_MAPPING[board_y]
						self.move_string = source_move_x + source_move_y + destination_move_x + destination_move_y

					# Pawn promotion
					if board_y == self.goal_rank and self.board[board_x][board_y].piece.piece_type == Constants.P_PAWN:
						self.is_board_clickable = False
						self.board_status = 'promoting'
						self.source_x = board_x
						self.source_y = board_y
					else:
						if self.is_two_player:
							self.speaker.send_message(self.move_string)

				# User clicked on tile that is not traversable? We cool as long as user didn't click on its own piece.
				else:
					if not is_piece_clicked:
						self.clear_traversable()

			# else: 
			# 	print event