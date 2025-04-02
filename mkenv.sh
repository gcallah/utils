#!/bin/sh

export PROJ_DIR=$(pwd)
export PROJ_NAME=${PWD##*/}

export VENV_NAME="$PROJ_NAME-venv"
echo "Creating $VENV_NAME"

python3 -m venv $VENV_NAME

echo "export PYTHONPATH=$PROJ_DIR" >> $VENV_NAME/bin/activate

echo "#/bin/bash
source $VENV_NAME/bin/activate" > act.sh

chmod 755 act.sh

