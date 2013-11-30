
from setuptools import setup
from pkg_resources import Requirement, resource_filename

filename = resource_filename(Requirement.parse("Chessnut"), "README.md")


# https://pythonhosted.org/setuptools/setuptools.html#id7
setup(
    name='Chessnut',
    version='0.2.6',
    packages=['Chessnut'],

    author="Chris Gearhart",
    author_email="chris@gearley.com",
    description="A basic chess model to imports/export FEN & finds moves.",
    long_description=open(filename).read(),
    license="UNLICENSE",
    keywords="chess",
    url="https://github.com/cgearhart/Chessnut",
)
