 #!/usr/bin/env bash

echo "Please enter the clone URL of your GitHub repo:"

read repo_url 

basename=$(basename $repo_url)
dir_name=${basename%.*}
makefile_dir="https://raw.githubusercontent.com/gcallah/utils/master/flask_setup/project_layout/makefile"

echo "Cloning $dir_name..."

if [ -d "$dir_name" ]; then
    echo "$dir_name already exists."
else
    echo "Cloning $dir_name directory..."
    git clone $repo_url
fi

echo "Changing directory to $dir_name"
cd $dir_name 


if [ -f "requirements.txt" ]; then 
    echo "requirements.txt already exists."
else 
    echo "Creating requirements.txt"
    touch requirements.txt
    echo "flask" > requirements.txt
    echo "flask_restx" >> requirements.txt
    echo "flask-sqlalchemy" >> requirements.txt
    echo "gunicorn" >> requirements.txt
fi


echo "Creating requirements-dev.txt"

if [ -f "requirements-dev.txt" ]; then 
    echo "requirements-dev.txt already exists."
else 
    touch requirements-dev.txt
    echo "flake8" > requirements-dev.txt
    echo "nose" >> requirements-dev.txt
    echo "coverage" >> requirements-dev.txt
fi


echo "Creating a makefile"

if [ -f "makefile" ]; then 
    echo "Makefile already exists."
else 
    curl $makefile_dir > makefile 
fi

echo "Installing requirements"
pip3 install -r requirements.txt --user

echo "Installing dev requirements"
pip3 install -r requirements-dev.txt --user
