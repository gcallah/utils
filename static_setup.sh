#!/bin/sh

# script to create a static website served by e.g. GitHub pages.

# we need the name of the git repo to clone as $1

# run sed on $1 to get dir name
dirname=$(echo $1 | sed 's/.*\/\([A-Za-z0-9]*\)\.git/\1/')
#dirname=OOP2
echo $dirname
echo "Dir name = $dirname"
