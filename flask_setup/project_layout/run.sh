#!/bin/bash

# This script runs the flask project
# You should run this in the project directory

#source ./bin/activate

export FLASK_APP=source
export FLASK_ENV=development

flask run