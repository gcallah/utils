#!/bin/bash
#
# This script is designed to setup a base pelican project
# It adds additional setup on top of 
# the existing pelican-quickstart tool

# Note: pelican-quickstart gives you a makefile as well
# If you have an existing makefile, please handle accordingly

# python3 comes with venv preinstalled
# Note: python3 is the default for python version 3+
# sudo apt-get install python3-venv is needed prior

set -e
# Variables
scriptDir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Check for input
if [[ -z $1 ]]; then
	printf "This script requires a github repo url or directory name\n"
	exit 1;
fi
# run sed on $1 to get dir name from git or get directory name
if [[ $1 == *"https://github.com/"* ]]; then
	projectDir=$(echo $1 | sed 's/.*\/\([^\/]*\)\.git/\1/')
	directoryType="github"
else
	projectDir=$1
	directoryType="local"
fi

printf "Project Directory Name = %s\n" $projectDir

# We shouldn't clone if directory already exists, but we can still proceed with the script
if  [[ -d $projectDir ]]; then
    printf "Directory already exists;\n"
    printf "No need to create directory / clone.\n"

elif [[ $directoryType == "github" ]]; then
    printf "We are going to clone %s\n" $1
    git clone $1 
	if [[ $? -ne 0 ]]; then
		printf "Trouble cloning %s, exiting script\n" $1
		exit 3;
	fi
else
    printf "Creating local repository: %s\n" $projectDir
    mkdir -p "$projectDir"
	git init $projectDir
fi

# Create a virtual environment for flask project
printf "Creating virtual environment in %s\n" $projectDir
python3 -m venv $projectDir

# Activate the virtual enviroment we just created, make sure script is being called with source
printf "Activating the virtual environment in %s\n" $projectDir
# Source = running the command in the current shell
source $projectDir/bin/activate

# Installing dependencies
printf "Installing pelican with markdown support"
pip3 install pelican[Markdown] --no-cache-dir

# Running pelican-quickstart
printf "Starting pelican-quickstart tool\n\n"
pelican-quickstart -p $projectDir

# Makes additional directories for custom themes
mkdir -p "$projectDir/content/pages"
mkdir -p "$projectDir/themes"

# Copies some basic themes
rsync -r --ignore-existing $scriptDir/themes/* $projectDir/themes

# Set theme to base_theme
chmod o+w $projectDir/pelicanconf.py

# Note: you need at least one new line between the command
# and the start of the heredoc
cat << EOI >> $projectDir/pelicanconf.py


# Inserted by pelican_setup.sh

THEME='themes/base_theme'
OUTPUT_PATH='docs' # Github Pages Standard
EOI

# Reset file permissions
chmod o-w $projectDir/pelicanconf.py

# Changing the output dir in the makefile
sed -i 's/OUTPUTDIR=$(BASEDIR)\/.*/OUTPUTDIR=$(BASEDIR)\/docs/' $projectDir/Makefile

# Remove empty output dir created by pelican-quickstart
rm -r $projectDir/output