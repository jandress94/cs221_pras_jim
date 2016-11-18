from GamePlayer import GamePlayer
from RandomEngine import Random
from LichessEngine import Lichess
from game_parser import parseGame
from os import listdir
from os.path import isfile, join

# game = GamePlayer(black_engine=Random())
# game.play_game()

data_folder = '../scraper/data/'
f = listdir(data_folder)[0]
file_reader = open(join(data_folder, f), 'r')
lineNum = 0
for line in file_reader:
    line = line.strip()
    if lineNum % 2 == 0:
        print 'Playing Game', line
    else:
        game_data = parseGame(line)
        if game_data is not None:
            game = GamePlayer(white_engine=Lichess(game_data, 'w'), black_engine=Lichess(game_data, 'b'))
            game.play_game()
            print
    lineNum += 1

file_reader.close()