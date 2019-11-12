#!/bin/sh

# initial cut at a django setup script

# run this in project dir:
django-admin startproject mysite_tmp
cp mysite_tmp/manage.py .
mv mysite_tmp/mysite/ mysite
rm -rf mysite_tmp
git add manage.py
git add mysite/*.py

