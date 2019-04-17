#!/bin/bash
work_dir=$PWD
BOTCMD=$work_dir'/venv/bin/python3 '$work_dir'/main.py'
$BOTCMD
#pgrep -f "$BOTCMD" &>/dev/null || $BOTCMD
