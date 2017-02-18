#!/bin/sh

cat $1 | sed 's/<p class="head\([0-9]\)">\(.*\)<\/p>/~<h\1>~\2~<\/h\1>~/' | tr "~" "\n"
