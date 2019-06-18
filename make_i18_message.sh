#!/bin/bash
work_dir=$PWD
args=("$@")
echo $args
find . -path ./venv3 -prune -o -path ./.git -prune -o -name \*.py -exec ./prepare_po_file.sh {} \;
