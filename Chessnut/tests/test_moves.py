
import unittest

from Chessnut.moves import MOVES


class MovesTest(unittest.TestCase):

    def test_moves(self):
        global MOVES

        # test that all the pieces are in the dictionary
        for piece in 'kqbnrpKQBNRP':
            self.assertIn(piece, MOVES)

            # test that every starting position is in the dictionary
            for idx in range(64):
                self.assertIsNotNone(MOVES[piece][idx])

                # test ordering of moves in each ray (should radiate out
                # from the starting index)
                for ray in MOVES[piece][idx]:
                    sorted_ray = sorted(ray, key=lambda x: abs(x - idx))
                    self.assertEqual(ray, sorted_ray)

        # verify that castling moves are present
        self.assertIn(6, MOVES['k'][4][0])
        self.assertIn(2, MOVES['k'][4][1])
        self.assertIn(62, MOVES['K'][60][0])
        self.assertIn(58, MOVES['K'][60][4])
