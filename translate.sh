#!/bin/bash
work_dir=$PWD
args=("$@")
echo $args
find lang -name \*.po -execdir msgfmt messages.po -o messages.mo \;
#msgfmt lang/ru/LC_MESSAGES/messages.po -o lang/ru/LC_MESSAGES/messages.mo
