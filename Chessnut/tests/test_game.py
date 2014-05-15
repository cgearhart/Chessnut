
import unittest
from Chessnut.game import Game, InvalidMove, DEFAULT_FEN


# Default FEN string
START_POS = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'

# Opening moves for white in sorted() order
LEGAL_OPENINGS = ['a2a3', 'a2a4', 'b1a3', 'b1c3', 'b2b3', 'b2b4', 'c2c3',
                  'c2c4', 'd2d3', 'd2d4', 'e2e3', 'e2e4', 'f2f3', 'f2f4',
                  'g1f3', 'g1h3', 'g2g3', 'g2g4', 'h2h3', 'h2h4']

# set of all board positions in index form and algebraic notation
ALG_POS = set(chr(l) + str(x) for x in range(1, 9) for l in range(97, 105))
IDX_POS = set(range(64))


class DefaultGameTest(unittest.TestCase):

    def setUp(self):
        self.game = Game()

    def test_fen(self):
        self.assertEqual(self.game.fen, DEFAULT_FEN)

    def test_get_moves(self):
        # legal openings
        game = Game()
        self.assertEqual(sorted(game.get_moves()), LEGAL_OPENINGS)

    def test_history(self):
        game = Game()
        self.assertEqual(game.history, [(DEFAULT_FEN, '')])
        game.apply_move('e2e4')
        self.assertTrue(len(game.history) == 2)

    # def test_apply_move(self):


    #     # apply moves
    #     game.apply_move('g8h7')
    #     self.assertEqual(str(game), 'Q2qk3/7b/8/8/8/8/7P/4K3 w - - 1 2')
    #     game.apply_move('h2h4')
    #     self.assertEqual(str(game), 'Q2qk3/7b/8/8/7P/8/8/4K3 b - h3 0 2')

    #     # block vector tail with capture
    #     moves = ['d8c8', 'd8b8', 'd8a8', 'e8f8', 'e8d7', 'e8e7', 'e8f7',
    #              'g8f7', 'g8e6', 'g8d5', 'g8c4', 'g8b3', 'g8a2', 'g8h7']
    #     game.reset(fen='Q2qk1b1/8/8/8/8/8/7P/4K3 b - - 0 1')
    #     self.assertEqual(game.get_moves(), moves)
    #     game.apply_move('d8b8')
    #     moves = set(game.get_moves())
    #     self.assertIn('a8b8', moves)
    #     self.assertNotIn('a8c8', moves)

    #     # capture
    #     fen = 'r2q1rk1/pppbbppp/2n5/3p4/3PN3/4PN2/1PPBBPPP/R2Q1RK1 b - - 0 9'
    #     game = Game(fen=fen)
    #     game.apply_move('d5e4')
    #     n_fen = 'r2q1rk1/pppbbppp/2n5/8/3Pp3/4PN2/1PPBBPPP/R2Q1RK1 w - - 0 10'
    #     self.assertEqual(str(game), n_fen)

    #     # invalid move
    #     game = Game()
    #     with self.assertRaises(InvalidMove):
    #         game.apply_move('e2e2')

class GameStatusTest(GameTest):
    
    def testStatus(self):
        # normal
        game = Game()
        self.assertTrue(game.status == Game.NORMAL)

        # check
        fen = ''
        game.set_fen()
        self.assertTrue(game.status == Game.CHECK)

        # checkmate
        fen = '8/p5kp/1p6/2p5/P5P1/2n4P/r2p4/1K6 w - - 2 37'
        game.set_fen()
        self.assertTrue(game.status == Game.CHECKMATE)

        # stalemate
        fen = ''
        game.set_fen()
        self.assertTrue(game.status == Game.STALEMATE)


