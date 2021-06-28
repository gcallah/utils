 #!/usr/bin/env bash

echo "Please enter the clone URL of your GitHub repo:"

read repo_url 

basename=$(basename $repo_url)
dir_name=${basename%.*}

echo "Cloning $dir_name..."

if [ -d "$dir_name" ]; then
    echo "$dir_name already exists."
else
    echo "Cloning $dir_name directory..."
    git clone $repo_url
fi

echo "Changing directory to $dir_name"
cd $dir_name 

echo "Creating requirements.txt"

if ls | grep -q "requirements.txt" ; then 
    echo "requirements.txt already exists."
else 
    touch requirements.txt
fi

echo "flask_restx" > ~/requirements.txt
echo "gunicorn" >> ~/requirements.txt

echo "Creating requirements-dev.txt"

if ls | grep -q "requirements-dev.txt" ; then 
    echo "requirements-dev.txt already exists."
else 
    touch requirements-dev.txt
fi

echo "flake8" > ~/requirements-dev.txt
echo "nose" >> requirements-dev.txt
echo "coverage" >> requirements-dev.txt

echo "Creating a makefile"

if ls | grep -q "makefile" ; then 
    echo "Makefile already exists."
else 
    touch makefile
fi

echo "Installing requirements"

pip3 install -r requirements.txt --user

echo "Installing dev requirements"

pip3 install -r requirements-dev.txt --user
