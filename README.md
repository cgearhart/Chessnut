# Chessnut
__Chessnut__ is a simple chess board model written in Python. __Chessnut__ is *not* a chess engine -- it has no AI to play games, and it has no GUI. It is a simple package that can import/export games in [Forsyth-Edwards Notation](http://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation) (FEN), generate a list of legal moves for the current board position, intelligently validate & apply moves (including *en passant*, *castling*, etc.), and keep track of the game with a history of both moves and corresponding FEN representation.

__Chessnut__ is not written for speed, it is written for simplicity (there are only two real classes, and only about 200 lines of code). By adding a custom move evaluation function, __Chessnut__ could be used as a chess engine. The simplicity of the model lends itself well to studying the construction of a chess engine without worrying about implementing a chess model, or to easily find the set of legal moves for either player on a particular chess board for use in conjunction with another chess application.

## Installation

### Virualenv
__Chessnut__ can be used as a module within your project or it can be installed on your system as a package. If you're going to install it as a package, you should consider using [Virtualenv](http://www.virtualenv.org/en/latest/) to manage your python environment. With virtualenv installed, creating a new project environment is easy. From your terminal shell:

```
~$ mkdir ~/project
~/$ cd project
~/project$ virtualenv env
~/project$ source env/bin/activate
(env):~/project$
```

From here you can use `pip` or `setup.py` to install the package and it will be restricted to the copy of python in the `env` directory. You can leave the virtual environment by typing `deactivate` in the terminal, and restart the environment with `source env/bin/activate`.


### PIP
`pip` is the easiest way to install __Chessnut__. It can be installed directly from the [pypi](https://pypi.python.org/) [package](https://pypi.python.org/pypi/Chessnut):

`pip install Chessnut`

Upgrading to the latest version can be performed with the `-U` flag:

`pip install -U Chessnut`

Or from the [github](https://github.com/) [repository](https://github.com/cgearhart/Chessnut.git):

`pip install git+https://github.com/cgearhart/Chessnut.git`

### Setup.py
If you prefer, you can install __Chessnut__ manually with `setup.py`. After downloading the source files to a local directory (and setting up a `virtualenv`), switch into the project directory and run `setup.py`:

`python -m setup.py install`

(Note: To install the package globally you may have to use the `sudo` command.)

### As a Module
Finally, __Chessnut__ is also a standalone module, so if you place the `Chessnut` directory within your project folder, you don't need to install the package, you can just import the module as usual. (Using one of the package versions--particularly PIP--is still recommended as a way to create separation between your code and the __Chessnut__ package, so that you don't have to worry about merging your changes into future upgrades of __Chessnut__.

```
from Chessnut import Game

...

*<your code>*
```

## Testing
Unit tests can be run with the `test.sh` shell script which launches the [`coverage.py`](http://nedbatchelder.com/code/coverage/) framework as configured in `.coveragerc`, or you can use the standard [unittest](http://docs.python.org/2/library/unittest.html) framework via `python -m unittest discover`. If you install the `pylint` package, you can run the checker with default options using `pylint --ignore=tests Chessnut`.


## Using Chessnut
There are only two real classes in the __Chessnut__ package: `Board` and `Game`. (There is also a [namedtuple](http://docs.python.org/2/library/collections.html#collections.namedtuple), `State`, which creates a class, and another class, `InvalidMove`--a subclass of `Exception`, used to avoid generic try/except statements). `Board` is only used internally by `Game` to keep track of pieces and perform string formatting to and from FEN notation, so `Game` should be the only class you need to import. After installing the Chessnut package, you can import and use it as you would expect:

```
from Chessnut import Game

chessgame = Game()
print(chessgame)  # 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'

print(chessgame.get_moves())
"""
['a2a3', 'a2a4', 'b2b3', 'b2b4', 'c2c3', 'c2c4', 'd2d3', 'd2d4', 'e2e3', 
 'e2e4', 'f2f3', 'f2f4', 'g2g3', 'g2g4', 'h2h3', 'h2h4', 'b1c3', 'b1a3', 
 'g1h3', 'g1f3']
"""

chessgame.apply_move('e2e4')  # succeeds!
print(chessgame)  # 'rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1'

chessgame.apply_move('e2e4')  # fails! (raises InvalidMove exception)
```
