#!/bin/bash
work_dir=$PWD
LANG_DIR="lang/ru/LC_MESSAGES"
args=("$@")
echo $args
#IFS="/" read -ra ADDR <<< "$args"; echo ${ADDR[-1]};
file_name=${args##*/}
file_name=${file_name//'.py'/''}
#echo $file_name
xgettext -o $LANG_DIR/prepare_$file_name.pot $args
#echo " PATH  - $LANG_DIRprepare_$file_name.pot"
msgmerge -U --no-fuzzy-matching --backup=off $LANG_DIR/messages.po $LANG_DIR/prepare_$file_name.pot
