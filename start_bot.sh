#!/bin/bash
work_dir=$PWD
BOTCMD=$work_dir'/venv3/bin/python '$work_dir'/main.py'
export $(cat .env | xargs) && $BOTCMD
#pgrep -f "$BOTCMD" &>/dev/null || $BOTCMD
