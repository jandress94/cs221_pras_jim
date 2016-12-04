from Engine import Engine
from Board import *

# IDEA: A version of alpha-beta that goes as far as possible into forced lines
# This is the most successful engine we have so far. After playing against a normal
# AlphaBeta with 10% randomization, we get the following stats dumps (NOT MOST RECENT):
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


class FLDDAlphaBeta(Engine):
    def __init__(self, eval_function=None, search_threshold=1, max_evals=1000):
        self.depth = 3
        self.max_evals = max_evals
        # We don't decrement depth whenver there are at most search_treshold moves
        # search_treshold = 1 corresponds to checking forced lines
        self.search_threshold = search_threshold
        self.evaluation_function = eval_function if eval_function is not None else self.default_eval_function

    def default_eval_function(self, board):
        return len(board.legal_moves)

    def get_next_move(self, board):
        if len(board.legal_moves) == 1: return (board.legal_moves[0], 0)
        calculated_best_moves = []
        eval_counts = []
        max_evals = self.max_evals
        total_evals = 0
        depth = self.depth
        curr_thresh = self.search_threshold
        while total_evals < max_evals:
            (move, ev), eval_count = self.get_next_move_help(board, depth, curr_thresh, max_evals - total_evals)
            calculated_best_moves.append((move, ev))
            eval_counts.append(eval_counts)
            total_evals += eval_count
            depth += 1
            curr_thresh += 1
        print "Max depth and threshold: ", (depth, curr_thresh)
        # check: the last run finished too early, so penultimate run was better
        # how to check: see which run evaluated more moves! more moves = better depth
        if len(calculated_best_moves) <= 1: return calculated_best_moves[0]
        return calculated_best_moves[len(eval_counts) - 1] \
        if eval_counts[len(eval_counts) - 1] > eval_counts[len(eval_counts) - 2] \
        else calculated_best_moves[len(eval_counts) - 2]

    def get_next_move_help(self, board, curr_depth, curr_thresh, max_evals):
        num_evals = [0]
        # if len(board.legal_moves) == 1: return (board.legal_moves[0], 0)
        # returns (move, eval) pair
        def recurse(board, maximizing, depth, alpha=float("-inf"), beta=float("inf")):
            num_evals[0] += 1
            depth = min(curr_depth, depth)
            # print (alpha, beta)
            legal_moves = board.legal_moves

            if board.get_result() != None or len(legal_moves) == 0 or depth <= 0:
                evaluation = self.evaluation_function(board)
                if board.get_result() != None:
                    if board.get_result() == board.turn:
                        evaluation = float('inf')
                    elif board.get_result() == 'd':
                        evaluation = 0
                    elif board.get_result() != board.turn:
                        evaluation = float('-inf')
                return (None, evaluation)

            # next_depth = depth - 1
            # next_carryover = False
            # if len(legal_moves) <= self.search_threshold and not carryover:
            #     next_depth = depth + 1
            #     next_carryover = len(legal_moves) <= self.search_threshold

            if maximizing:
                # next_depth = depth if len(legal_moves) <= self.search_threshold else depth - 1
                next_depth = depth + 1 if len(legal_moves) <= curr_thresh else depth - 1
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
                # next_depth = depth + 1 if len(legal_moves) <= self.search_threshold and not carryover else depth - 1
                lowest_eval  = float("inf")
                opt_move = None
                next_depth = depth + 1 if len(legal_moves) <= curr_thresh else depth - 1
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
        print "evaluated %d positions" % num_evals[0]
        return (recurse(board, True, curr_depth), num_evals[0])
