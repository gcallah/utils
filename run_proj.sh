#!/bin/bash

if [ -z $1 ]
then
    echo "You must pass a directory name."
    exit 1
fi

cd $1
export PYTHONPATH=$(pwd)
