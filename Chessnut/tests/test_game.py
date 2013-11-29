
import unittest
from Chessnut.game import Game, InvalidMove


# Default FEN string
START_POS = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'

# Opening moves for white in sorted() order
LEGAL_OPENINGS = ['a2a3', 'a2a4', 'b1a3', 'b1c3', 'b2b3', 'b2b4', 'c2c3',
                  'c2c4', 'd2d3', 'd2d4', 'e2e3', 'e2e4', 'f2f3', 'f2f4',
                  'g1f3', 'g1h3', 'g2g3', 'g2g4', 'h2h3', 'h2h4']

# set of all board positions in index form and algebraic notation
ALG_POS = set(chr(l) + str(x) for x in range(1, 9) for l in range(97, 105))
IDX_POS = set(range(64))


class GameTest(unittest.TestCase):

    def setUp(self):
        self.game = Game()

    def test_i2xy(self):
        for idx in xrange(64):
            self.assertIn(Game.i2xy(idx), ALG_POS)

    def test_xy2i(self):
        for pos in ALG_POS:
            self.assertIn(Game.xy2i(pos), IDX_POS)

    def test_str(self):
        self.game.reset()  # reset board to starting position
        self.assertEqual(str(self.game), START_POS)

    def test_fen_history(self):
        #
        self.game.reset()
        self.assertEqual(self.game.fen_history, [START_POS])
        self.game.apply_move('e2e4')
        hist = [START_POS,
                'rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1']
        self.assertEqual(self.game.fen_history, hist)

    def test_get_moves(self):
        #
        self.game.reset()
        self.assertEqual(sorted(self.game.get_moves()), LEGAL_OPENINGS)

        fen = 'rnbqkbnr/ppp2ppp/4p3/3pP3/8/8/PPPP1PPP/RNBQKBNR w KQkq d6 0 1'
        self.game = Game(fen=fen)
        self.assertEqual(self.game.get_moves(idx_list=[28]), ['e5d6'])

    def test_apply_move(self):
        # pawn promotion
        fen = '3qk1b1/P7/8/8/8/8/7P/4K3 w - - 0 1'
        self.game = Game(fen=fen)
        self.game.apply_move('a7a8q')
        self.assertEqual(str(self.game), 'Q2qk1b1/8/8/8/8/8/7P/4K3 b - - 0 1')
        
        # apply moves
        self.game.apply_move('g8h7')
        self.assertEqual(str(self.game), 'Q2qk3/7b/8/8/8/8/7P/4K3 w - - 1 2')
        self.game.apply_move('h2h4')
        self.assertEqual(str(self.game), 'Q2qk3/7b/8/8/7P/8/8/4K3 b - h3 0 2')

        # white castling
        fen = 'r3k2r/pppqbppp/3pb3/8/8/3PB3/PPPQBPPP/R3K2R w KQkq - 0 7'
        new_fen = 'r3k2r/pppqbppp/3pb3/8/8/3PB3/PPPQBPPP/R4RK1 b kq - 1 7'
        self.game = Game(fen=fen)
        self.game.apply_move('e1g1')
        self.assertEqual(str(self.game), new_fen)
        new_fen = 'r3k2r/pppqbppp/3pb3/8/8/3PB3/PPPQBPPP/2KR3R b kq - 1 7'
        self.game = Game(fen=fen)
        self.game.apply_move('e1c1')
        self.assertEqual(str(self.game), new_fen)

        # black castling
        fen = 'r3k2r/pppqbppp/3pb3/8/8/3PB3/PPPQBPPP/R3K2R b KQkq - 0 7'
        new_fen = 'r4rk1/pppqbppp/3pb3/8/8/3PB3/PPPQBPPP/R3K2R w KQ - 1 8'
        self.game = Game(fen=fen)
        self.game.apply_move('e8g8')
        self.assertEqual(str(self.game), new_fen)
        new_fen = '2kr3r/pppqbppp/3pb3/8/8/3PB3/PPPQBPPP/R3K2R w KQ - 1 8'
        self.game = Game(fen=fen)
        self.game.apply_move('e8c8')
        self.assertEqual(str(self.game), new_fen)

        # white en passant
        fen = 'rnbqkbnr/ppp2ppp/4p3/3pP3/8/8/PPPP1PPP/RNBQKBNR w KQkq d6 0 1'
        self.game = Game(fen=fen)
        self.game.apply_move('e5d6')
        new_fen = 'rnbqkbnr/ppp2ppp/3Pp3/8/8/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1'
        self.assertEqual(str(self.game), new_fen)

        # black en passant
        fen = 'rnbqkbnr/ppp1pppp/8/8/3pP3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1'
        self.game = Game(fen=fen)
        self.game.apply_move('d4e3')
        new_fen = 'rnbqkbnr/ppp1pppp/8/8/8/4p3/PPPP1PPP/RNBQKBNR w KQkq - 0 2'
        self.assertEqual(str(self.game), new_fen)

        # invalid move
        self.game.reset()
        with self.assertRaises(InvalidMove):
            self.game.apply_move('e2e2')
