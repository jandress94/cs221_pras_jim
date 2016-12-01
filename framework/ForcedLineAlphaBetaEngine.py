from Engine import Engine
from Board import *

# IDEA: A version of alpha-beta that goes as far as possible into forced lines
# This is the most successful engine we have so far. After playing against a normal
# AlphaBeta with 10% randomization, we get the following stats dumps:
# As WHITE:
# In 10 games there were 8 wins for white, 2 wins for black, and 0 draws
# On average, the winner was certain of a win 6 moves before the win
# **************** TOTALS FOR WHITE ****************
# On average,  white  made  25.3  moves
# On average,  white  had  12.6628378863  legal moves
# **************** TOTALS FOR BLACK ****************
# On average,  black  made  25.1  moves
# On average,  black  had  7.6592784744  legal moves
#
# As BLACK:
# In 10 games there were 0 wins for white, 10 wins for black, and 0 draws
# On average, the winner was certain of a win 13 moves before the win
# **************** TOTALS FOR WHITE ****************
# On average,  white  made  20.7  moves
# On average,  white  had  5.81346473562  legal moves
# **************** TOTALS FOR BLACK ****************
# On average,  black  made  19.7  moves
# On average,  black  had  10.6810538155  legal moves
#
# NOTE: there may be bug in "certain of win before..." code, I think i fixed it; will check in morning


class ForcedLineAlphaBeta(Engine):
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
                evaluation = self.evaluation_function(board)
                if board.get_result() != None:
                    if board.get_result() == board.turn:
                        evaluation = float('inf')
                    elif board.get_result() == 'd':
                        evaluation = 0
                    elif board.get_result() != board.turn:
                        evaluation = float('-inf')
                return (None, evaluation)

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
                next_depth = depth + 1 if len(legal_moves) <= 1 else depth - 1
                for move in legal_moves:
                    succ = board.make_move_from_move(move)
                    lowest_eval = min(lowest_eval, \
                    recurse(succ, not maximizing, next_depth, alpha, beta)[1])
                    if lowest_eval < beta:
                        beta = lowest_eval
                        opt_move = move
                    # cutoff
                    if beta <= alpha:
                        break
                return (opt_move, lowest_eval)

        return recurse(board, True, self.depth)
