#!/bin/bash

# should probably say something if directory already exists

if [[ -n $1 ]]; then
	mkdir -p "$1"

else
	echo "must enter in directory name"
fi

echo "checking for python and pip"

sudo apt install python
sudo apt-get install python-pip

#should we use virtual environments
echo "checking for virtualenv"
sudo apt-get install virtualenv
sudo pip install -r requirements.txt


