from random import choice
from Engine import Engine
import pdb

class Human(Engine):
    def __init__(self):
        pass

    def get_next_move(self, board):
        move = "ILLEGAL_MOVE"
        while move == "ILLEGAL_MOVE":
            move_str = raw_input("Play a move: ")
            if len(move_str) == 0:
                return board.legal_moves[0], 0
            try:
                move = board.get_move(move_str)
            except IndexError:
                print "Invalid input, here are your choices: "
                board.print_legal_moves()
                continue

            # board.print_legal_moves()
            if str(move) not in [str(poss) for poss in board.legal_moves]:
                move = "ILLEGAL_MOVE"
                print "Invalid input, here are your choices: "
                board.print_legal_moves()
        return move, 0

        # move_map = {move.move_to_str(): move for move in board.get_legal_moves()}
        # move = "ILLEGAL_MOVE"
        # while move == "ILLEGAL_MOVE":
        #     move_str = raw_input("Play a move: ")
        #     if move_str in move_map:
        #         return move_map[move_str]
