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
        pass
        # INCOMPLETEEEEEE
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
