#!/usr/bin/env bash

indra_dir=IndraABM

if [ -d "$indra_dir" ]; then 
    echo "$indra_dir already exists."
else 
    echo "Cloning $indra_dir directory..."
    git clone https://github.com/TandonDevOps/IndraABM.git
fi

echo "setting up INDRA_HOME"

if grep -q "INDRA_HOME" ~/.bashrc ; then
   echo "INDRA_HOME is already setup."
else 
   echo "export INDRA_HOME=\"$HOME/$indra_dir\"" >> ~/.bashrc
fi

echo "setting up PYTHONPATH"

if grep -q "PYTHONPATH" ~/.bashrc ; then
    echo "PYTHONPATH is already setup."
else 
    echo "export PYTHONPATH=$INDRA_HOME" >> ~/.bashrc
fi

cd $indra_dir 

echo "Installing requirements"
pip3 install -r requirements.txt --user 

echo "Installing dev requirements"
pip3 install -r requirements-dev.txt --user

echo "set up is now complete!"
