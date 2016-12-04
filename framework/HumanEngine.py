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
            try:
                move = board.get_move(move_str)
            except IndexError:
                print "Invalid input, here are your choices: "
                board.print_legal_moves()
                continue

            # board.print_legal_moves()
            if move.params not in [poss.params for poss in board.get_legal_moves()]:
                move = "ILLEGAL_MOVE"
        return move, 0

        # move_map = {move.move_to_str(): move for move in board.get_legal_moves()}
        # move = "ILLEGAL_MOVE"
        # while move == "ILLEGAL_MOVE":
        #     move_str = raw_input("Play a move: ")
        #     if move_str in move_map:
        #         return move_map[move_str]
