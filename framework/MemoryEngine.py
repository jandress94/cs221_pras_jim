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

# components of a game tree
class SearchNode:
    def __init__(self, board, successors={}, parent=None, index=-1, \
     eval=0, best_move=None, is_leaf=True):
        # board in the game tree
        self.board = board
        # possible nodes that can be reached via a move on self.board
        self.successors = successors
        # the parent node; needed so that we can update evals accordingly
        # the current board will always become the "root", and then it will
        # have no parent (well, we'll get rid of it)
        self.parent = parent
        # index of this node in the parent's sucessor array (for cutoffs)
        self.index = index
        # cutoffs
        # self.alpha = alpha
        # self.beta = beta
        # optimal stuff data
        self.eval_estimate = 0
        self.best_move = None
        self.is_leaf = is_leaf
        # self.maxi_node = maxi

class MemoryEngine(Engine):
    def __init__(self, eval_function=None, search_threshold=1):
        # self.pref_min_search = 1000
        # self.pref_max_search = 10000
        self.depth = 3
        self.current_node = SearchNode(Board())
        self.leaves = [self.current_node]
        # self.orig_depth = 3
        # We don't decrement depth whenver there are at most search_treshold moves
        # search_treshold = 1 corresponds to checking forced lines
        self.search_threshold = search_threshold
        self.evaluation_function = eval_function if eval_function is not None else self.default_eval_function


    # def make_node(self, board):
    #
    # def get_next_move(self, board):
    #     old_node = self.current_node
    #     children = self.sucessors
    #     for child in children:
    #         if str(child.board) == str(board):
    #             self.current_node =

    # def extend(self):
    #     new_leaves = []
    #     for leaf in leaves:
    #         succ_boards = [leaf.board.make_move_from_move(move) for move in leaf.board.legal_moves]
    #         succ_nodes = [SearchNode(board, not leaf.maxi_node) for board in succ_boards]
    #         # leaf.successors = succ_nodes
    #         for node in succ_nodes:
    #             node.eval_estimate = self.evaluation_function(node.board)
    #         # leaf.sucessors = [node in succ_nodes if ]
    #         leaf.successors = succ_nodes

    def update_current_node(self, board):
        if str(board) == str(self.current_node.board): return
        for succ in self.current_node.successors:
            if str(succ.board) == str(board):
                self.current_node = succ
                return

    def make_successors(self, leaf):
        # print "HERE"
        # print leaf.board
        succ_nodes = {SearchNode(leaf.board.make_move_from_move(move)):move for move in leaf.board.legal_moves}
        # succ_nodes = [SearchNode(board) for board in succ_boards]
        # leaf.successors = succ_nodes
        for node in succ_nodes:
            node.eval_estimate = self.evaluation_function(node.board)
            # leaf.sucessors = [node in succ_nodes if ]
        leaf.successors = succ_nodes


    def default_eval_function(self, board):
        return len(board.legal_moves)

    def get_next_move(self, board):
        counter = [0]
        # if len(board.legal_moves) == 1: return (board.legal_moves[0], 0)
        # returns (move, eval) pair
        def recurse(node, maximizing, depth, alpha=float("-inf"), beta=float("inf")):
            print counter[0]
            # print node.board
            counter[0] += 1
            depth = min(self.depth, depth)

            if node.is_leaf:
                self.make_successors(node)
                node.is_leaf = False

            # print (alpha, beta)
            # sort by treewidth
            # succs = sorted(node.successors, key=lambda succ: len(succ.successors))
            succs = [succ for succ in node.successors]

            # legal_moves = sorted(board.legal_moves, key=lambda \
            # move: len(board.make_move_from_move(move).legal_moves))

            if node.board.get_result() != None or len(succs) == 0 or depth <= 0:
                evaluation = node.eval_estimate
                if node.board.get_result() != None:
                    if node.board.get_result() == node.board.turn:
                        evaluation = float('inf')
                    elif node.board.get_result() == 'd':
                        evaluation = 0
                    elif node.board.get_result() != board.turn:
                        evaluation = float('-inf')
                return (None, evaluation)

            # next_depth = depth - 1
            # next_carryover = False
            # if len(legal_moves) <= self.search_threshold and not carryover:
            #     next_depth = depth + 1
            #     next_carryover = len(legal_moves) <= self.search_threshold

            if maximizing:
                # next_depth = depth if len(legal_moves) <= self.search_threshold else depth - 1
                next_depth = depth + 1 if len(succs) <= self.search_threshold else depth - 1
                highest_eval = float("-inf")
                opt_move = None
                for succ in succs:
                    # succ = board.make_move_from_move(move)
                    highest_eval = max(highest_eval, \
                    recurse(succ, not maximizing, depth - 1, alpha, beta)[1])
                    if highest_eval > alpha:
                        alpha = highest_eval
                        opt_move = node.successors[succ]
                    # cutoff
                    if beta <= alpha:
                        break
                return (opt_move, highest_eval)
            else:
                # next_depth = depth + 1 if len(legal_moves) <= self.search_threshold and not carryover else depth - 1
                lowest_eval  = float("inf")
                opt_move = None
                next_depth = depth + 1 if len(succs) <= self.search_threshold else depth - 1
                for succ in succs:
                    # succ = board.make_move_from_move(move)
                    lowest_eval = min(lowest_eval, \
                    recurse(succ, not maximizing, next_depth, alpha, beta)[1])
                    if lowest_eval < beta:
                        beta = lowest_eval
                        opt_move = node.successors[succ]
                    # cutoff
                    if beta <= alpha:
                        break
                return (opt_move, lowest_eval)

        self.update_current_node(board)
        if len(board.legal_moves) == 1:
            mv, ev = (board.legal_moves[0], 0)
        else:
            mv, ev = recurse(self.current_node, True, self.depth)
        self.update_current_node(self.current_node.make_move_from_move(mv))
        print "evaluation count: ", counter[0]
        return (mv, ev)


        ret = recurse(board, True, self.depth)
        # print "evaluation: ", counter[0]
        if counter[0] < self.pref_min_search:
            self.depth += 1
        if counter[0] > self.pref_max_search:
            self.depth = max(self.orig_depth, self.depth - 1)
        print self.depth
        return ret