class CastlingTest(GameTest):

    #     # white castling
    #     fen = 'r3k2r/pppqbppp/3pb3/8/8/3PB3/PPPQBPPP/R3K2R w KQkq - 0 7'
    #     new_fen = 'r3k2r/pppqbppp/3pb3/8/8/3PB3/PPPQBPPP/R4RK1 b kq - 1 7'
    #     game = Game(fen=fen)
    #     game.apply_move('e1g1')
    #     self.assertEqual(str(game), new_fen)
    #     new_fen = 'r3k2r/pppqbppp/3pb3/8/8/3PB3/PPPQBPPP/2KR3R b kq - 1 7'
    #     game = Game(fen=fen)
    #     game.apply_move('e1c1')
    #     self.assertEqual(str(game), new_fen)

    #     # black castling
    #     fen = 'r3k2r/pppqbppp/3pb3/8/8/3PB3/PPPQBPPP/R3K2R b KQkq - 0 7'
    #     new_fen = 'r4rk1/pppqbppp/3pb3/8/8/3PB3/PPPQBPPP/R3K2R w KQ - 1 8'
    #     game = Game(fen=fen)
    #     game.apply_move('e8g8')
    #     self.assertEqual(str(game), new_fen)
    #     new_fen = '2kr3r/pppqbppp/3pb3/8/8/3PB3/PPPQBPPP/R3K2R w KQ - 1 8'
    #     game = Game(fen=fen)
    #     game.apply_move('e8c8')
    #     self.assertEqual(str(game), new_fen)

    #     # Disable castling on capture
    #     fen = '1r2k2r/3nb1Qp/p1pp4/3p4/3P4/P1N2P2/1PP3PP/R1B3K1 w k - 0 22'
    #     new_fen = '1r2k2Q/3nb2p/p1pp4/3p4/3P4/P1N2P2/1PP3PP/R1B3K1 b - - 0 22'
    #     game = Game(fen=fen)
    #     game.apply_move('g7h8')
    #     self.assertEqual(str(game), new_fen)

    #     # castling into occupied space & king moving into check
    #     fen = '8/2p5/5p2/7r/7P/3R1P2/P3R1P1/2k1K3 b - - 13 46'
    #     game = Game(fen=fen)
    #     self.assertIn('c7c6', game.get_moves())
    #     fen = '8/8/2p2p2/7r/7P/3R1P2/P3R1P1/2k1K3 w - - 0 47'
    #     game = Game(fen=fen)
    #     self.assertNotIn('e1c1', game.get_moves())

    #     # castling through check
    #     fen = 'r3k2r/8/8/8/8/8/8/3RKR2 b kq - 0 1'
    #     game = Game(fen=fen)
    #     self.assertNotIn('e8c8', game.get_moves(idx_list=[4]))
    #     self.assertNotIn('e8g8', game.get_moves(idx_list=[4]))

    #     # castling out of check
    #     fen = 'r3rk2/8/8/8/8/8/8/R3K2R w KQ - 0 1'
    #     game = Game(fen=fen)
    #     self.assertNotIn('e1c8', game.get_moves(idx_list=[60]))

class PawnMovesTest(GameTest):

    def setUp(self):
        pass

#     # pawn promotion
    #     fen = '3qk1b1/P7/8/8/8/8/7P/4K3 w - - 0 1'
    #     game = Game(fen=fen)
    #     game.apply_move('a7a8q')
    #     self.assertEqual(str(game), 'Q2qk1b1/8/8/8/8/8/7P/4K3 b - - 0 1')

    #     # en passant
    #     fen = 'rnbqkbnr/ppp2ppp/4p3/3pP3/8/8/PPPP1PPP/RNBQKBNR w KQkq d6 0 1'
    #     game = Game(fen=fen)
    #     self.assertEqual(game.get_moves(idx_list=[28]), ['e5d6'])

    #     # white en passant
    #     fen = 'rnbqkbnr/ppp2ppp/4p3/3pP3/8/8/PPPP1PPP/RNBQKBNR w KQkq d6 0 1'
    #     game = Game(fen=fen)
    #     game.apply_move('e5d6')
    #     new_fen = 'rnbqkbnr/ppp2ppp/3Pp3/8/8/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1'
    #     self.assertEqual(str(game), new_fen)

    #     # black en passant
    #     fen = 'rnbqkbnr/ppp1pppp/8/8/3pP3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1'
    #     game = Game(fen=fen)
    #     game.apply_move('d4e3')
    #     new_fen = 'rnbqkbnr/ppp1pppp/8/8/8/4p3/PPPP1PPP/RNBQKBNR w KQkq - 0 2'
    #     self.assertEqual(str(game), new_fen)

