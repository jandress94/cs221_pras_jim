chess_pieces = {
    'w': {'K', 'Q', 'R', 'B', 'N', 'P'},
    'b': {'k', 'q', 'r', 'b', 'n', 'p'}
}

# promoted pieces are marked, because they are converted
# to pawns when captured
promotion_pieces = {
    'w': {'Q*', 'R*', 'B*', 'N*'},
    'b': {'q*', 'r*', 'b*', 'n*'}
}

opponent = {
    'w': 'b',
    'b': 'w'
}

unicode_pieces = {
    'K': u"\u2654",
    'Q': u"\u2655",
    'R': u"\u2656",
    'B': u"\u2657",
    'N': u"\u2658",
    'P': u"\u2659",
    'k': u"\u265A",
    'q': u"\u265B",
    'r': u"\u265C",
    'b': u"\u265D",
    'n': u"\u265E",
    'p': u"\u265F"
}

piece_values = {
    'K': 0,
    'Q': 9,
    'R': 5,
    'B': 3,
    'N': 3,
    'P': 1,
    'k': 0,
    'q': 9,
    'r': 5,
    'b': 3,
    'n': 3,
    'p': 1
}
