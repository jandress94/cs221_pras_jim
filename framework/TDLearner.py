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
from DynamicDepthAlphaBetaEngine import DynamicDepthAlphaBeta
from EpsGreedyAlphaBetaEngine import EpsGreedyAlphaBeta
from ForcedLineAlphaBetaEngine import ForcedLineAlphaBeta
from HumanEngine import Human
import random

class TDLearnerGame:
    # I'm not entirely sure what win is, or why it's important, help?
    # I know that this is a lot of parameters. If some of them aren't necessary,
    # we should make life easier
    def __init__(self, white_engine=Random(), black_engine=Random(), win = 'w',\
    feature_extractor=feature_extractor, eval_fn=eval, eta=0.001, log=False):
        self.white_engine = white_engine
        self.black_engine = black_engine
        self.board = Board()
        self.eta = eta
        self.grad_sum = defaultdict(float)
        self.lambd = 0.7
        self.winner = win
        self.extractor = feature_extractor
        self.eval_fn = eval_fn
        self.log = log

    def set_engine(self, color, engine):
        if color == 'w':
            self.white_engine = engine
        elif color == 'b':
            self.black_engine = engine

    def update_weights(self, start_board, end_board, weights, turn):
        if end_board.result is None:
            reward = self.eval_fn(end_board, weights, turn)
        elif end_board.result == turn: reward = 1
        else: reward = -1

        update_weight = self.eta * (reward - self.eval_fn(start_board, weights, turn))
        grad_value = self.extractor(start_board, turn)

        addScaled(grad_value, self.grad_sum, self.lambd)
        self.grad_sum = grad_value

        addScaled(weights, self.grad_sum, update_weight)

        return weights

    def learn_from_game(self, weights):
        oldBoard = None
        while self.board.result == None:
            # make a move
            turn = self.board.turn

            if turn == self.winner:
                if oldBoard != None:
                    weights = self.update_weights(oldBoard, self.board, weights, turn)
                oldBoard = self.board


            if turn == 'w':
                move, ev = self.white_engine.get_next_move(self.board)
            else:
                move, ev = self.black_engine.get_next_move(self.board)
            next_board = self.board.make_move_from_move(move)

            # update weights
            # if turn == self.winner:
            #     weights = self.update_weights(self.board, next_board, weights, turn)

            self.board = next_board
        weights = self.update_weights(oldBoard, self.board, weights, self.winner)
        if self.log: print weights
        return weights

