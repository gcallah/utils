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

if [ -z "$1" ]; then
    echo "Usage: static_setup.sh [repo]."
    exit 1
fi

# run sed on $1 to get dir name
export newdir=$(echo $1 | sed 's/.*\/\([^\/]*\)\.git/\1/')

echo "Dir name = $newdir"

export old_templs=$utilsdir/templates
export new_templs=$newdir/templates
export html_src_dir=$newdir/html_src

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
add_dir $newdir md

utilsdir=utils
if [ -n "$2" ]; then
    utilsdir=$2
fi
echo "utils dir is $utilsdir"

add_file $old_templs style.css $newdir
add_file $old_templs index.ptml $html_src_dir
add_file $old_templs about.ptml $html_src_dir
add_file $old_templs index.md $newdir/md
add_file $old_templs makefile $newdir
add_file $old_templs head.txt $new_templs
add_file $old_templs menu.txt $new_templs
add_file $old_templs logo.txt $new_templs
add_file "$utilsdir/docker" Dockerfile $newdir/docker
add_file "$utilsdir/docker" requirements.txt $newdir/docker

# make cloning utils an option!
cd $newdir; 
echo "We are going to add utils as a submodule."
git submodule add https://github.com/gcallah/utils
echo "We are going to update utils."
git submodule update --init

# install requirements
cd ..
echo "We are going to install requirements."
pip install -r $newdir/docker/requirements.txt
