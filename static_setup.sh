#!/bin/sh

# script to create a static website served by e.g. GitHub pages.
# we need the name of the git repo to clone as $1

add_file()
{
    cp $1/$2 $3/$2
    cd $3; git add $2; cd -
}

if [[ -z "$1" ]]
then
    echo "Usage: static_setup.sh [repo]."
    exit 1
fi

# run sed on $1 to get dir name
newdir=$(echo $1 | sed 's/.*\/\([^\/]*\)\.git/\1/')

echo "Dir name = $newdir"

if [ -d $newdir ]
then
    echo "Directory already exists; not cloning."
else
    echo "going to clone $1"
    git clone $1 
fi

echo "We are going to add utils as a submodule."
git submodule add https://github.com/gcallah/utils.git

if [ -d "$newdir/html_src" ]
then
    echo "$newdir/html_src exists."
else
    echo "we are going to try to make: $newdir/html_src "
    mkdir $newdir/html_src
fi
mkdir $newdir/docker 
mkdir $newdir/templates
mkdir $newdir/tests

utilsdir=utils
if [ -n "$2" ]; then
    utilsdir=$2
fi
echo "utils dir is $utilsdir"

add_file "$utilsdir/templates" style.css $newdir
add_file "$utilsdir/templates" index.ptml "$newdir/html_src"
add_file "$utilsdir/templates" about.ptml "$newdir/html_src"
add_file "$utilsdir/templates" makefile "$newdir"
add_file "$utilsdir/templates" head.txt "$newdir/templates"
add_file "$utilsdir/templates" menu.txt "$newdir/templates"
add_file "$utilsdir/templates" logo.txt "$newdir/templates"

# make cloning utils an option!
cd $newdir; git submodule add https://github.com/gcallah/utils
