#!/bin/bash
work_dir=$PWD
args=("$@")
echo $args
$PWD/venv3/bin/python $PWD/store/migrations/$args
