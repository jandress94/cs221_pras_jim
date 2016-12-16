from Engine import Engine
from Board import *
from AlphaBetaEngine import AlphaBeta
import random

# Notes and optimizations:
# -> currently creates every board from scratch, which is expensive.
#   would be better to keep track of some sort of game tree, and expand when needed
# -> uses simple eval function, should eventually use Features.py for eval function
# -> simple eval function beats Random() every time, perhaps can serve as an improved baseline.
# -> AlphaBeta has a hard time moving first because of all the possibilities. It might be useful
#   to keep a small opening book (like a few moves which are known not to be totally losing)
#   and playing one of those at random.

class EpsGreedyAlphaBeta(Engine):
    def __init__(self, alpha_beta=None, eval_function=None, eps = 0.1):
        self.epsilon = eps
        self.alpha_beta = alpha_beta if alpha_beta != None else AlphaBeta(eval_function)

    def get_next_move(self, board):
        if random.random() < self.epsilon:
            return random.choice(board.legal_moves), 0
        else:
            return self.alpha_beta.get_next_move(board)
