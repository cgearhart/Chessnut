# pylint: disable=too-many-instance-attributes, star-args
"""
"""

from itertools import imap, chain, groupby

from Chessnut.moves import gen


# map starting index to voided castling rights
RIGHTS = {60: 'KQ', 63: 'K', 56: 'Q', 4: 'kq', 0: 'q', 7: 'k'}

# Define constants for default game setup and state values
DEFAULT_FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'


def a2i(pos):
    """ Convert algebraic notation to board index """
    return (8 - int(pos[1])) * 8 + (ord(pos[0]) - ord('a'))


def i2a(idx):
    """ Convert board index to algebraic notation """
    return chr(97 + idx % 8) + str(8 - idx / 8)


class InvalidMove(Exception):
    """ Subclass base `Exception` to relay useful error messages """
    pass


class Game(object):
    """ """

    # Game states
    NORMAL = 0
    CHECK = 1
    CHECKMATE = 2
    STALEMATE = 3

    # Graph definition
    _nodes = [' '] * 64
    _edges = [[[] for _ in range(8)] for _ in range(64)]  # edges out from x
    _viewers = [set() for _ in range(64)]  # (idx, raynum) into node at x

    # chess game state information
    _player = 1  # white
    _rights = set('KQkq')
    _ep = None
    _ply = 0
    _turn = 1

    # Game data bookkeeping for fast lookup
    _status = NORMAL
    _king_location = [None, None]
    _edgemap = [gen(x) for x in range(64)]
    __changes = set()
    __fen_history = []
    __move_history = []

    def __init__(self, fen=DEFAULT_FEN):
        self._set_fen(fen)

    def _fen(self):
        """ Convert the game information to a fen string """
        ranks = []
        for rank in imap(groupby, zip(*[iter(self._nodes)] * 8)):
            tmp = [[len(list(g))] if e == ' ' else list(g) for e, g in rank]
            ranks.append(''.join(str(x) for x in chain(*tmp)))
        fen = ' '.join(['/'.join(ranks),
                        'bw'[self._player],
                        ''.join(x for x in 'KQkq' if x in self._rights) or '-',
                        '-' if not self._ep else i2a(self._ep),
                        str(self._ply),
                        str(self._turn)])
        return fen

    @property
    def fen(self):
        """ Return the FEN string for the current board """
        return self.__fen_history[-1]

    @property
    def history(self):
        """ List containing sequential position/move pairs """
        return zip(self.__fen_history, self.__move_history + [''])

    @property
    def status(self):
        """ Game status: NORMAL, CHECK, CHECKMATE, or STALEMATE """
        return self._status

    def _set_fen(self, fen_str):
        """ Set game configuration to the specified fen & preserve history """
        pos, _, state = fen_str.partition(' ')
        self.__fen_history.append(fen_str)
        self._set_state(state)

        # place the pieces on the board by setting the name of each node
        sym = [[' '] * int(p) if p.isdigit() else [p] for p in pos if p != '/']
        for idx, token in enumerate(chain(*sym)):
            self._modify(idx, token)

        # update the moves for each node
        self._update()

    def _set_state(self, state):
        """ Format the fields of the FEN state information to a game state """
        fields = state.split(' ')
        self._player = 'bw'.index(fields[0])
        self._rights = set(fields[1])
        self._ep = None if fields[2] == '-' else a2i(fields[2])
        self._ply = int(fields[3])
        self._turn = int(fields[4])

    def _modify(self, idx, token):
        """ Change the contents of a node and register for updates """
        self._nodes[idx] = token
        if token.lower() == "k":
            self._king_location[token.isupper()] = idx
        for rnum, ray in enumerate(self._edges[idx]):
            for end in ray:
                # stop watching node at 'end'
                self._viewers[end].remove((idx, rnum))
        self.__changes.update([(idx, i) for i in range(8)])
        self.__changes.update(self._viewers[idx])

    def _move(self, start, end):
        """ Perform an unchecked move from start to end on the graph """
        self._modify(end, self._nodes[start])
        self._modify(start, ' ')

    def undo(self):
        """ Undo the last move applied to the board """
        if self.__move_history:
            self.__move_history.pop()
            self.__fen_history.pop()  # pop the last then set to the previous
            self._set_fen(self.__fen_history.pop())

    def apply_move(self, move):
        """
        Apply a move given in simple algebraic notation.

        NOTE: simple algebraic notation differs from FEN move notation.
        Castling is not given any special notation, and pawn promotion piece
        is always lowercase.
        """

        # convert coords from algebraic notation to board index
        idx = a2i(move[0:2])
        end = a2i(move[2:4])

        # verify the legality of the move before applying it
        if move not in self._moves(indexes=[idx]):
            raise InvalidMove(move + " is not valid for game: " + self.fen)

        # grab the piece tokens
        token = self._nodes[idx]
        target = self._nodes[end]
        sym = token.lower()

        # perform an unsafe move from idx to end vertex on the graph
        self._move(idx, end)

        # always increment the ply count; reset for captures
        self._ply = self._ply + 1
        if target.lower() != ' ':
            self._ply = 0

        # handle promotion and en passant for pawns
        ep_idx = self._ep
        self._ep = None  # clear the ep state on every move
        if sym == "p":
            self._ply = 0  # reset the ply count on pawn moves

            if len(move) == 5:
                # replace the piece token at end for promotion
                # (switch case of promoted piece for white)
                new_piece = move[5].upper() if self._player else move[5]
                self._modify(end, new_piece)
            elif end == ep_idx:
                # handle en passant capture
                ep_tgt = idx + end % 8 - idx % 8  # idx +/- 1
                self._modify(ep_tgt, " ")  # remove the ep target
            elif abs(idx - end) == 16:
                # set ep for next turn by setting state and updating ep viewers
                self._ep = (idx + end) // 2
                self._modify(self._ep, " ")

        # unsafely move the rook on castling moves; don't need to check _rights
        # because it is already tested in .get_moves()
        if sym == "k":
            deltax = idx - end
            offset = self._player * 56  # white player position offset
            if deltax == 2:
                self._move(offset, offset + 3)
            elif deltax == -2:
                self._move(offset + 7, offset + 5)

        # update castling rights; must test start and end because opponent
        # captures can eliminate castling rights
        if sym == "k" or sym == "r" and self._rights:
            self._rights.difference_update(RIGHTS.get(idx, ''))
            self._rights.difference_update(RIGHTS.get(end, ''))

        # update the remaining state information (player & turn)
        self._player = self._player ^ 1
        self._turn = self._turn + self._player

        # update the history
        self.__fen_history.append(self._fen())
        self.__move_history.append(move)

        # important that update happens after the state change
        self._update()

    def get_moves(self, indexes=range(64)):
        """ The list of legal moves from each index for the active player """
        return sorted(list(self._moves(indexes)))

    def _moves(self, indexes=range(64)):
        """ Calculate the legal moves for the active player """
        moves = set()
        fmt = "{}{}{}".format

        for idx in indexes:

            token = self._nodes[idx]
            if not token.strip() or not self._is_active(idx):
                # skip the index if it is not the current player's piece
                continue

            kdx = self._king_location[token.isupper()]

            start = i2a(idx)
            for edge in chain(*self._edges[idx]):
                end = i2a(edge)

                if not self._safe(token, edge, kdx, kdx):
                    # skip if king is exposed after token moves from idx->end
                    continue

                if token.lower() == "p" and (edge < 8 or edge > 55):
                    # insert the possible piece types for pawn promotions here
                    # because they are the only moves with distinct notation
                    promotions = ['b', 'n', 'q', 'r']
                    moves.update([fmt(start, end, s) for s in promotions])
                    continue

                moves.add(fmt(start, end, ''))

        return moves

    def _update(self):
        """ Update edges for nodes that have been marked as changed """

        changes = set()

        while self.__changes:

            idx, rnum = self.__changes.pop()
            self._edges[idx][rnum] = []

            ray = self._trace(idx, rnum)
            if not ray:
                continue

            for end in ray:
                # register as a viewer for notification of changes to 'end'
                self._viewers[end].add((idx, rnum))

            # filter pawn moves because they have different rules
            token = self._nodes[idx]
            target = self._nodes[ray[-1]]
            is_blocked = target != ' '
            is_capture = token.islower() != target.islower()

            if token.lower() == 'p':
                if ray[-1] == self._ep and 16 < idx < 40:
                    # allow ep but mark it to be cleared on the next turn
                    changes.add((idx, rnum))
                elif rnum % 2 != (is_blocked and is_capture):
                    # drop pawn moves to empty diagonal or full forward cells
                    ray.pop()
            elif is_blocked and not is_capture:
                ray.pop()

            self._edges[idx][rnum] = ray

        # Insert castling moves - it is not necessary to track through viewers
        # list because the moves are updated every turn
        if "K" in self._rights and self._can_castle((60, 'K'), (56, 'R'), 4):
            self._edges[60][4] = [59, 58]
        if "Q" in self._rights and self._can_castle((60, 'K'), (63, 'R'), 0):
            self._edges[60][0] = [61, 62]
        if "k" in self._rights and self._can_castle((4, 'k'), (0, 'r'), 4):
            self._edges[4][4] = [3, 2]
        if "q" in self._rights and self._can_castle((4, 'k'), (7, 'r'), 0):
            self._edges[4][0] = [5, 6]

        self.__changes = changes  # propagate en passant tracking
        self._update_status()

    def _safe(self, sym, idx, kdx, vdx):
        """ True if sym at idx guards the piece at kdx from viewers of vdx """
        # temporarily replace the piece at tdx
        token = self._nodes[idx]
        self._nodes[idx] = sym

        # test to see whether the king is in check
        for end, rnum in self._viewers[vdx]:
            if self._nodes[end].isupper() != self._nodes[kdx].isupper():
                ray = self._trace(end, rnum)
                if ray and ray[-1] == kdx:
                    self._nodes[idx] = token
                    return False

        # put the original piece back
        self._nodes[idx] = token

        return True

    def _can_castle(self, kdata, rdata, ray):
        """ Test castling rights conditions """
        kdx, ksym = kdata
        rdx, rsym = rdata
        k_ok = self._nodes[kdx] == ksym and self._safe(ksym, kdx, kdx, kdx)
        r_ok = self._nodes[rdx] == rsym
        edx = kdx + 2 - ray  # where the king will end up
        can_move = self._edges[kdx][ray] and self._safe(ksym, *[edx] * 3)
        if k_ok and r_ok and can_move:
            return True

    def _trace(self, idx, rnum):
        """ Return the first n unobstructed nodes in a ray """
        token = self._nodes[idx].strip()
        if not token:
            return []

        ray = self._edgemap[idx][token][rnum]

        for edx, end in enumerate(ray):
            if self._nodes[end].strip():
                return ray[:edx + 1]

        return ray

    def _is_active(self, idx):
        """ Test whether the piece at idx belongs to the active player """
        token = self._nodes[idx].strip()
        return token and token.isupper() == self._player

    def _update_status(self):
        """ Update the game status for check/checkmate/stalemate """

        king_viewers = self._viewers[self._king_location[self._player]]
        is_exposed = [True for i, _ in king_viewers if not self._is_active(i)]
        edges = [e for i, e in enumerate(self._edges) if self._is_active(i)]
        can_move = list(chain(*list(chain(*edges))))

        self._status = Game.NORMAL
        if is_exposed:
            self._status = Game.CHECK
            if not can_move:
                self.status = Game.CHECKMATE
        elif not can_move:
            self._status = Game.STALEMATE
