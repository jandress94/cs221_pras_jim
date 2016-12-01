from Engine import Engine
from Board import *

# Notes and optimizations:
# IDEA: if the tree grows exponentially, then redoing things isn't actually expensive
# eg, if the number of nodes at each depth is 1, 2, ..., 2^n,
# then doing these n evaluations is only 2^(n + 1) in expense. This is better than just guessing n.
# i.e., it's slower by a linear factor, which is fine for big O, but isn't good enough!!


class DynamicDepthAlphaBeta(Engine):
    def __init__(self, eval_function=None, max_evals=1000):
        self.depth = 3
        self.max_evals = max_evals
        self.evaluation_function = eval_function if eval_function is not None else self.default_eval_function

    def default_eval_function(self, board):
        return len(board.get_legal_moves())

    def get_next_move(self, board):
        calculated_best_moves = []
        eval_counts = []
        max_evals = self.max_evals
        num_evals = 0
        depth = self.depth
        while num_evals < max_evals:
            (move, ev), eval_count = self.get_next_move_help(board, depth, max_evals - num_evals)
            calculated_best_moves.append((move, ev))
            eval_counts.append(eval_counts)
            num_evals += eval_count
            depth += 1
        # print "Max depth: ", depth
        # check: the last run finished too early, so penultimate run was better
        # how to check: see which run evaluated more moves! more moves = better depth
        if len(calculated_best_moves) <= 1: return calculated_best_moves[0]
        return calculated_best_moves[len(eval_counts) - 1] \
        if eval_counts[len(eval_counts) - 1] > eval_counts[len(eval_counts) - 2] \
        else calculated_best_moves[len(eval_counts) - 2]





    def get_next_move_help(self, board, curr_depth, max_evals):
        num_evals = [0]
        maxminzing_player = board.turn
        # returns (move, eval) pair
        def recurse(board, maximizing, depth, alpha=float("-inf"), beta=float("inf")):
            num_evals[0] += 1
            legal_moves = board.get_legal_moves()

            if board.get_result() != None or len(legal_moves) == 0 or (depth <= 0 or num_evals[0] >= self.max_evals):
                evaluation = self.evaluation_function(board)
                # if board.get_result() == board.turn:
                #     evaluation = float('inf')
                # elif board.get_result() == 'd':
                #     evaluation = 0
                # elif board.get_result() != board.turn:
                #     evaluation = float('-inf')
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

        return (recurse(board, True, curr_depth), num_evals[0])
