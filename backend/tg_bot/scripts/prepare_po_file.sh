#!/bin/bash
#if [[ "$OSTYPE" == "linux-gnu" ]]; then
#        GETTEXT_CMD="gettext"
#elif [[ "$OSTYPE" == "darwin"* ]]; then
#        GETTEXT_CMD="xgettext"
#elif [[ "$OSTYPE" == "cygwin" ]]; then
#        GETTEXT_CMD="gettext"
#elif [[ "$OSTYPE" == "msys" ]]; then
#        GETTEXT_CMD="gettext"
#elif [[ "$OSTYPE" == "win32" ]]; then
#        GETTEXT_CMD="gettext"
#elif [[ "$OSTYPE" == "freebsd"* ]]; then
#        GETTEXT_CMD="gettext"
#else
GETTEXT_CMD="xgettext"
#fi

work_dir=$PWD
LANG_DIR="lang/ru/LC_MESSAGES"
args=("$@")
echo $args
#IFS="/" read -ra ADDR <<< "$args"; echo ${ADDR[-1]};
file_name=${args##*/}
file_name=${file_name//'.py'/''}
#echo $file_name

$GETTEXT_CMD -o $LANG_DIR/prepare_$file_name.pot $args
#echo " PATH  - $LANG_DIRprepare_$file_name.pot"
msgmerge -U --no-fuzzy-matching --backup=off $LANG_DIR/messages.po $LANG_DIR/prepare_$file_name.pot
