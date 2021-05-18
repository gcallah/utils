# Django Project Setup

This script sets up a generic django project.

**Prerequisites**
1) The user has the utils repo or at least the django_setup folder in the utils repo on their machine.
2) The user has python 3.x preinstalled on their machine
3) The user has python3-venv preinstalled on their machine

**To run this script**
2) Run `./path_to_this_folder/setup.sh <link to github repo / project directory name>`
    - If a github repo is used, no existing files in the repo will be overwritten
    - If a project directory name is used, the script will initialize a local git repo

**Script Behavior:**
1) Clones an existing github repo from a provided url or creates a local directory with the provided name.
2) Creates a python virtual environment with the project name.
3) The script will install all dependencies listed in `requirements.txt`
4) If `/mysite` directory does not already exist, starts a new django project. Moves `/mysite` contents up one directory level. Creates generic `/static` folder structure.
Resulting file structure:
```
project/
    manage.py
    mysite/
        static/
            admin/
                css/
                fonts/
                img/
                js/
        __init__.py
        settings.py
        urls.py
        wsgi.py
```
**To run the django project**
1) cd into project directory
2) Run `python manage.py runserver`
    - By default, `runserver` starts the server on port 8000.
    - To change the port: `python manage.py runserver <port number>`
3) Visit `http://127.0.0.1:8000/` with your web browser.

**To quit the server**
1) `Ctrl-C`
