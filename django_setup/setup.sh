#!/bin/bash
# Work in progress django setup script. Do not use this version.

set -e

# Variables
# If no argument passed to script, use "mysite" as default directory name.
DIRECTORY="mysite"
scriptDir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Check for input
if [[ -z $1 ]]; then
	echo "This script requires a github repo url or directory name"
	exit 1;
fi


# run sed on $1 to get dir name from git or get directory name
if [[ $1 == *"https://github.com/"* ]]; then
	DIRECTORY=$(echo $1 | sed 's/.*\/\([^\/]*\)\.git/\1/')
	directoryType="github"
else
	DIRECTORY=$1
	directoryType="local"
fi

echo "Project Directory Name = $DIRECTORY"

# We shouldn't clone if directory already exists, but we can still proceed with the script
if  [[ -d $DIRECTORY ]]; then
    echo "Directory already exists; No need to create directory / clone."

elif [[ $directoryType == "github" ]]; then
    echo "We are going to clone $1"
    git clone $1 
	if [[ $? -ne 0 ]]; then
		echo "Trouble cloning $1, exiting script"
		exit 3;
	fi
else
    echo "Creating local repository: $DIRECTORY"
    mkdir -p "$DIRECTORY"
	git init $DIRECTORY
fi

# No longer needed because of virtual env
# Refresh package cache
# sudo apt update

# Python and pip are now prerequisites to running the script.
# First install Python and pip if they are not already installed.
# echo "Installing python if not installed..."
# sudo apt-get install python3.6

# echo "Installing pip if not installed..."
# sudo apt-get install python-pip

# Create virtual environment. venv is a prerequisite.
echo "Creating virtual environment in $DIRECTORY..."
python3 -m venv $DIRECTORY

# Activate the virtual enviroment we just created, make sure script is being called with source
echo "Activating the virtual environment in $DIRECTORY..."
source $DIRECTORY/bin/activate

# Copies our generic project folder structure to project directory
# rsync -r --ignore-existing $scriptDir/project_layout/* $DIRECTORY

# Install all requirements listed in requirements.txt.
echo "Installing requirements..."
pip install -r $DIRECTORY/requirements/requirements.txt
pip install -r $DIRECTORY/requirements/requirements-dev.txt

# Set up django project.
echo "Setting up django project..."
if [ ! -d "$DIRECTORY" ]; then
    # Moves $DIRECTORY contents up one directory
    django-admin startproject "$DIRECTORY"
    mv "$DIRECTORY"/"$DIRECTORY"/* "$DIRECTORY"
    mv "$DIRECTORY"/manage.py .
    rm -rf "$DIRECTORY"/"$DIRECTORY"
    git add manage.py
    git add "$DIRECTORY"/*.py
    # Creates generic static directory
    # Should be turned into shell function that does mkdir, touch, and git add.
    mkdir -p "$DIRECTORY"/static/admin/css
    touch "$DIRECTORY"/static/admin/css/README.md
    git add "$DIRECTORY"/static/admin/css/README.md
    mkdir -p "$DIRECTORY"/static/admin/fonts
    mkdir -p "$DIRECTORY"/static/admin/img
    mkdir -p "$DIRECTORY"/static/admin/js
else
    echo "Directory /$DIRECTORY already exists."
fi

echo "Script complete."
