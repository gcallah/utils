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
    # Control will enter here if $DIRECTORY doesn't exist.
    django-admin startproject mysite_tmp
    cp mysite_tmp/manage.py .
    mv mysite_tmp/mysite_tmp/ mysite
    rm -rf mysite_tmp
    git add manage.py
    git add mysite/*.py
else
    echo "Directory /mysite already exists."
fi

echo "Script complete."