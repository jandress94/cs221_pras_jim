from Board import *
from collections import defaultdict
import math

# modifies d1 so that it is d1 + m*d2
def addScaled(d1, d2, m):
    for key in d2:
        d1[key] += m * d2[key]

def dotProduct(d1, d2):
    if len(d1) < len(d2):
        return dotProduct(d2, d1)
    else:
        return sum(d1.get(f, 0) * v for f, v in d2.items())

def learning_eval(board, weights, turn):
    return dotProduct(weights, feature_extractor(board, turn))

def eval(board, weights, turn):
    # print "DOING NORMAL EVALLLL"
    # if board.result != None:
    #     if board.result == turn: return float('inf')
    #     if board.result == 'd': return 0
    #     if board.result != turn: return float('-inf')
    return dotProduct(weights, feature_extractor(board, turn))

# def other_eval(board, weights, turn):
#     # print "DOING OTHER EVALLLLLLL"
#     mult = 1 if turn == 'w' else -1
#     # print "OTHER FEATURES:", other_feature_extractor(board)
#     return mult * dotProduct(weights, other_feature_extractor(board))

# helpers for the evaluaton function

def get_player_features(board, side, turn):
    # TODO add more features
    whoseFeatures = 'my' if side == turn else 'opponent'

    features = defaultdict(float)
    features[whoseFeatures + ' mobility'] = mobility(board, side)
    pieces = piece_features(board, side)
    for piece in pieces:
        features[whoseFeatures + ' pieces ' + piece] = pieces[piece]
    return features

def feature_extractor(board, turn):
    white_features = get_player_features(board, 'w', turn)
    black_features = get_player_features(board, 'b', turn)
    addScaled(white_features, black_features, 1)
    return white_features

# def get_player_features_wcenter(board, turn):
#     # TODO add more features
#     features = defaultdict(float)
#     features[turn + ' mobility'] = mobility(board, turn)
#     centers, pieces = center_and_pieces(board, turn)
#     for piece in pieces:
#         features[turn + ' pieces ' + piece] = pieces[piece]
#         features[turn + ' center ' + piece] = centers[piece]
#     return features
#
#
# def other_feature_extractor(board):
#     white_features = get_player_features_wcenter(board, 'w')
#     black_features = get_player_features_wcenter(board, 'b')
#     addScaled(white_features, black_features, 1)
#     return white_features

# def man_dist(p1, p2 ):
#   "Returns the Manhattan distance between points xy1 and xy2"
#   return abs( p1[0] - p2[0] ) + abs( p1[1] - p2[1] )
#
# def center_and_pieces(board, turn):
#     position = board.position
#     center = (3.5, 3.5)
#     pieces = defaultdict(float)
#     centers = defaultdict(float)
#     for (row, col) in product(xrange(len(position)), xrange(len(position))):
#         piece  = position[row][col]
#         if piece != None and (piece.islower() == (turn == 'b')):
#             piece = piece[0]
#             centers[piece.lower()] += man_dist(center, (row, col))
#             pieces[piece.lower()] += 1
#     for piece in centers:
#         centers[piece] = centers[piece]/float(pieces[piece])
#     return centers, pieces



def mobility(board, side):
    real_turn = board.turn
    board.turn = side
    result = len(board.get_legal_moves())
    board.turn = real_turn
    return result

def piece_features(board, side):
    pieces = defaultdict(float)
    # mult = 1 if turn == 'w' else -1
    position = board.position
    for (row, col) in product(xrange(len(position)), xrange(len(position))):
        piece  = position[row][col]
        if piece != None and (piece.islower() == (side == 'b')):
            piece = piece[0]
            pieces[piece.lower()] += 1
    return pieces
