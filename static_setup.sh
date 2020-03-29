#!/bin/sh

# script to create a static website served by e.g. GitHub pages.
# we need the name of the git repo to clone as $1

add_file()
{
    if [ -f $3/$2 ]; then
        echo "$3/$2 exists."
    else
        echo "We are going to add" $2
        cp $1/$2 $3/$2
        cd $3; git add $2; cd - > /dev/null 
    fi
}

add_dir()
{
    if [ -d $1/$2 ]; then
        echo "$1/$2 exists."
    else
        echo "We are going to make directory" $1/$2
        mkdir $1/$2
        # we have to add a file to dir or git won't keep it:
        cd $1/$2; touch .gitignore; git add .gitignore; cd - > /dev/null
    fi
}

if [[ -z "$1" ]]; then
    echo "Usage: static_setup.sh [repo]."
    exit 1
fi

# run sed on $1 to get dir name
newdir=$(echo $1 | sed 's/.*\/\([^\/]*\)\.git/\1/')

echo "Dir name = $newdir"

if [ -d $newdir ]; then
    echo "Directory already exists; not cloning."
else
    echo "We are going to clone $1"
    git clone $1 
fi

add_dir $newdir html_src
add_dir $newdir templates
add_dir $newdir docker
add_dir $newdir tests
add_dir $newdir markdown

utilsdir=utils
if [ -n "$2" ]; then
    utilsdir=$2
fi
echo "utils dir is $utilsdir"

add_file "$utilsdir/templates" style.css $newdir
add_file "$utilsdir/templates" index.ptml $newdir/html_src
add_file "$utilsdir/templates" about.ptml $newdir/html_src
add_file "$utilsdir/templates" makefile $newdir
add_file "$utilsdir/templates" head.txt $newdir/templates
add_file "$utilsdir/templates" menu.txt $newdir/templates
add_file "$utilsdir/templates" logo.txt $newdir/templates
add_file "$utilsdir/docker" Dockerfile $newdir/docker
add_file "$utilsdir/docker" requirements.txt $newdir/docker

# make cloning utils an option!
cd $newdir; 
echo "We are going to add utils as a submodule."
git submodule add https://github.com/gcallah/utils
echo "We are going to update utils."
git submodule update --init

