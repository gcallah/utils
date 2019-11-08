#!/bin/bash

# Variables
projectDir=
scriptDir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# should probably say something if directory already exists
if [[ -n $1 ]]; then
	mkdir -p "$1"
	projectDir=$1
else
	echo "must enter in directory name"
	exit 1
fi

echo "attempting to install python and pip"
sudo apt-get install python
sudo apt-get install python-pip

#should we use virtual environments
echo "attempting to install virtualenv & dependencies from requirements.txt"
sudo apt-get install virtualenv
sudo pip install -r requirements.txt

#Copies our generic project folder structure to project directory
cp -r $scriptDir/flash_project_layout/* $projectDir

#Append flask environment variables to ~/.bashrc
while IFS="=" read -r key val
do
	varExists="$( cat ~/.bashrc | grep "export $key=")"
	if [[ -z "${varExists}" ]]; then
		echo "Setting $key"
		echo "export $key=$val" >> ~/.bashrc
	fi
done < "$scriptDir/env.txt"