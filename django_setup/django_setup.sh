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

# Refresh package cache
sudo apt update

# First install Python and pip if they are not already installed.
echo "Installing python if not installed..."
sudo apt-get install python3.6

echo "Installing pip if not installed..."
sudo apt-get install python-pip

# Install all requirements listed in requirements.txt.
echo "Installing requirements..."
sudo pip install -r requirements.txt

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