#!/bin/sh

# script to create a static website served by e.g. GitHub pages.
# we need the name of the git repo to clone as $1

add_file()
{
    cp $1/$2 $3/$2
    cd $3; git add $2; cd -
}

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

add_file $utilsdir style.css $newdir
add_file "$utilsdir/templates" index.ptml "$newdir/html_src"
add_file "$utilsdir/templates" makefile "$newdir"
add_file "$utilsdir/templates" head.txt "$newdir/templates"
add_file "$utilsdir/templates" menu.txt "$newdir/templates"
add_file "$utilsdir/templates" logo.txt "$newdir/templates"

cd $newdir; git submodule add https://github.com/gcallah/utils
