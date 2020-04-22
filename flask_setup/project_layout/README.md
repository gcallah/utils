# Boilerplate Flask Project
    This project was setup by initial_flask_setup.sh

    The script copies a generic flask project boilerplate structure and starter files to the destinated project directory

    Script properties: The script is idempotent

## Prerequisites
    1.) The user has the utils repo or at least the flask_setup folder in the utils repo on their machine.
    2.) The user has installed the required packages found in requirements.txt or requirements-dev.txt
    Or has at least installed flask-restplus.

## Script Behavior
    1.) Clones an existing github directory that user provides / Creates a local directory for the user
    2.) Then copies a generic flask project structure from the script directory into the project / target directory.

## Environment    
    ENV variables that are set (by run.sh using export command)
    1.) FLASK_APP, default val = source
    2.) FLASK_ENV, default val = development

    To change or add environment variables when running flask app
    1.) modify the "run.sh" to change or include new variables

## Running project / script
    To run setup script
    1.) run the following line in your shell: 
	./setup.sh <link to clone github repo / project directory name>

    To run flask project,
    1.) cd into the cloned git repo
    2.) run the "run.sh" script to start the flask app

## Available Build Targets (pre-packaged)
    1.) make tests
    2.) make lint
    3.) make pytests