class TDLearnerData:
    # eval_fn should take in a board, weights, and a turn
    # there are a lot of parameters, but each one is something that we might want to have
    # control over abstractly, so I think it's justified
    def __init__(self, turn, feature_extractor, eval_fn, data_folder, eta=0.001, log=False):
        self.turn = turn
        self.extractor = feature_extractor
        self.data_folder = data_folder
        self.log = log
        self.eval_fn = eval_fn
        self.eta = eta



    def get_weights(self):

        # i think multiplying by a constant shouldn't be a problem
        # as long as that constant is positive
        # def normalize(d):
        #     total = sum([abs(x) for x in dict(d).values()])
        #     for key in d:
        #         d[key] /= total

        weights ={'my pieces b': -0.020884877164403185, 'opponent pieces q': 0.0027937649315177247, 'opponent pieces p': 0.08656753045185818, 'opponent pieces r': 0.03167985225714283, 'my pieces k': -0.0034953612874587697, 'my pieces r': -0.01436313443653616, 'my pieces n': -0.019945511993351116, 'my pieces p': -0.041124848373068006, 'my pieces q': -0.015330339027318493, 'my mobility': -0.0043991206349213875, 'opponent pieces b': 0.01474448329758195,\
         'opponent pieces n': 0.029737402031847958, 'my mobility sqrt': 0.07165475201315358, 'opponent pieces k': 0.026506066354947826}
        # # weights = {'my pieces b': -0.020805240865742317, 'opponent mobility': 0.006038924232797547, \
        # #     'opponent pieces q': 0.0031809482535582563, 'opponent pieces p': 0.08542855701037787, \
        # #     'opponent pieces r': 0.03130194131137462, 'my pieces k': -0.004348334410101487, \
        # #     'my pieces r': -0.012264248129115054, 'my pieces n': -0.021129062238778695, \
        # #     'my pieces p': -0.04592605265576196, 'my pieces q': -0.016223203304076266, \
        # #     'my mobility': 0.005539364980023288, 'opponent pieces b': 0.014757655681540789, \
        # #     'opponent pieces n': 0.030392414884365324, 'opponent pieces k': 0.026302758142338463}
        return weights
        weights = defaultdict(float)
        # return weights

        # data_folder = '../scraper/data/'
        f = listdir(self.data_folder)[1]
        file_reader = open(join(self.data_folder, f), 'r')
        print "I'm learning some weights for %s from %s!" % \
        ("white" if self.turn == 'w' else "black", self.data_folder)
        lineNum = 0
        for line in file_reader:
            line = line.strip()
            if lineNum % 2 == 0:
                if self.log: print 'Learning from game', line
            else:
                game_data = parseGame(line)
                if game_data is not None:

                    game = GamePlayer(white_engine=Lichess(game_data, 'w'), black_engine=Lichess(game_data, 'b'), log = False)
                    game.play_game()

                    winner = game.board.result
                    tdLearner = TDLearnerGame(white_engine=Lichess(game_data, 'w'), black_engine=Lichess(game_data, 'b'), \
                        win = winner, feature_extractor=self.extractor, eval_fn=self.eval_fn, eta=self.eta, log=self.log)
                    # TODO look at eval_fn necessecity
                    weights = tdLearner.learn_from_game(weights)
                    if self.log: print
            lineNum += 1
        if self.log: print weights
        print "These are the weights I've learned for %s" % ("white" if self.turn == 'w' else "black")
        # normalize(weights)
        for feature, weight in sorted(dict(weights).items()):
            print feature, ": ", weight
        file_reader.close()
        print weights
        return weights
        # return AlphaBeta(eval_function = lambda board : eval_fn(board, weights, turn))

    def get_board_evaluator(self):
        weights = self.get_weights()
        return lambda board : self.eval_fn(board, weights, self.turn)

    def get_engine(self):
        return AlphaBeta(self.get_board_evaluator())


def get_eval(weights):
    return lambda board : self.eval_fn(board, weights, self.turn)

# TESTING STUFF
data_folder = '../scraper/data/'
white_learner = TDLearnerData('w', feature_extractor, learning_eval, data_folder, 0.0001, True)
black_learner = TDLearnerData('b', feature_extractor, learning_eval, data_folder, 0.0001, False)
# weights = white_learner.get_weights()
w_eval = white_learner.get_board_evaluator()
b_eval = black_learner.get_board_evaluator()

# for _ in range(10):
game = GamePlayer(Human(), ForcedLineAlphaBeta(b_eval, 1), log=True)
# game1 = GamePlayer(EpsGreedyAlphaBeta(w_eval, 0.2), ForcedLineAlphaBeta(b_eval, 1), log=True)
# game2 = GamePlayer(ForcedLineAlphaBeta(w_eval, 1), EpsGreedyAlphaBeta(b_eval, 0.2), log=False)

# game = GamePlayer(EpsGreedyAlphaBeta(b_eval, 0.1), DynamicDepthAlphaBeta(w_eval), log=False)
# game = GamePlayer(AlphaBeta(w_eval), EpsGreedyAlphaBeta(b_eval, 0.5), log=False)
# game = GamePlayer(DepthlessAlphaBeta(w_eval), EpsGreedyAlphaBeta(b_eval, 0.5), log=False)
# game = GamePlayer(DepthlessAlphaBeta(lambda board : eval(board, weights, 'w')), EpsGreedyAlphaBeta(lambda board : eval(board, weights, 'b')), log=True)
# game = GamePlayer(white_engine=get_engine(eval, 'w', feature_extractor), black_engine=get_engine(eval, 'b', feature_extractor))
game.play_n_games(1)
# game1.play_n_games(5)
# game2.play_n_games(5)
