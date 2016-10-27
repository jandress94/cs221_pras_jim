from random import choice

class Human:
    def __init__(self):
        pass

    def get_best_move(self, board):
        move = "ILLEGAL_MOVE"
        while move == "ILLEGAL_MOVE":
            move_str = raw_input("Play a move: ")
            move = board.get_move(move_str)
            board.print_legal_moves()
            if move.params not in [poss.params for poss in board.get_legal_moves()]:
                move = "ILLEGAL_MOVE"
        return move, 0

        # move_map = {move.move_to_str(): move for move in board.get_legal_moves()}
        # move = "ILLEGAL_MOVE"
        # while move == "ILLEGAL_MOVE":
        #     move_str = raw_input("Play a move: ")
        #     if move_str in move_map:
        #         return move_map[move_str]
