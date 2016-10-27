from Board import Board

# takes a game list and produces a nice list of positions, moves, and a dictionary
# mapping positions to the moves chosen at those positions.
class GameProcessor:
    def __init__(self, game):
        # algebraic representation of a game
        self.alg_game = game
        # list of positions
        self.positions = []
        # list of moves
        self.moves = []
        # dictionary from positions to moves (may become unnecessary)
        self.pmdict = []

    def get_positions(self):
        return self.positions

    def get_moves(self):
        return self.moves

    def simulate_game(self):
        board = Board()
        moves = [move for pair in self.alg_game for move in pair if move != None]
        (self.positions).append(board)
        for move in moves:
            curr_move = board.algebraic_to_se(move)
            (self.moves).append(curr_move)
            board = board.make_move_from_move(curr_move)
            (self.positions).append(board)
        self.pmdict = {self.positions[i]:self.moves[i] for i in range(len(moves))}
