from Features import *
from collections import defaultdict
from game_parser import parseGame
from LichessEngine import Lichess
from Board import Board
from RandomEngine import Random
from os import listdir
from os.path import isfile, join
from GamePlayer import GamePlayer
from AlphaBetaEngine import AlphaBeta
from EpsGreedyAlphaBetaEngine import EpsGreedyAlphaBeta
from HumanEngine import Human
import random

class TDLearner:
    def __init__(self, white_engine=Random(), black_engine=Random(), win = 'w'):
        self.white_engine = white_engine
        self.black_engine = black_engine
        self.board = Board()
        self.eta = 0.001
        self.grad_sum = defaultdict(float)
        self.winner = win
        self.lambd = 0.25

    def set_engine(self, color, engine):
        if color == 'w':
            self.white_engine = engine
        elif color == 'b':
            self.black_engine = engine

    def update_weights(self, start_board, end_board, weights):
        if end_board.result is None: reward = eval(end_board, weights, 'w')
        elif end_board.result == 'w': reward = 1
        else: reward = -1
        # if reward != 0:
        #     print reward

        update_weight = self.eta * (reward - eval(start_board, weights, 'w'))

        grad_value = feature_extractor(start_board)
        addScaled(grad_value, self.grad_sum, self.lambd)
        self.grad_sum = grad_value
        addScaled(weights, self.grad_sum, update_weight)

        # grad_value = feature_extractor(start_board)
        # for key in grad_value:

        #     # self.grad_sum[key] += grad_value[key]
        #     # weights[key] -= update_weight * self.grad_sum[key]
        #     weights[key] += update_weight * grad_value[key]
        return weights

    def learn_from_game(self, weights):
        while self.board.result == None:
            # make a move
            turn = self.board.turn
            if turn == 'w':
                move, ev = self.white_engine.get_next_move(self.board)
            else:
                move, ev = self.black_engine.get_next_move(self.board)
            next_board = self.board.make_move_from_move(move)

            # update weights
            if turn == self.winner:
                weights = self.update_weights(self.board, next_board, weights)

            self.board = next_board
        weights = self.update_weights(self.board, next_board, weights)
        print weights
        return weights


weights = defaultdict(float)
weights['w mobility'] = 0.1

data_folder = '../scraper/data/'
f = listdir(data_folder)[1]
file_reader = open(join(data_folder, f), 'r')
lineNum = 0
for line in file_reader:
    line = line.strip()
    if lineNum % 2 == 0:
        print 'Learning from game', line
    else:
        game_data = parseGame(line)
        if game_data is not None:

            game = GamePlayer(white_engine=Lichess(game_data, 'w'), black_engine=Lichess(game_data, 'b'), log = False)
            game.play_game()

            # winner = 'b' if game_data[len(game_data) - 1][1] == None else 'w'
            tdLearner = TDLearner(white_engine=Lichess(game_data, 'w'), black_engine=Lichess(game_data, 'b'), win = game.board.result)
            weights = tdLearner.learn_from_game(weights)
            print
    lineNum += 1
print weights
file_reader.close()

game = GamePlayer(white_engine=AlphaBeta(), black_engine=AlphaBeta(eval_function = lambda board : eval(board, weights, 'b')))
game.play_game()