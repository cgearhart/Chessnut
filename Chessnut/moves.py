"""
Moves generates and returns the superset of legal moves in classic chess in a
64 x 8 x 8 array. The index of the outermost array is the board index, i. The
middle layer is a dict keyed to the letter corresponding to the piece type, p.
The innermost index corresponds to the direction of movement, d. Each element
of the innermost array is a (possibly empty) list of board indexes that are
reachable by a piece p, at location i, moving in direction d, sorted by
increasing distance from the starting point.

A raster-style index is used for the chessboard beginning at the top left
and proceeding right before moving down to the next line (i.e., 'a8'=0, 'h8'=8,
'a7'=8,...'h1'=63). Movement directions map to inner array index corresponding
to rotation angles from horizontal.

For example: A queen on 'h8' (idx = 7) can move to the left (West) to each
of the indices 0, 1, 2, 3, 4, 5, 6, and cannot move right (East), right/up
(Northeast), up (North), up/left (Northwest), or down/right (Southeast)
because the piece is at the corner of the board. e.g.,

MOVES[7]["q"][0] = []  # empty because idx 7 is the right edge of the board
...
MOVES[7]["q"][4] = [6, 5, 4, 3, 2, 1, 0]  # sorted by distance from idx = 7
...
"""

from math import atan2
from copy import deepcopy

# Precalculate angles for index pairs that form legal moves
DIRECTIONS = [(1, 0), (1, 1), (0, 1), (-1, 1),  # straight lines
              (-1, 0), (-1, -1), (0, -1), (1, -1),
              (2, 1), (1, 2), (-1, 2), (-2, 1),  # knight moves
              (-2, -1), (-1, -2), (1, -2), (2, -1)
              ]
RAYS = [atan2(y, x) for x, y in DIRECTIONS]

# Legality tests of move direction for each piece type
TESTS = {'k': lambda r, dx, dy, d: dx <= 1 and dy <= 1,
         'q': lambda r, dx, dy, d: dx == 0 or dy == 0 or dx == dy,
         'n': lambda r, dx, dy, d: dx >= 1 and dy >= 1 and dx + dy == 3,
         'b': lambda r, dx, dy, d: dx == dy,
         'r': lambda r, dx, dy, d: dx == 0 or dy == 0,
         'p': lambda r, dx, dy, d: 1 < r < 8 and dx <= 1 and d == -1,
         'P': lambda r, dx, dy, d: 1 < r < 8 and dx <= 1 and d == 1
         }


def gen(idx):
    """ Generate the legal moves for all piece types from position idx """

    mlist = dict()
    for sym, test in TESTS.items():

        mlist[sym] = [list() for _ in xrange(8)]  # 8 possible directions

        # Sort the list of end points by distance from the starting point
        # to ensure the desired ouptut order
        for end in sorted(range(64), key=lambda x: abs(x - idx)):

            # row, change in column, and change in row of the start/end pair
            row = 8 - idx // 8
            d_x = (end % 8) - (idx % 8)
            d_y = (8 - end // 8) - row

            if idx == end or not test(row, abs(d_x), abs(d_y), d_y):
                continue

            angle = atan2(d_y, d_x)
            if angle in RAYS:
                # mod 8 shifts the ray index of knight moves
                mlist[sym][RAYS.index(angle) % 8].append(end)

        # Create references for other piece types
        if sym == "k":
            mlist["K"] = deepcopy(mlist["k"])
        elif sym.lower() != "p":
            mlist[sym.upper()] = mlist[sym]

    # Directly add double-space pawn opening moves
    if 8 <= idx <= 15:
        mlist["p"][6].append(idx + 16)
    elif 48 <= idx <= 55:
        mlist["P"][2].append(idx - 16)

    return mlist
