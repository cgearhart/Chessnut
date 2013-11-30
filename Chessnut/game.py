
"""
The game module implements core Chessnut class, `Game`, to control a chess
game.

Two additional classes are defined: `InvalidMove` -- a subclass of the base
`Exception` class, and `State` -- a namedtuple for handling game state
information.

Chessnut has neither an *engine*, nor a *GUI*, and it cannot currently
handle any chess variants (e.g., Chess960) that are not equivalent to standard
chess rules.
"""

from collections import namedtuple

from Chessnut.board import Board
from Chessnut.moves import MOVES

# Define a named tuple with FEN field names to hold game state information
State = namedtuple('State', ['player', 'rights', 'en_passant', 'ply', 'turn'])


class InvalidMove(Exception):
    """
    Subclass base `Exception` so that exception handling doesn't have to
    be generic.
    """
    pass


class Game(object):
    """
    This class manages a chess game instance -- it stores an internal
    representation of the position of each piece on the board in an instance
    of the `Board` class, and the additional state information in an instance
    of the `State` namedtuple class.
    """

    default_fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
    board = None
    state = None
    move_history = []
    fen_history = []

    def __init__(self, fen=default_fen, validate=True):
        """
        Initialize the game board to the supplied FEN state (or the default
        starting state if none is supplied), and determine whether to check
        the validity of moves returned by `get_moves()`.
        """
        self.validate = validate
        self.reset(fen=fen)

    def __str__(self):
        """Return the current FEN representation of the game."""
        return ' '.join(str(x) for x in [self.board] + list(self.state))

    @staticmethod
    def i2xy(pos_idx):
        """
        Convert a board index to algebraic notation.
        """
        return chr(97 + pos_idx % 8) + str(8 - pos_idx / 8)

    @staticmethod
    def xy2i(pos_xy):
        """
        Convert algebraic notation to board index.
        """
        return (8 - int(pos_xy[1])) * 8 + (ord(pos_xy[0]) - ord('a'))

    def set_fen(self, fen):
        """
        Parse a FEN string into components and store in the `board` and `state`
        properties, and append the FEN string to the game history *without*
        clearing it first.
        """
        self.fen_history.append(fen)
        fields = fen.split(' ')
        fields[4] = int(fields[4])
        fields[5] = int(fields[5])
        self.board = Board(position=fields[0])
        self.state = State(*fields[1:])

    def reset(self, fen=default_fen):
        """
        Clear the game history and set the board to the default starting
        position.
        """
        self.move_history = []
        self.fen_history = []
        self.set_fen(fen)

    def apply_move(self, move):
        """
        Update the state information (player, castling rights, en passant
        target, ply, and turn), apply the move to the game board, and
        update the game history.
        """

        # declare the status fields using default parameters
        fields = ['w', 'KQkq', '-', 0, 1]

        start = Game.xy2i(move[:2])
        end = Game.xy2i(move[2:4])
        piece = self.board.get_piece(start)
        target = self.board.get_piece(end)

        if self.validate and move not in self.get_moves(idx_list=[start]):
            raise InvalidMove("Illegal move: {}".format(move))

        # toggle the active player
        if self.state.player == 'w':
            fields[0] = 'b'
        elif self.state.player == 'b':
            fields[0] = 'w'

        # modify castling rights - the set of castling rights that *might*
        # be voided by a move is uniquely determined by the starting index
        # of the move - regardless of what piece moves from that position
        # (excluding chess variants like chess960).
        void_set = {0: 'q', 4: 'kq', 7: 'k',
                    56: 'Q', 60: 'KQ', 63: 'K'}.get(start, '')
        new_rights = [r for r in self.state.rights if r not in void_set]
        fields[1] = ''.join(new_rights) or '-'

        # set en passant target square when a pawn advances two spaces
        if piece.lower() == 'p' and abs(start - end) == 16:
            fields[2] = Game.i2xy((start + end) // 2)

        # reset the half move counter when a pawn moves or is captured
        fields[3] = self.state.ply + 1
        if piece.lower() == 'p' or target.lower() != ' ':
            fields[3] = 0

        # Increment the turn counter when the next move is from white, i.e.,
        # the current player is black
        fields[4] = self.state.turn
        if self.state.player == 'b':
            fields[4] = self.state.turn + 1

        # check for pawn promotion
        if len(move) == 5:
            piece = move[4]
            if self.state.player == 'w':
                piece = piece.upper()

        # record the move in the game history and apply it to the board
        self.move_history.append(move)
        self.board.move_piece(start, end, piece)

        # move the rook to the other side of the king in case of castling
        c_type = {62: 'K', 58: 'Q', 6: 'k', 2: 'q'}.get(end, None)
        if piece.lower() == 'k' and c_type and c_type in self.state.rights:
            coords = {'K': (63, 61), 'Q': (56, 59),
                      'k': (7, 5), 'q': (0, 3)}[c_type]
            r_piece = self.board.get_piece(coords[0])
            self.board.move_piece(coords[0], coords[1], r_piece)

        # in en passant remove the piece that is captured
        if piece.lower() == 'p' and self.state.en_passant != '-':
            ep_tgt = Game.xy2i(self.state.en_passant)
            if ep_tgt < 24:
                self.board.move_piece(end + 8, end + 8, ' ')
            elif ep_tgt > 32:
                self.board.move_piece(end - 8, end - 8, ' ')

        # state update must happen after castling
        self.set_fen(' '.join(str(x) for x in [self.board] + list(fields)))

    def get_moves(self, player=None, idx_list=xrange(64)):
        """
        Find the set of legal moves (i.e., moves that abide all the rules of
        standard chess) for the specified player at the specified starting
        index. If no player is provided, it uses the currently active player.
        If no index is provided, it finds all legal moves for the player.
        """
        if not self.validate:
            return self._all_moves(player=player, idx_list=idx_list)

        res_moves = []
        test_board = Game(fen=str(self), validate=False)

        for move in self._all_moves(player=player, idx_list=idx_list):
            test_board.reset(fen=str(self))
            test_board.apply_move(move)

            # a move is legal unless the opponent can attack the king at the
            # end of a move
            k_idx = [x for x in xrange(64)
                     if test_board.board.get_piece(x).lower() == 'k'
                     and test_board.board.get_owner(x) == self.state.player]

            tgts = set([m[2:4] for m in test_board.get_moves()])

            if Game.i2xy(k_idx[0]) not in tgts:
                res_moves.append(move)
        return res_moves

    def _all_moves(self, player=None, idx_list=xrange(64)):
        """
        Find all moves for the given player at the specified starting index.
        _all_moves() differs from get_moves in that it performs no validation
        on the legality of the moves returned - so _all_moves() can return
        moves that would leave the player in check.
        """
        res_moves = []
        for start in idx_list:
            if self.board.get_owner(start) != (player or self.state.player):
                continue

            piece = self.board.get_piece(start)
            rays = MOVES.get(piece, [''] * 64)

            for ray in rays[start]:
                # Trace each of the 8 (or fewer) possible directions that a
                # piece at the given starting index could move

                res_moves.extend(self._trace_ray(start, piece, ray))

        return res_moves

    def _trace_ray(self, start, piece, ray):
        """
        Trace along the rays for the specified piece and starting location,
        and validate that the piece can legally move there (do not validate
        whether the move would result in check).
        """
        res_moves = []

        for end in ray:

            sym = piece.lower()
            del_x = (end - start) % 8
            move = [Game.i2xy(start) + Game.i2xy(end)]
            tgt_owner = self.board.get_owner(end)

            # Abort if the current player owns the piece at the end point
            if tgt_owner == self.state.player:
                break

            # Test castling exception for king
            elif sym == 'k' and del_x == 2:
                rights = {62: 'K', 58: 'Q', 6: 'k', 2: 'q'}.get(end, '')
                mid_p = self.board.get_piece((start + end) // 2)
                if rights not in self.state.rights or not mid_p.isspace():
                    # Abort castling because missing castling rights
                    # or piece in the way
                    break

            # Test en passant exception for pawn
            if sym == 'p' and del_x != 0 and not tgt_owner:
                ep_coords = self.state.en_passant
                if ep_coords == '-' or end != Game.xy2i(ep_coords):
                    break

            # Pawns cannot move forward to a non-empty square
            elif tgt_owner and sym == 'p' and del_x == 0:
                break

            # Pawn promotions should list all possible promotions
            if piece.lower() == 'p' and (end < 8 or end > 56):
                move = [move[0] + s for s in ['b', 'n', 'r', 'q']]

            res_moves.extend(move)

            # Cannot continue beyond capturing an enemy piece
            if tgt_owner:
                break
        return res_moves
