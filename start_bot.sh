#!/bin/bash
work_dir=$PWD
#'/home/yaricp/projects/PyTGBots/publication_to_nets'
BOTCMD=$work_dir'/venv/bin/python3 '$work_dir'/main.py'
$BOTCMD
#pgrep -f "$BOTCMD" &>/dev/null || $BOTCMD
