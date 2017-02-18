#!/bin/sh

cat $1 | sed 's/<p class="normal">\(.*\)/~<p>~\1/' | tr "~" "\n"
