#!/bin/sh

export PROJ_DIR=$(pwd)

python3 -m venv .venv

echo "export PYTHONPATH=$PROJ_DIR" >> .venv/bin/activate

echo "#/bin/sh

source .venv/bin/activate" > act.sh

chmod 755 act.sh

