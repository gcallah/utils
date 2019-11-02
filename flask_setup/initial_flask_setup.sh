#!/bin/bash

# Variables
projectDir=
scriptDir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# ================= Helper Functions
# copies file from script directory to a destination
copyFileToDir() 
{
	cp $scriptDir/$1 $2
}

# should probably say something if directory already exists
if [[ -n $1 ]]; then
	mkdir -p "$1"
	projectDir=$1
else
	echo "must enter in directory name"
	exit 1
fi

echo "attempting to install python and pip"
sudo apt-get install python3
sudo apt-get install python3-pip

#should we use virtual environments
echo "attempting to install virtualenv & dependencies from requirements.txt"
sudo apt-get install virtualenv
sudo pip install -r requirements.txt

#Copies our generic project folder structure to project directory
cp $scriptDir/flash_project_layout/* $projectDir