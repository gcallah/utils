#!/bin/bash

# python3 comes with venv preinstalled
# Note: python3 is the default for python version 3+
# sudo apt-get install python3-venv is needed prior

set -e

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

echo "Project Directory Name = $projectDir"

# We shouldn't clone if directory already exists, but we can still proceed with the script
if  [[ -d $projectDir ]]; then
    echo "Directory already exists; No need to create directory / clone."

elif [[ $directoryType == "github" ]]; then
    echo "We are going to clone $1"
    git clone $1 
	if [[ $? -ne 0 ]]; then
		echo "Trouble cloning $1, exiting script"
		exit 3;
	fi
else
    echo "Creating local repository: $projectDir"
    mkdir -p "$projectDir"
	git init $projectDir
fi

# Create a virtual environment for flask project
echo "Creating virtual environment in $projectDir"
python3 -m venv $projectDir

# Activate the virtual enviroment we just created, make sure script is being called with source
echo "Activating the virtual environment in $projectDir"
source $projectDir/bin/activate

# Copies our generic project folder structure to project directory
rsync -r --ignore-existing $scriptDir/project_layout/* $projectDir

# Copy the gitignore file (if doesn't already exit)
if [[ ! -f $projectDir/.gitignore ]]; then
	cp $scriptDir/project_layout/.gitignore $projectDir
fi

# Installing dependencies
echo "Attempting to install dependencies from requirements.txt within virtual environment"
pip install -r $projectDir/requirements.txt --no-cache-dir


