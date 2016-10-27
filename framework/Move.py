from PieceUtils import *

class Move:
    # a4a5 = (self, 0, 3, 0, 4, board)
    def __init__(self, start, end, promoting_piece=None, capture=False):
        self.start = start
        self.end = end
        self.promoting_piece = promoting_piece
        self.capture = capture
        # for the purpose of checking if move_a == move_b
        self.params = [self.start, self.end, self.promoting_piece, self.capture]

    def __str__(self):
        return self.move_to_str()

    def move_to_str(self):

        def pos_to_str(pos):
            return chr(7 - pos[1] + ord('a')) + str(pos[0] + 1)

        if self.promoting_piece == None:
            return pos_to_str(self.start) + pos_to_str(self.end)

        if self.promoting_piece != None:
            return pos_to_str(self.start) + pos_to_str(self.end) + ", " + self.promoting_piece

        else:
            return self.placing_piece + "@" + pos_to_str(self.end)


    def se_to_algebraic(self, board):

        def pos_to_str(pos):
            return chr(7 - pos[1] + ord('a')) + str(pos[0] + 1)


        if promoting_piece == None and not capture:
            moving_piece = board.get_piece(self.start[0], self.start[1])
            # pawn move
            if moving_piece.lower() == 'p':
                return pos_to_str(self.end)
            else:
                return moving_piece.upper + pos_to_str(self.end)

        if capture:
            moving_piece = board.get_piece(self.start[0], self.start[1])
            # pawn capture
            if moving_piece.lower() == 'p':
                return pos_to_str(self.end) + 'x' + pos_to_str(self.end)
            else:
                return moving_piece.upper + 'x' + pos_to_str(self.end)



# conversion from algebraic notation to start-end notation
# takes in string
def algebraic_to_se(board, alg):

    def str_to_square(str):
        return (int(str[1]) - 1, 7 - ord(str[0]) + ord('a'))

    def pos_to_str(pos):
        return chr(7 - pos[1] + ord('a')) + str(pos[0] + 1)

    # possible cases:
    # 1. Be5
    #   -> no capture, just movement
    # 2. Rfe5
    #   -> two possible pieces, specified by column
    # 3. R5f6
    #   -> two possible pieces, specified by row
    # 3. Bxe5
    #   -> capture
    # 2. e5
    #   -> pawn move
    # 4. exf5
    #   -> pawn capture
    # 5. f8=Q DONE
    #   -> promotion

    capt = ('x' in alg)
    prom = None
    # remove capture part of the move
    norm_alg = alg if (not capt) else ''.join(alg.split('x'))

    # promotion case (5)
    if '=' in norm_alg:
        start_str = norm_alg[0] + ('7' if norm_alg[-3] == 'w' else '2')
        end_str = norm_alg[-4:-2]
        prom = norm_alg[-1].upper() if '8' == end_str[-1] else norm_alg[-1].lower()
    else:
        end_str = norm_alg[-2:]
        end = str_to_square(end_str)
        moves = board.get_legal_moves()

        # checks are in this order:
        #   1. end point is correct
        poss_moves = [move for move in moves if (move.end == end and \
        (board.get_piece(move.start[0], move.start[1]).upper() == norm_alg[0] or\
        (board.get_piece(move.start[0], move.start[1]).upper() ==  'P' and \
        norm_alg[0].islower())))]
        if len(poss_moves) == 0: print "MAYDAY MAYDAY ABORT ABORT"
        if len(poss_moves) == 1: return poss_moves[0]
        for move in moves:
            start_str = pos_to_str(move.start)
            # check if column matches or row matches
            if start_str[0] == norm_move[1] or start_str[1] == norm_move[1]:
                return move
        start, end = str_to_square(start_str), str_to_square(end_str)
        return Move(start, end, prom, capt)
