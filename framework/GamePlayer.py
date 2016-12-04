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
            
    def print_result(self, i):
        if not self.log: return
        print "**************** RESULTS FOR GAME %d ****************" % i
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

    def print_game_stats(self, p_stats, player):
        print player, " made a total of ", p_stats["num moves"], " moves"
        print player, " on average had ", p_stats["avg legal moves"], " legal moves"
        if p_stats["game won at"] == 0:
            print player, " lost."
        else:
            print player, " called the game after ", p_stats["game won at"], " legal moves"

    def print_agg_stats(self, p_stats, player):
        print "**************** TOTALS FOR %s ****************" % player.upper()
        print "On average, ", player, " made ", p_stats["num moves"], " moves"
        print "On average, ", player, " had ", p_stats["avg legal moves"], " legal moves"

    def play_n_games(self, n):
        def add(d1, d2):
            return {key:d1[key] + d2[key] for key in d1}

        def divide_by(d, m):
            return {key:float(d[key])/m for key in d}


        counter = {'w':0, 'd':0, 'b':0}
        w_averages = {"num moves":0, "avg legal moves":0, "game won at":0}
        b_averages = {"num moves":0, "avg legal moves":0, "game won at":0}
        predict_avg = 0
        for i in range(n):
            w_stats, b_stats, result = self.play_game()
            self.print_result(i)

            counter[result] += 1
            w_averages = add(w_stats, w_averages)
            b_averages = add(b_stats, b_averages)
            predict_avg += self.board.moves - max(w_stats["game won at"], b_stats["game won at"])
            self.print_game_stats(w_stats, "white")
            self.print_game_stats(b_stats, "black")
        w_averages = divide_by(w_averages, n)
        b_averages = divide_by(b_averages, n)
        predict_avg /= float(n)
        "**************** AGGREGATE STATS DUMP ****************"
        print "In %d games there were %d wins for white, %d wins for black, and %d draws" % (n, counter['w'], counter['b'], counter['d'])
        print "On average, the winner was certain of a win %d moves before the win" % predict_avg
        self.print_agg_stats(w_averages, "white")
        self.print_agg_stats(b_averages, "black")

    def play_game(self):
        self.board = Board()
        # relevant stats
        # avg legal moves
        w_stats = {"num moves":0, "avg legal moves":0, "game won at": 0}
        b_stats = {"num moves":0, "avg legal moves":0, "game won at": 0}
        self.print_log(self.board)
        while self.board.result == None:
            if self.board.turn == 'w':
                w_stats["num moves"] += 1
                w_stats["avg legal moves"] += len(self.board.legal_moves)
                move, ev = self.white_engine.get_next_move(self.board)
                if self.log: print "white evaluated ", move, " to ", ev
                if ev > 1000 and w_stats["game won at"] == 0:
                    w_stats["game won at"] = self.board.moves
            else:
                b_stats["num moves"] += 1
                b_stats["avg legal moves"] += len(self.board.legal_moves)
                move, ev = self.black_engine.get_next_move(self.board)
                if self.log: print "black evaluated ", move, " to ", ev
                if ev > 1000 and b_stats["game won at"] == 0:
                    b_stats["game won at"] = self.board.moves
            self.print_move_information(move)
            self.board = self.board.make_move_from_move(move)
            self.print_log(self.board)
        # in case we didn't figure out that we were winning until the end
        if w_stats["game won at"] == 0 and b_stats["game won at"] == 0:
            if self.board.result == 'w':
                w_stats["game won at"] = self.board.moves
            elif self.board.result == 'b':
                b_stats["game won at"] = self.board.moves

        # print w_stats, b_stats
        w_stats["avg legal moves"] /= float(w_stats["num moves"])
        b_stats["avg legal moves"] /= float(b_stats["num moves"])
        return (w_stats, b_stats, self.board.result)
