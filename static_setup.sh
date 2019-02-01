#!/bin/sh

# script to create a static website served by e.g. GitHub pages.

# we need the name of the git repo to clone as $1

# run sed on $1 to get dir name
dirname=$(echo $1 | sed 's/.*\/\([A-Za-z0-9]*\)\.git/\1/')
#dirname=OOP2
echo $dirname
echo "Dir name = $dirname"

mkdir html_src
mkdir docker 
mkdir templates
mkdir tests

cp utils/templates/index.ptml html_src/index.ptml
cp utils/templates/makefile makefile 
cp utils/templates/head.txt templates/head.txt
cp utils/templates/menu.txt templates/menu.txt
cp utils/templates/logo.txt templates/logo.txt

git submodule add https://github.com/gcallah/utils