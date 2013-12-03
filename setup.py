
from setuptools import setup
from pkg_resources import resource_string


# https://pythonhosted.org/setuptools/setuptools.html#id7
setup(
    name='Chessnut',
    version='0.2.8',
    packages=['Chessnut'],

    author="Chris Gearhart",
    author_email="chris@gearley.com",
    description="A basic chess model to imports/export FEN & finds moves.",
    long_description=resource_string(__name__, "README.md"),
    license="UNLICENSE",
    keywords="chess",
    url="https://github.com/cgearhart/Chessnut",
)
