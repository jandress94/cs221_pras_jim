
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


    # def se_to_algebraic(self, board):
    #
    #     def pos_to_str(pos):
    #         return chr(7 - pos[1] + ord('a')) + str(pos[0] + 1)
    #
    #
    #     if promoting_piece == None and not capture:
    #         moving_piece = board.get_piece(self.start[0], self.start[1])
    #         # pawn move
    #         if moving_piece.lower() == 'p':
    #             return pos_to_str(self.end)
    #         else:
    #             return moving_piece.upper + pos_to_str(self.end)
    #
    #     if capture:
    #         moving_piece = board.get_piece(self.start[0], self.start[1])
    #         # pawn capture
    #         if moving_piece.lower() == 'p':
    #             return pos_to_str(self.end) + 'x' + pos_to_str(self.end)
    #         else:
    #             return moving_piece.upper + 'x' + pos_to_str(self.end)




    # # conversion from algebraic notation to start-end notation
    # # takes in string
    # def algebraic_to_se(board, alg):
    #     # possible cases:
    #     # 1. Be5
    #     #   -> no capture, just movement
    #     # 2. e5
    #     #   -> pawn move
    #     # 3. Bxe5
    #     #   -> capture
    #     # 4. exe5
    #     #   -> pawn capture
    #     # 5. exd6e.p.
    #     #   -> en passant




    # def __init__(self, start_row, start_col, end_row, end_col, board):
    #     self.start_row = start_row
    #     self.start_col = start_col
    #     self.end_row = end_row
    #     self.end_col = end_col
    #     self.board = board
    #     self.player = board.turn
    #     self.is_ep =  ((self.board).ep == (end_row, end_col))
    #     self.captured = self.captured_piece()
    #     self.is_capture = (self.captured != None)

    # def captured_piece(self):
    #     # general case
    #     end_piece = (self.board).position[self.end_row][self.end_col]
    #     if end_piece in chess_pieces[opponent[(self.board).turn]]:
    #         return end_piece

        # en passant case -_-
        # if self.is_ep:
        #     return 'P' if self.player == 'w' else 'p'
        #
        # return None
