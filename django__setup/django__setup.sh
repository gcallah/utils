#!/bin/sh
# Work in progress django setup script. Do not use this version.

# Variables
DIRECTORY="mysite"

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
    # Moves mysite contents up one directory
    django-admin startproject mysite
    mv mysite/mysite/* mysite
    mv mysite/manage.py .
    rm -rf mysite/mysite
    git add manage.py
    git add mysite/*.py
else
    echo "Directory /mysite already exists."
fi

echo "Script complete."