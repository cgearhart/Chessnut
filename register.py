import pandoc
import os

pandoc.core.PANDOC_PATH = '/usr/local/bin/pandoc'

doc = pandoc.Document()
readme = open('README.md').read()
doc.markdown = readme
with open('README.txt', 'w+') as f:
    f.write(doc.rst)
    f.close()
os.system("python setup.py register")
os.remove('README.txt')
os.system("python setup.py sdist upload")
