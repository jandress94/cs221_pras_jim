from Board import *
from collections import defaultdict

# modifies d1 so that it is d1 + m*d2
def addScaled(d1, d2, m):
    for key in d2:
        d1[key] += m * d2[key]

def dotProduct(d1, d2):
    if len(d1) < len(d2):
        return dotProduct(d2, d1)
    else:
        return sum(d1.get(f, 0) * v for f, v in d2.items())

def eval(board, weights, turn):
    mult = 1 if turn == 'w' else -1
    return mult * dotProduct(weights, feature_extractor(board))

# helpers for the evaluaton function

def get_player_features(board, turn):
    # TODO add more features
    features = defaultdict(float)
    features[turn + ' mobility'] = mobility(board, turn)
    pieces = piece_features(board, turn)
    for piece in pieces:
        features[turn + ' pieces ' + piece] = pieces[piece]
    return features

def feature_extractor(board):
    white_features = get_player_features(board, 'w')
    black_features = get_player_features(board, 'b')
    addScaled(white_features, black_features, 1)
    return white_features

def mobility(board, turn):
    real_turn = board.turn
    board.turn = turn
    result = len(board.get_legal_moves())
    board.turn = real_turn
    return result

def piece_features(board, turn):
    pieces = defaultdict(float)
    # mult = 1 if turn == 'w' else -1
    position = board.position
    for (row, col) in product(xrange(len(position)), xrange(len(position))):
        piece  = position[row][col]
        if piece != None and (piece.islower() == (turn == 'b')):
            piece = piece[0]
            pieces[piece.lower()] += 1
    return pieces