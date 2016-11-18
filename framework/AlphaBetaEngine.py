from Engine import Engine
from Board import *

# Notes and optimizations:
# -> currently creates every board from scratch, which is expensive.
#   would be better to keep track of some sort of game tree, and expand when needed
# -> uses simple eval function, should eventually use Features.py for eval function
# -> simple eval function beats Random() every time, perhaps can serve as an improved baseline.
# -> AlphaBeta has a hard time moving first because of all the possibilities. It might be useful
#   to keep a small opening book (like a few moves which are known not to be totally losing)
#   and playing one of those at random.

class AlphaBeta(Engine):
    def __init__(self, eval_function = None):
        self.depth = 3
        self.evaluation_function = eval_function if eval_function is not None else self.default_eval_function

    def default_eval_function(self, board):
        return len(board.get_legal_moves())

    def get_next_move(self, board):
        # returns (move, eval) pair
        def recurse(board, maximizing, depth, alpha=float("-inf"), beta=float("inf")):
            legal_moves = board.get_legal_moves()

            if board.get_result() != None or len(legal_moves) == 0 or depth == 0:
                return (None, self.evaluation_function(board))

            if maximizing:
                highest_eval = float("-inf")
                opt_move = None
                for move in legal_moves:
                    succ = board.make_move_from_move(move)
                    highest_eval = max(highest_eval, \
                    recurse(succ, not maximizing, depth - 1, alpha, beta)[1])
                    if highest_eval > alpha:
                        alpha = highest_eval
                        opt_move = move
                    # cutoff
                    if beta <= alpha:
                        break
                return (opt_move, highest_eval)
            else:
                lowest_eval  = float("inf")
                opt_move = None
                for move in legal_moves:
                    succ = board.make_move_from_move(move)
                    lowest_eval = min(lowest_eval, \
                    recurse(succ, not maximizing, depth - 1, alpha, beta)[1])
                    if lowest_eval < beta:
                        beta = lowest_eval
                        opt_move = move
                    # cutoff
                    if beta <= alpha:
                        break
                return (opt_move, lowest_eval)

        return recurse(board, True, self.depth)
