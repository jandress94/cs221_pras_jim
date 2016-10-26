from random import choice

class Random:
    def __init__(self):
        pass

    def get_best_move(self, board):
        return choice(board.get_legal_moves()), 0
