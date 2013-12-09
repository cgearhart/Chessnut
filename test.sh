#!/usr/bin/env bash

usage() {
    echo `basename $0`: ERROR: $* 1>&2
    echo usage: `basename $0` '[--pylint | --unittest]' 1>&2
    exit 1
}

while :
do
    case "$1" in
    --pylint) pylint --ignore=tests Chessnut;;
    --unittest) coverage run  -m unittest discover; coverage html; open htmlcov/index.html
;;
    -*) usage "bad argument $1";;
    *) break;;
    esac
    shift
done