
from setuptools import setup, find_packages
import os

long_description = 'A simple chess model in pure Python'
if os.path.exists('README.md'):
    long_description = open('README.md', 'r').read()

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
