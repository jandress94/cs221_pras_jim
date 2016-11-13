from Board import *
from collections import defaultdict


# helpers for the evaluaton function


def feature_extractor(board):
    # TODO add more features
    features = defaultdict(float)
    features['mobility'] = mobility(board)
    adv = material_advantage(board)
    for piece in adv:
        features['mat adv ' + piece] = adv[piece]
    features['win'] = is_win(board)
    return features

def mobility(board):
    return len(board.get_legal_moves())

def material_advantage(board):
    advantages = defaultdict(float)
    mult = 1 if board.turn == 'w' else -1
    position = board.position
    for (row, col) in product(xrange(len(position)), xrange(len(position))):
        piece  = position[row][col]
        if piece != None:
            piece = piece[0]
            advantages[piece.lower()] += (mult if piece.islower() else -1*mult )
    return advantages

def is_win(board):
    if board.result == board.turn:
        return 1
    if board.result == opponent[board.turn]:
        return -1
    return 0
