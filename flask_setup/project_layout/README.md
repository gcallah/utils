# Boilerplate Flask Project
    This project was setup by initial_flask_setup.sh

    The script copies a generic flask project boilerplate structure and starter files to the destinated project directory

    Script properties: The script is idempotent

## Prerequisites
    1.) The user has the utils repo or at least the flask_setup folder in the utils repo on their machine.
    2.) The user has python 3.x preinstalled on their machine
    3.) The user has python3-venv preinstalled on their machine

## Script Behavior
    1.) Clones an existing github directory that user provides / Creates a local directory for the user
    2.) Creates a python virtual environment with the project name, extracted from the github URL / provided in directory name
    3.) Then copies a generic flask project structure from the script directory into the project / target directory.
        - This comes with a default setup that allows you to immediately run a development flask server to test the setup
          by following the directions to run the flask project
    4.) Installs flask dependencies from requirements.txt

## Environment
    The flask project runs within a virtual environment
    
    ENV variables that are set
    1.) FLASK_APP, default val = source
    2.) FLASK_ENV, default val = development

    To change or add environment variables for virtual environment
    1.) modify the "run.sh" to change or include new variables

## Running project / script
    To run setup script
    1.) run the following line in your shell: 
	source ./initial_flask_setup <link to clone github repo / project directory name>

    To run flask project,
    1.) cd into the cloned git repo
    2.) run the "run.sh" script to start the virtual environment and flask app

    To activate virtual environment
    Run "source ./bin/activate" from the root of the project directory

    To deactivate virtual environment
    Run "deactivate" in the terminal

## Available Build Targets (pre-packaged)
    1.) make tests
    2.) make lint
    3.) make pytests
