#!/usr/bin/env bash

# python -m unittest discover -v
coverage run  -m unittest discover; coverage html; open htmlcov/index.html
