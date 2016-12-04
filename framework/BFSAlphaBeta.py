from Engine import Engine
from Board import *

# Notes and optimizations:
# CURRENTLY JUST ALPHABETA; HAVEN'T ACTUALLY BUILT THIS YET
# DON'T BOTHER READING THIS FILE
# SERIOUSLY STOP


# class SearchNode:
#     def __init__(self, some_params):
#         self.board = board
#         self.successors = pass
#         self.


class BFSAlphaBeta(Engine):
    def __init__(self, eval_function = None):
        self.depth = 3
        self.evaluation_function = eval_function if eval_function is not None else self.default_eval_function

    def default_eval_function(self, board):
        return len(board.legal_moves)

    def get_next_move(self, board):
        # returns (move, eval) pair
        def recurse(board, maximizing, depth, alpha=float("-inf"), beta=float("inf")):
            legal_moves = board.legal_moves

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
