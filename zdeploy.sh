#!/bin/bash
work_dir=$PWD
args=("$@")
git checkout master
git branch
git merge dev
git push
git checkout dev
git branch
