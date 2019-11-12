# Boilerplate Flask Project
'''
    This project was setup by initial_flask_setup.sh

    The script copies a generic flask project boilerplate structure and starter files to the destinated project directory

    Script properties: The script is idempotent

    Prerequisites:
    1.) The user has the utils repo or at least the flask_setup folder in the utils repo on their machine.
    
    To execute this script:
    1.) cd into the project directory
    2.) Run bash initial_flask_setup.sh (filename)
    
    Script Behavior:
    1.) Creates flask project directory (target directory) indicated by the user.
    2.) Installs python and pip if not on machine
    3.) Installs virtualenv and any flask dependencies from requirements.txt
    4.) Then copies a generic flask project structure from the script directory into the project / target directory.
        - This comes with a default setup that allows you to immediately run a development flask server to test the setup
          by following the directions to run the flask project
    5.) Setups the flask environment variables if they haven't been set. It writes the environment to bashrc file.


    ENV variables that were set
    1.) FLASK_APP, default val = flaskr
    2.) FLASK_ENV, default val = development

    To run flask project,
    1.) cd into project directory
    2.) run "flask run" to start the development server
'''
