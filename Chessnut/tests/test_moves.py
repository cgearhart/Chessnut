
import random
import unittest

from itertools import chain

from Chessnut.moves import gen

PIECES = "kqbnrpKQBNRP"

MSG = "{!s} failed {} at {!s}\n{!s}"


class MovesTest(unittest.TestCase):

    def test_pieces(self):
        """ test that the move set contains all piece types """
        moves = gen(random.randint(0, 63))
        for piece in PIECES:
            self.assertIn(piece, moves)

    def test_corner(self):
        """ test features of move sets generated for corner cells """

        corners = [0, 7, 56, 63]
        expected = {'p': 0, 'n': 2, 'b': 7, 'r': 14, 'q': 21, 'k': 3}

        for idx in corners:
            moves = gen(idx)
            for sym in PIECES:
                act = len(list(chain(*moves[sym])))
                exp = expected[sym.lower()]
                self.assertEqual(act, exp,
                                 msg=MSG.format(sym,
                                                "corner test",
                                                idx,
                                                moves[sym]))

    def test_edge(self):
        """ test the upper and lower limits of move sets generated at walls """
        choices = range(8, 48, 8) + range(7, 63, 8)
        min_exp = {'p': 2, 'n': 2, 'b': 7, 'r': 14, 'q': 21, 'k': 5}
        max_exp = {'p': 4, 'n': 4, 'b': 7, 'r': 14, 'q': 21, 'k': 5}
        idx = random.choice(choices)
        moves = gen(idx)
        sym = random.choice(PIECES)

        self.assertTrue(len(list(chain(*moves[sym]))) <= max_exp[sym.lower()],
                        msg="{!s} failed {} at {!s}\n{!s}"
                        .format(sym, "max edge test", idx, moves[sym]))
        self.assertTrue(min_exp[sym.lower()] <= len(list(chain(*moves[sym]))),
                        msg="{!s} failed {} at {!s}\n{!s}"
                        .format(sym, "min edge test", idx, moves[sym]))

    def test_center(self):
        choices = list(chain(*[range(8 + i, 48 + i, 8) for i in xrange(1, 7)]))
        min_exp = {'p': 3, 'n': 4, 'b': 9, 'r': 14, 'q': 23, 'k': 8}
        max_exp = {'p': 4, 'n': 8, 'b': 14, 'r': 14, 'q': 28, 'k': 8}
        idx = random.choice(choices)
        moves = gen(idx)
        sym = random.choice(PIECES)

        self.assertTrue(len(list(chain(*moves[sym]))) <= max_exp[sym.lower()],
                        msg="{!s} failed {} at {!s}\n{!s}"
                        .format(sym, "max center test", idx, moves[sym]))
        self.assertTrue(min_exp[sym.lower()] <= len(list(chain(*moves[sym]))),
                        msg="{!s} failed {} at {!s}\n{!s}"
                        .format(sym, "min center test", idx, moves[sym]))

    def test_exceptions(self):
        for i in range(6):
            idx_a = 9 + i
            idx_b = 49 + i

            moves = gen(idx_a)
            self.assertEqual(len(moves['p'][6]), 2,
                             msg="p failed {} at {!s}\n{!s}"
                             .format("exception test", idx_a, moves['p']))
            moves = gen(idx_b)
            self.assertEqual(len(moves['P'][2]), 2,
                             msg="P failed {} at {!s}\n{!s}"
                             .format("exception test", idx_b, moves['P']))
