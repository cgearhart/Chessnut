
from setuptools import setup
import os

long_description = 'A simple chess model in pure Python'
if os.path.exists('README.txt'):
    long_description = open('README.txt').read()

# https://pythonhosted.org/setuptools/setuptools.html#id7
setup(
    name='Chessnut',
    version='0.2.13',
    packages=['Chessnut'],

    author="Chris Gearhart",
    author_email="chris@gearley.com",
    description="A basic chess model to imports/export FEN & finds moves.",
    long_description=long_description,
    license="UNLICENSE",
    keywords="chess",
    url="https://github.com/cgearhart/Chessnut",
)
