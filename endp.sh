#!/bin/sh

cat $1 | sed 's/\(.*\)<\/p>/\1~<\/p>~/' | tr "~" "\n"
