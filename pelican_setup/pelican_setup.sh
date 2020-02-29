#!/bin/bash
#
# This script is designed to setup a base pelican project
# It adds additional setup on top of the existing pelican-quickstart tool

# The script has a slight bias towards github pages by changing output directory
# to called "docs" since github pages reads from docs folder.
# This is useful if you want to push the pelican project source code with the 
# processed html output while keeping your files organized and separate.

# The pelican-quickstart provide an alternative (ghp-import) that might not be convenient
# in comparison to pushing the whole project directory

# Default behavior: copies a base pelican project that we provide
# Interactive behavior: Runs pelican-quickstart with additional modifications
# 						To configuration files

# NOTE: pelican-quickstart does overwrite existing configuration files
# 		but leaves content folder alone.

# Note: pelican-quickstart gives you a makefile as well
# If you have an existing makefile, please handle accordingly

# python3 comes with venv preinstalled
# Note: python3 is the default for python version 3+
# sudo apt-get install python3-venv is needed prior

set -e

# Function
usage() { 	
	printf "Usage: ./pelican_setup [directory / github repo url] [-i] [-t] <name of theme (case sensitive)>\n\n"
	printf "Use --help for more info" 
}

# Variables
# Gets the current location of the script we are running
scriptDir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
INTERACTIVE_MODE=0
PELICAN_THEME_DIR=$scriptDir/pelican-themes
SELECTED_THEME=base_theme

# import common functions
source $(dirname $scriptDir)/common_functions.sh

# Help output
if [[ $1 == "--help" || $# -gt 5 ]]; then
	usage
	printf "Options: \n"
	printf "\t-i : enable the use of pelican-quickstart (interactive)\n\n"
	printf "\t-t : allows you to select a theme from the pelican-themes repo for your project\n\n\n"
	printf "By default: pelican_setup.sh will provide you with a template pelican project\n"
	printf "pelican-quickstart allows for more customizations during setup.\n"
	exit 0;
fi

# Check for required input
if [[ -z $1 ]]; then
	printf "This script requires a github repo url or target directory name\n"
	usage
	printf "Use --help for more info.\n"
	exit 1;
fi

# run sed on $1 to get dir name from git or get directory name
if [[ $1 == *"https://github.com/"* ]]; then
	extract_github_url projectDir $1
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

# Look through the flags / options if any
for ((i=2; i<=$#; i++)); do
	# turn interactive mode on
  if [[ ${!i} == "-i" ]]; then
	INTERACTIVE_MODE=1

  elif [[ ${!i} == "-t" ]]; then

	#increment i to see what the theme is potentially
	i=$((i+1))

	if [[ ${!i} != "-*" && -n ${!i} ]]; then
		SELECTED_THEME=${!i}

		# Check if we have a valid theme in pelican-themes
		if [[ ! -d $PELICAN_THEME_DIR/$SELECTED_THEME ]]; then
			printf "$SELECTED_THEME is not a part of the known pelican-themes\n. --help for more info\n"
			exit 3
		fi

	else
		printf "[-t] expects a theme directory from pelican-themes\n"
		exit 2
	fi
  fi
done

# Create a virtual environment for flask project
printf "Creating virtual environment in %s\n" $projectDir
python3 -m venv $projectDir

# Activate the virtual enviroment we just created, make sure script is being called with source
printf "Activating the virtual environment in %s\n" $projectDir
# Source = running the command in the current shell
source $projectDir/bin/activate

# Installing dependencies
printf "Installing pelican with markdown support\n"
pip3 install pelican[Markdown] --no-cache-dir

# Runs pelican-quickstart if enabled, else copies a base project from utils
if [[ INTERACTIVE_MODE -eq 1 ]]; then
	# Running pelican-quickstart
	printf "\n\nStarting pelican-quickstart tool\n\n"
	pelican-quickstart -p $projectDir

	# Makes additional directories for custom themes
	mkdir -p "$projectDir/content/pages"
	mkdir -p "$projectDir/themes"
	
	if [[ -e $projectDir/Makefile ]]; then
		# Changing the output dir in the makefile
		sed -i 's/OUTPUTDIR=$(BASEDIR)\/.*/OUTPUTDIR=$(BASEDIR)\/docs/' $projectDir/Makefile
	fi

	# Remove empty output dir created by pelican-quickstart
	rm -r $projectDir/output

else
	printf "\nCopying base project from utils\n\n"
	# Copies base project
	rsync -r --ignore-existing $scriptDir/base_project/* $projectDir/
fi

# Sets up themes for the new project

# Default theme
if [[ $SELECTED_THEME == "base_theme" ]]; then
	# Copies basic theme from our own library
	rsync -r --ignore-existing $scriptDir/custom_themes/$SELECTED_THEME $projectDir/themes
else
	# Copies theme from offical pelican-themes repo
	rsync -r --ignore-existing $scriptDir/pelican-themes/$SELECTED_THEME $projectDir/themes
fi

# Set theme to base_theme
chmod o+w $projectDir/pelicanconf.py

# Note: you need at least one new line between the command
# and the start of the heredoc
cat << EOI >> $projectDir/pelicanconf.py


# Inserted by pelican_setup.sh

THEME="themes/$SELECTED_THEME"
OUTPUT_PATH="docs" # Github Pages Standard
EOI

# Reset file permissions
chmod o-w $projectDir/pelicanconf.py

printf "\n\nYour project is now available at: %s\n" $projectDir/