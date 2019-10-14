#!/bin/sh

# script to create a static website served by e.g. GitHub pages.
# we need the name of the git repo to clone as $1

add_file()
{
    echo "we are going to add" $2
    cp $1/$2 $3/$2
    cd $3; git add $2; cd -
}

add_dir()
{
    echo "we are going to make directory:" $1
    mkdir $1
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

[ -d $newdir/html_src ] && echo "$newdir/html_src exists." || add_dir $newdir/html_src
[ -d $newdir/templates ] && echo "$newdir/templates exists." || add_dir $newdir/templates
[ -d $newdir/docker ] && echo "$newdir/docker exists." || add_dir $newdir/docker
[ -d $newdir/tests ] && echo "$newdir/tests exists." || add_dir $newdir/tests

utilsdir=utils
if [ -n "$2" ]; then
    utilsdir=$2
fi
echo "utils dir is $utilsdir"

[ -f $newdir/style.css ] && echo "style.css exists." || add_file "$utilsdir/templates" style.css $newdir
[ -f $newdir/html_src/index.ptml ] && echo "index.ptml exists." || add_file "$utilsdir/templates" index.ptml "$newdir/html_src"
[ -f $newdir/html_src/about.ptml ] && echo "about.ptml exists." || add_file "$utilsdir/templates" about.ptml "$newdir/html_src"
[ -f $newdir/makefile ] && echo "makefile exists." || add_file "$utilsdir/templates" makefile "$newdir"
[ -f $newdir/templates/head.txt ] && echo "head.txt exists." || add_file "$utilsdir/templates" head.txt "$newdir/templates"
[ -f $newdir/templates/menu.txt ] && echo "menu.txt exists." || add_file "$utilsdir/templates" menu.txt "$newdir/templates"
[ -f $newdir/templates/logo.txt ] && echo "logo.txt exists." || add_file "$utilsdir/templates" logo.txt "$newdir/templates"
[ -f $newdir/docker/Dockerfile ] && echo "Dockerfile exists." || add_file "$utilsdir/docker" Dockerfile "$newdir/docker"
[ -f $newdir/docker/requirements.txt ] && echo "requirements.txt exists." || add_file "$utilsdir/docker" requirements.txt "$newdir/docker"

# make cloning utils an option!
cd $newdir; git submodule add https://github.com/gcallah/utils
