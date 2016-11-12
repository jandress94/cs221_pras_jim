import sys
from Engine import Engine

class Lichess(Engine):
    def __init__(self, data, color):
    	Engine.__init__(self)
    	self.game_data = data
    	self.player = 0 if color == 'w' else 1
    	self.moveIndex = 0

    def get_next_move(self, board):
    	if self.moveIndex >= len(self.game_data):
    		print 'Error simulating Lichess game: No more moves'
    		sys.exit(1)

    	move = board.algebraic_to_se(self.game_data[self.moveIndex][self.player])

    	if move.params not in [poss.params for poss in board.get_legal_moves()]:
    		print 'Error simulating Lichess game: a move in the game is not valid (', str(move), ')'
    		sys.exit(1)

    	self.moveIndex += 1

        return move, 0