
from Chessnut.board import Board
import unittest


class BoardTest(unittest.TestCase):

    def setUp(self):
        # implicitly tests set_position (called from __init__)
        self.board = Board('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR')

    def test_get_piece(self):
        self.board.set_position('r7/8/8/8/8/8/8/8')
        self.assertEqual(self.board.get_piece(0), 'r')
        self.assertEqual(self.board.get_piece(1), ' ')

    def test_get_owner(self):
        self.board.set_position('r7/8/8/8/8/8/8/7R')
        self.assertEqual(self.board.get_owner(0), 'b')
        self.assertEqual(self.board.get_owner(63), 'w')
        self.assertEqual(self.board.get_owner(32), None)

    def test_move_piece(self):
        self.board.set_position('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR')
        self.board.move_piece(52, 36, 'P')  # e2e4
        self.assertEqual(str(self.board),
                         'rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR')

    def test_find_all_pieces(self):
        self.board.set_position('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR')
        self.assertEqual(self.board.find_all_pieces('P'), [48, 49, 50, 51, 52, 53, 54, 55])
        self.assertEqual(self.board.find_all_pieces('R'), [56, 63])
        self.assertEqual(self.board.find_all_pieces('r'), [0, 7])
