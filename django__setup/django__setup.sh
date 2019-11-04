#!/bin/sh
# Work in progress django setup script. Do not use this version.

# First install Python and pip if they are not already installed.
echo "Installing python if not installed..."
sudo apt install python

echo "Installing pip if not installed..."
sudo apt-get install python-pip

# Install all requirements listed in requirements.txt.
echo "Installing requirements..."
sudo pip install -r requirements.txt

# Set up django project.
echo "Setting up django project..."
django-admin startproject mysite_tmp
cp mysite_tmp/manage.py .
mv mysite_tmp/mysite_tmp/ mysite
rm -rf mysite_tmp
git add manage.py
git add mysite/*.py

echo "Script complete."