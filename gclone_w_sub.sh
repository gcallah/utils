#!/bin/sh

git clone $1
# here we want to extract just the name of the repo from the entire URL:
cd $1
git submodule init
git submodule update
