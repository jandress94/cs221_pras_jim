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


class ForcedLineAlphaBeta(Engine):
    def __init__(self, eval_function = None, search_threshold=1):
        self.pref_min_search = 0
        self.pref_max_search = 100000
        self.depth = 3
        self.orig_depth = 3
        # We don't decrement depth whenver there are at most search_treshold moves
        # search_treshold = 1 corresponds to checking forced lines
        self.search_threshold = search_threshold
        self.evaluation_function = eval_function if eval_function is not None else self.default_eval_function

    def default_eval_function(self, board):
        return len(board.legal_moves)

    def get_next_move(self, board):
        counter = [0]
        if len(board.legal_moves) == 1: return (board.legal_moves[0], 0)
        # returns (move, eval) pair
        def recurse(board, maximizing, depth, alpha=float("-inf"), beta=float("inf")):
            # print counter[0]
            counter[0] += 1
            depth = min(self.depth, depth)
            # print (alpha, beta)
            # sort by treewidth
            # legal_moves = board.legal_moves
            legal_moves = sorted(board.legal_moves, key=lambda \
            move: len(board.make_move_from_move(move).legal_moves))

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
                next_depth = depth + 0.1 if len(legal_moves) <= self.search_threshold else depth - 1
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
                next_depth = depth + 0.1 if len(legal_moves) <= self.search_threshold else depth - 1
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
        ret = recurse(board, True, self.depth)
        print "evaluated %d positions" % counter[0]
        if counter[0] < self.pref_min_search:
            self.depth += 1
        if counter[0] > self.pref_max_search:
            self.depth = max(self.orig_depth, self.depth - 1)
        # print self.depth
        return ret
