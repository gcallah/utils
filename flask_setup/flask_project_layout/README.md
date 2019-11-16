# Boilerplate Flask Project
    This project was setup by initial_flask_setup.sh

    The script copies a generic flask project boilerplate structure and starter files to the destinated project directory

    Script properties: The script is idempotent

## Prerequisites
    1.) The user has the utils repo or at least the flask_setup folder in the utils repo on their machine.
    2.) The user has python 3.x preinstalled on their machine
    3.) The user has python3-venv preinstalled on their machine

## Script Behavior
    1.) Clones existing directory that user inputs
    2.) Creates a python virtual environment with the project name, extracted from the github URL
    3.) Then copies a generic flask project structure from the script directory into the project / target directory.
        - This comes with a default setup that allows you to immediately run a development flask server to test the setup
          by following the directions to run the flask project
    4.) Installs flask dependencies from requirements.txt
    5.) Writes into bin/activate within project directory to setup environment variables

## Environment
    The flask project runs within a virtual environment
    
    ENV variables that are set
    1.) FLASK_APP, default val = source
    2.) FLASK_ENV, default val = development

    To change or add environment variables for virtual environment
    1.) cd into bin/app within your project directory
    2.) modified the "activate" file acccordingly by inserting "export <var_name>=<var_value>"
        Warning: this file is used by venv to setup the virtual environment when it is activated.
		Do not delete or heavily modify code that you are unsure of.

## Running project / script
    To run script
    1.) run the following line in your shell: 
	source ./initial_flask_setup <link to clone github repo>

    To run flask project,
    1.) cd into the cloned git repo
    2.) activate the virtual environment, "source ./bin/activate"
    3.) run "flask run" to start the development server

    To deactivate virtual environment
    Run "deactivate"
