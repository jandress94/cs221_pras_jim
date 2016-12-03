from Board import Board
from HumanEngine import Human
from Features import feature_extractor

class GamePlayer:
    def __init__(self, white_engine=Human(), black_engine=Human(), log=True):
        self.white_engine = white_engine
        self.black_engine = black_engine
        self.board = Board()
        self.log = log

    def set_engine(self, color, engine):
        if color == 'w':
            self.white_engine = engine
        elif color == 'b':
            self.black_engine = engine

    def print_log(self, s):
        if self.log:
            print s

    def print_result(self):
        if not self.log: return
        
        board = self.board
        # winner
        if board.result == 'd':
            print "DRAWN GAME"
        else:
            print "WINNER: ", (board.white if board.result == 'w' else board.black)
        print "Number of moves: ", board.moves


    def print_move_information(self, move):
        if self.log:
            player = "White" if self.board.turn == 'w' else "Black"
            print "Move: ", self.board.moves
            print player, "played the move ", str(move)

    def play_game(self):
        self.print_log(self.board)
        while self.board.result == None:
            if self.board.turn == 'w':
                move, ev = self.white_engine.get_next_move(self.board)
            else:
                move, ev = self.black_engine.get_next_move(self.board)
            self.print_move_information(move)
            self.board = self.board.make_move_from_move(move)
            self.print_log(self.board)
        self.print_result()
