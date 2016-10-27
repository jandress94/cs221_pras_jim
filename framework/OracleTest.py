
# class comares engine outputs with real game play
class OracleTest:
    def __init__(self, pmdict, engine):
        self.pmdict = pmdict
        self.engine = engine

    def compare(self):
        for pos, mv in self.pmdict:
            engine_move = (self.engine).get_best_move(pos)
            print "The engine chose the move ", str(engine_move)
            print "The data chose the move   ", str(mv)
            # TODO for LATER:
            # implement more thorough comparison (rather than just move1 = move2)
            # perhaps provide an evaluaton of the moves, etc.
            if str(mv) == str(engine_move):
                print "These moves are the same"
            else:
                print "THese moves are not the same"
