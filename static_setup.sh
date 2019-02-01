#!/bin/sh

# script to create a static website served by e.g. GitHub pages.
# we need the name of the git repo to clone as $1

# run sed on $1 to get dir name
newdir=$(echo $1 | sed 's/.*\/\([A-Za-z0-9]*\)\.git/\1/')

echo "Dir name = $newdir"

echo "going to clone $1"
git clone $1 

echo "we are going to try to make: $newdir/html_src "
mkdir $newdir/html_src
mkdir $newdir/docker 
mkdir $newdir/templates
mkdir $newdir/tests

utilsdir=utils
if [ -n "$2" ]; then
    utilsdir=$2
fi
echo "utils dir is $utilsdir"

cp $utilsdir/style.css $newdir/style.css
cp $utilsdir/templates/index.ptml $newdir/html_src/index.ptml
cp $utilsdir/templates/makefile $newdir/makefile 
cp $utilsdir/templates/head.txt $newdir/templates/head.txt
cp $utilsdir/templates/menu.txt $newdir/templates/menu.txt
cp $utilsdir/templates/logo.txt $newdir/templates/logo.txt

cd $newdir; git submodule add https://github.com/gcallah/utils
