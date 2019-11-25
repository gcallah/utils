#!/bin/sh
# Work in progress django setup script. Do not use this version.

# Variables
# If no argument passed to script, use "mysite" as default directory name.
DIRECTORY="mysite"

# Use first argument as directory name
if [ ! -z "$1" ]
    then
        DIRECTORY="$1"
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
# rsync -r --ignore-existing $scriptDir/project_layout/* $projectDir

# Install all requirements listed in requirements.txt.
echo "Installing requirements..."
pip install -r requirements/requirements.txt
pip install -r requirements/requirements-dev.txt

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
    mkdir -p "$DIRECTORY"/static/admin/css
    mkdir -p "$DIRECTORY"/static/admin/fonts
    mkdir -p "$DIRECTORY"/static/admin/img
    mkdir -p "$DIRECTORY"/static/admin/js
else
    echo "Directory /$DIRECTORY already exists."
fi

echo "Script complete."