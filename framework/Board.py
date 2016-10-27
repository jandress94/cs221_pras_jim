from Constants import *
from itertools import product
from PieceUtils import *
from Move import Move
from copy import deepcopy, copy
from random import shuffle

class Board:
    def __init__(self, white="White", black="Black", position=None):
        self.white = white
        self.black = black
        self.position = self.get_starting_position()
        self.turn = 'w'
        self.pieces = self.find_pieces()
        self.ep = None
        self.halfmove_since_capt_pawn = 0
        self.moves = 1
        self.result = None # possible values: 'w', 'b', 'd'

    def __str__(self):
        s = "\n"
        board = self.position
        for row in board:
            for piece in row:
                if piece == None:
                    s +=  " .  "
                else:
                    s +=  " " + piece + "  "
            s +=  '\n\n'
        return s

    def print_board(self):
        print self
        # print "\n"
        # board = self.position
        # for row in board:
        #     for piece in row:
        #         if piece == None:
        #             print " . ",
        #         else:
        #             print unicode_pieces[piece] + " ",
        #     print '\n'



    def get_piece(self, row, col):
        return self.position[row][col]

    def set_piece(self, row, col, piece):
        self.position[row][col] = piece


    def find_pieces(self):
        pieces = {
            piece:[] for piece in (chess_pieces['w'] | chess_pieces['b'])
        }
        position = self.position
        # iterate through board and populate pieces
        for (row, col) in product(xrange(len(position)), xrange(len(position))):
            piece = self.get_piece(row, col)
            if piece != None: (pieces[piece]).append((row, col))
        return pieces



    def get_starting_position(self):
        return [
            ['R', 'N', 'B', 'K', 'Q', 'B', 'N', 'R'],
            ['P']*8,
            [None]*8,
            [None]*8,
            [None]*8,
            [None]*8,
            ['p']*8,
            ['r', 'n', 'b', 'k', 'q', 'b', 'n', 'r'],
        ]

    def pieces(self, player):
        return chess_pieces[player]

    # better version of under attack
    # iterates trough some under_attack_by_X()
    def under_attack(self, pos, perspective):
        check_fns = [under_attack_by_pawn, under_attack_by_king,
                    under_attack_by_knight, under_attack_by_bishop,
                    under_attack_by_rook, under_attack_by_queen]
        old_turn = self.turn
        self.turn = perspective
        for check_fn in check_fns:
            attacking_piece = check_fn(self, pos)
            if attacking_piece != None:
                self.turn = old_turn
                return attacking_piece
        self.turn = old_turn
        return None


    # checks if a square is "under attack" from the perspective of some player
    # def under_attack(self, pos, perspective):
    #     board_cpy = deepcopy(self)
    #     # pretend it's the opponent's turn
    #     board_cpy.turn = opponent[perspective]
    #     # we can pretend that castling isn't allowed because it's irrelvant to
    #     # checking if a square is under attack
    #     board_cpy.castling = {
    #         'w': [False, False],
    #         'b': [False, False]
    #     }
    #     moves = board_cpy.get_legal_moves_help()
    #     for move in moves:
    #         if (move.end == pos) and (move.placing_piece == None):
    #             return True
    #     return False


    # checks if the player is in check

    def exists_capture(self, moves):
        for move in moves:
            if move.capture: return True
        return False

    def get_legal_moves(self):
        moves_to_return = []
        position = self.position
        moves = []
        for (row, col) in product(xrange(len(position)), xrange(len(position))):
            if position[row][col] != None and is_mine(self, position[row][col]):
                moves += get_legal_moves_for_piece(self, (row, col))
        if self.exists_capture(moves):
            return [move for move in moves if move.capture]
        return moves



    def print_legal_moves(self):
        print [move.move_to_str() for move in self.get_legal_moves()]

    # takes a string "e2e4" and returns the move
    # Move((2, 4), (4, 4))
    # figures out if it's a promotion, a castle, or some madness like that
    # possible types of moves:
    #   -> normal translation, capture, or castle. encoded "e2e4"
    #       for this sort of encoding, this function figures out which of
    #       the above types is correct
    #   -> promotion: encoded "e7e8, Q" for white, or "e2e1, q" for black
    # assumes that move strings are correctly formatted
    def get_move(self, move_str):

        def str_to_square(str):
            return (int(str[1]) - 1, 7 - ord(str[0]) + ord('a'))

        if ',' in move_str: # promotion case
            start_str = move_str[:2]
            end_str = move_str[2:4]
            start = str_to_square(start_str)
            end = str_to_square(end_str)

            return Move(start, end, move_str[len(move_str) - 1])

        else:
            start_str = move_str[:2]
            end_str = move_str[2:]
            start = str_to_square(start_str)
            end = str_to_square(end_str)

        return Move(start, end, capture=(self.get_piece(end[0], end[1]) != None))


    def has_pieces(self, player):
        for (row, col) in product(xrange(len(self.position)), xrange(len(self.position))):
            piece = self.get_piece(row, col)
            if piece != None and ((player == 'w') == (piece[0]).isupper()):
                print piece
                return True
        return False


    def result_checks(self):
        if len(self.get_legal_moves()) == 0:
            if not self.has_pieces(self.turn): # out of pieces!!
                return opponent[self.turn]
            else: # Stalemate!!
                return 'd'
        if self.halfmove_since_capt_pawn >= 50:
            return 'd'
        return None

    # makes move given an instance of Move (rather than a string)
    def make_move_from_move(self, move):

        def switch_sides(piece, player):
            return piece.upper() if player == 'w' else piece.lower()


        # need to adjust the parameters of the board
        board_cpy = deepcopy(self)

        # list of possible moves and what parameters need to be changed for each
        # ***** REMEMBER: we need to see if any given move results in a check ******
        # the possible moves are as follows:
        # 1. moving a piece from one spot to an empty spot that's not the ep target
        #   -> essentially constitutes changing the position of a piece
        # 2. taking a piece
        #   -> change position of taking piece
        #   -> add taken piece to board.turn's in_hand
        #   -> note: castling rights can change here
        # 3. en passant
        #   -> change position of taking pawn
        #   -> remove pawn
        #   -> add pawn to board.turn's in_hand
        # 4. promoting piece
        #   -> putting piece on square
        #

        if move.start != None: moving_piece = board_cpy.get_piece(move.start[0], move.start[1])
        taken_piece = board_cpy.get_piece(move.end[0], move.end[1])

        # conditions for (1) or (2): move or take
        if (move.end != board_cpy.ep) and move.promoting_piece == None:
            # change board
            # TODO update piece locations
            board_cpy.set_piece(move.start[0], move.start[1], None)
            board_cpy.set_piece(move.end[0], move.end[1], moving_piece)

            # if a piece is taken or pawn is advanced, we need to restart halfmove count
            if taken_piece != None or moving_piece == 'p' or moving_piece == 'P':
                board_cpy.halfmove_since_capt_pawn = 0


        #  condition (3): ep
        elif (move.end == board_cpy.ep) and (moving_piece == 'p' or moving_piece == 'P'):
            # change board
            board_cpy.set_piece(move.start[0], move.start[1], None)
            board_cpy.set_piece(move.end[0], move.end[1], moving_piece)
            board_cpy.set_piece(move.end[0] - (1 if board_cpy.turn == 'w' else -1), move.end[1], None)
            board_cpy.in_hand[board_cpy.turn]['P' if board_cpy.turn == 'w' else 'p'] += 1

        # condition (4): promotion
        elif move.promoting_piece != None:
            board_cpy.set_piece(move.start[0], move.start[1], None)
            board_cpy.set_piece(move.end[0], move.end[1], move.promoting_piece + '*')
            if taken_piece != None:
                if len(taken_piece) == 1:
                    board_cpy.in_hand[board_cpy.turn][switch_sides(taken_piece, board_cpy.turn)] += 1
                else: # capturing a piece that was promoted
                    board_cpy.in_hand[board_cpy.turn]['P' if board_cpy.turn == 'w' else 'p'] += 1

            board_cpy.halfmove_since_capt_pawn = 0


        # final adjustments
        board_cpy.turn = opponent[board_cpy.turn]
        if board_cpy.turn == 'w': board_cpy.moves += 1

        if board_cpy.halfmove_since_capt_pawn !=  0: # means no capture or pawn advance
            board_cpy.halfmove_since_capt_pawn += 1

        board_cpy.result = board_cpy.result_checks()


        return board_cpy


    # moves are made like: e2e4, e2e3
    # returns "ILLEGAL_MOVE" if illegal
    def make_move(self, move_str):
        move = self.get_move(move_str)
        if not (move.params in [poss.params for poss in self.get_legal_moves()]):
            return "ILLEGAL_MOVE"
        return self.make_move_from_move(move)

    # conversion from algebraic notation to start-end notation
    # takes in string
    def algebraic_to_se(self, alg):

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
            moves = self.get_legal_moves()

            # checks are in this order:
            #   1. end point is correct
            poss_moves = [move for move in moves if (move.end == end and \
            (self.get_piece(move.start[0], move.start[1]).upper() == norm_alg[0] or\
            (self.get_piece(move.start[0], move.start[1]).upper() ==  'P' and \
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


    def get_result(self):
        return self.result
