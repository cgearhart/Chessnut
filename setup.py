from setuptools import setup

setup(
    name='Chessnut',
    version='0.1',  # TODO: https://pythonhosted.org/setuptools/setuptools.html#id7
    packages=['Chessnut'],

    author="Chris Gearhart",
    author_email="cgearhart@example.com",
    description="A basic chess model to imports/export FEN & finds moves.",
    long_description=open('README.md').read(),
    license="Unlicense",
    keywords="chess",
    url="https://github.com/cgearhart/Chessnut",
)
