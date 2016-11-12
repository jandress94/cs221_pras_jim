from GamePlayer import GamePlayer
from RandomEngine import Random

game = GamePlayer(black_engine=Random())
game.play_game()