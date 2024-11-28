
from setuptools import setup, find_packages
import os

long_description = '''\
Chessnut is a simple chess board model written in Python. Chessnut is not a chess engine – it has no AI to play games, and it has no GUI. It is a simple package that can import/export games in Forsyth-Edwards Notation (FEN), generate a list of legal moves for the current board position, intelligently validate & apply moves (including en passant, castling, etc.), and keep track of the game with a history of both moves and corresponding FEN representation.

Chessnut is not written for speed, it is written for simplicity (there are only two real classes, and only about 200 lines of code). By adding a custom move evaluation function, Chessnut could be used as a chess engine. The simplicity of the model lends itself well to studying the construction of a chess engine without worrying about implementing a chess model, or to easily find the set of legal moves for either player on a particular chess board for use in conjunction with another chess application.
'''

# https://pythonhosted.org/setuptools/setuptools.html#id7
setup(
    name='Chessnut',
    version='0.0.0',  # This will be updated automatically by the GitHub Action
    packages=find_packages(),
    author="Chris Gearhart",
    author_email="chris@gearley.com",
    description="A basic chess model to imports/export FEN & finds moves.",
    long_description=long_description,
    license="UNLICENSE",
    keywords="chess",
    url="https://github.com/cgearhart/Chessnut",
)
