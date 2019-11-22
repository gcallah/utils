#!/bin/bash

# python3 comes with venv preinstalled
# Note: python3 is the default for python version 3+

# Variables
scriptDir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Check for input
if [[ -z $1 ]]; then
	echo "This script requires a github repo url or directory name"
	exit 1;
fi
# run sed on $1 to get dir name from git or get directory name
if [[ $1 == *"https://github.com/"* ]]; then
	projectDir=$(echo $1 | sed 's/.*\/\([^\/]*\)\.git/\1/')
	directoryType="github"

else
	projectDir=$1
	directoryType="local"
fi

set -e

echo "Project Directory Name = $projectDir"

if [[ -d $projectDir ]]; then
    echo "Directory already exists; not cloning."
    exit 2;

elif [[ $directoryType == "github" ]]; then
    echo "We are going to clone $1"
    git clone $1 
	if [[ $? -ne 0 ]]; then
		echo "Trouble cloning $1, exiting script"
		exit 3;
	fi
else
    echo "Creating local repository: $1"
    mkdir -p "$1"
    cp -r $scriptDir/flask_project_layout/* $projectDir
fi

# Install Virtual Environment. This is a requirement
# Might need to have this as a preqrequiste to using the script
# echo "Installing python3-venv. Requires sudo"
# sudo apt-get install python3-venv

# Create a virtual environment for flask project
echo "Creating virtual environment in $projectDir"
python3 -m venv $projectDir

# Activate the virtual enviroment we just created, make sure script is being called with source
echo "Activating the virtual environment in $projectDir"
source $projectDir/bin/activate

# This is not needed since the virtual environment created has pip installed by default
# sudo apt-get update
# sudo apt-get install python-pip

# Copies our generic project folder structure to project directory
rsync -r --ignore-existing $scriptDir/flask_project_layout/* $projectDir

# Installing dependencies
echo "Attempting to install dependencies from requirements.txt within virtual environment"
pip install -r $projectDir/requirements.txt --no-cache-dir

# Append flask environment variables to ~/.bashrc
# while IFS="=" read -r key val
# do
# 	varExists="$( cat $projectDir/bin/activate | grep "export $key=")"
# 	if [[ -z "${varExists}" ]]; then
# 		echo "Setting $key"
# 		echo "export $key=$val" >> $projectDir/bin/activate
# 	fi
# done < "$projectDir/env.txt"


