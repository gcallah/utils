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

echo "pip installing some packages..."

pip3 install gunicorn --user
pip3 install ipython --user
pip3 install matplotlib --user
pip3 install scipy --user
pip3 install numpy==1.19.0 --user
pip3 install flask --user
pip3 install werkzeug==0.16.1 --user
pip3 install flask_restplus --user
pip3 install flask-cors --user
pip3 install propargs==0.0.16 --user
pip3 install seaborn --user
pip3 install asyncio --user
pip3 install aiohttp --user
pip3 install requests --user

echo "pip installing dev packages..."

pip3 install jupyter --user
pip3 install flake8 --user
pip3 install coverage --user
pip3 install nose --user
pip3 install urllib3 --user

echo "set up is now complete!"
