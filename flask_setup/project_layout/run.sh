#!/bin/bash

# This script runs the flask project

source ./bin/activate

export FLASK_APP=source
export FLASK_ENV=development

flask run