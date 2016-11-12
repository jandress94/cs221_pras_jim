from random import choice
from Engine import Engine

class Random(Engine):
    def __init__(self):
        pass

    def get_next_move(self, board):
        return choice(board.get_legal_moves()), 0
