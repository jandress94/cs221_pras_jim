from GamePlayer import GamePlayer
from RandomEngine import Random
from LichessEngine import Lichess
from AlphaBetaEngine import AlphaBeta
from game_parser import parseGame
from os import listdir
from os.path import isfile, join
from Features import *

# game = GamePlayer(black_engine=Random())
# game.play_game()

# data_folder = '../scraper/data/'
# f = listdir(data_folder)[0]
# file_reader = open(join(data_folder, f), 'r')
# lineNum = 0
# for line in file_reader:
#     line = line.strip()
#     if lineNum % 2 == 0:
#         print 'Playing Game', line
#     else:
#         game_data = parseGame(line)
#         if game_data is not None:
#             game = GamePlayer(white_engine=Lichess(game_data, 'w'), black_engine=Lichess(game_data, 'b'))
#             game.play_game()
#             print
#     lineNum += 1

# file_reader.close()

# my guess
weights = {'my mobility': 1, 'my pieces n': -3, \
        'opponent pieces n': 3, 'my pieces k': -2, \
        'opponent pieces k': 2, 'my pieces r': -5, \
        'my pieces q': -9, 'my pieces b': -3, \
        'opponent pieces b': 3, 'opponent pieces r': 5, \
        'opponent pieces q': 9,'opponent pieces p': 1, \
        'my pieces p': -1, 'opponent mobility': -1}

# what we hard coded 
weights2 = {'my mobility': 0.00794453399588799, 'my pieces n': -0.37770634987581486, \
        'opponent pieces n': 0.3259256111814666, 'my pieces k': -0.217740060989421, \
        'opponent pieces k': 0.1975389514945781, 'my pieces r': -0.43857848646965436, \
        'my pieces q': -0.1965540356358875, 'my pieces b': -0.32153572268987485, \
        'opponent pieces b': 0.25215039828608354, 'opponent pieces r': 0.30588559507108515, \
        'opponent pieces q': 0.106430088995805,'opponent pieces p': 0.5986063533783763, \
        'my pieces p': -0.9282910790839152, 'opponent mobility': -0.006369695141804626}

# recomputed
weights3 = {'my pieces b': -0.21938452840893785, 'opponent pieces n': 0.012559381665896827, \
    'opponent pieces q': 0.009034347366887671, 'opponent pieces p': 0.021073937083046747, \
    'opponent pieces r': -0.001320935277564358, 'my pieces k': -0.2187209500603979, \
    'my mobility': 0.004476556143545838, 'my pieces n': -0.31590142245629727, \
    'my pieces p': -0.9806307808606477, 'my pieces q': -0.09746731364334703, \
    'my pieces r': -0.33623482229558654, 'opponent pieces b': 0.014244966737145195, \
    'opponent mobility': 0.013870714758610512, 'opponent pieces k': -0.009498968464082092}

# weights 3 swapped
weights4 = {'opponent pieces b': -0.21938452840893785, 'my pieces n': 0.012559381665896827, \
    'my pieces q': 0.009034347366887671, 'my pieces p': 0.021073937083046747, \
    'my pieces r': -0.001320935277564358, 'opponent pieces k': -0.2187209500603979, \
    'opponent mobility': 0.004476556143545838, 'opponent pieces n': -0.31590142245629727, \
    'opponent pieces p': -0.9806307808606477, 'opponent pieces q': -0.09746731364334703, \
    'opponent pieces r': -0.33623482229558654, 'my pieces b': 0.014244966737145195, \
    'my mobility': 0.013870714758610512, 'my pieces k': -0.009498968464082092}

# weights with every two
weights5 = {'my pieces b': -0.2893630954069259, 'opponent mobility': -0.009047193001818138, \
    'opponent pieces q': 0.022491678652511306, 'opponent pieces p': 0.5016118232502623, \
    'opponent pieces r': 0.2862796002329135, 'my pieces k': -0.1121762494805236, \
    'my pieces r': -0.2220589904426514, 'my pieces n': -0.2602621308703907, \
    'my pieces p': -0.4967786641973036, 'my pieces q': -0.2318797920150573, \
    'my mobility': 0.032986011312793606, 'opponent pieces b': 0.11468715464276205, \
    'opponent pieces n': 0.2593102126638174, 'opponent pieces k': 0.22001222207990012}

eval_white = lambda board: eval(board, weights5, 'w')
eval_black = lambda board: eval(board, weights2, 'b')

game = GamePlayer(white_engine = AlphaBeta(eval_white), black_engine = AlphaBeta(eval_black))
game.play_game()