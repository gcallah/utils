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

# pelican-themes is a very large repo that has directories and other submodules
# upon first run on this script on a fresh utils repo, it will take a while to initialize
# Afterwhich, the script will be much faster.

# Using themes

# All themes gets placed into the themes folder of your respective project directory
# If you wish to use this script to insert a pelican-theme, please note it will attempt 
# to modify the THEME variable in your pelicanconf.py if it exists. 
# Otherwise, it will append both THEME and OUTPUT_PATH to pelicanconf.py

# Example of using the -t option (sensitive, must match theme name in pelican-themes repo)
# 	./setup.sh <dir> -t Flex
# 	./setup.sh <dir> -t blue-penguin

# In the event that it seems no themes was added after successful completion of the script
# please check if your pelicanconf.py has the THEME (case sensitive to pelican) 
# is set to the directory of where the theme should be
# The script will attempt its best to modify the THEME variable, but it could fail in unforeseen cases.
# Should work most of the time.

# Or also check if themes folder in your project directory has been populated with actual 
# files in your selected theme.
# I.E, if blue-penguin was your theme, there should be a folder called blue-penguin in 
# your project/theme folder, which should contain files with used by the theme.
# This could happen if the pelican-themes repo was not initialized by the script correctly.

set -e

# Functions
usageMessage() { 	
	printf "Usage: ./setup.sh <directory / github repo url> [-i] [-t] [--help]\n\n"
}

helpMessage() {
	usageMessage
	printf "Options: \n"
	printf "\t-i : enable the use of pelican-quickstart (interactive)\n\n"
	printf "\t-t : allows you to select a theme from the pelican-themes repo\n"
	printf "\t     for your project. (case-sensitive)\n\n"
	printf "\t You need to give the exact directory name as shown in the\n"
	printf "\t pelican-themes repository.\n\n"
	printf "\t Example: If \"blue-penguin\" is the directory name in pelican-themes repo\n"
	printf "\t Then the command would be: \n\t \"setup.h <your project directory> -t blue-penguin\"\n\n"
	printf "By default: setup.sh will provide you with a template pelican project\n"
	printf "pelican-quickstart allows for more customizations during setup.\n(Enabled by -i flag)\n\n"

	printf "Please note: pelican-themes is a submodule within 'utils/pelican_setup'\n"
	printf "The official pelican-themes repository can be found at: \nhttps://github.com/getpelican/pelican-themes\n\n"
	printf "If you have recently clone a fresh utils repo,\nit might take a while for the script "
	printf "to init and update pelican-themes.\n"
}

# Variables
# Gets the current location of the script we are running
scriptDir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
INTERACTIVE_MODE=0
PELICAN_THEME_DIR=$scriptDir/pelican-themes
SELECTED_THEME=base_theme
CURRENT_DIR="$(pwd)"

# This lets you run the script from anywhere. Independent of the current working dir
# the path is relative to this script's directory
source $scriptDir/../lib/common_functions.sh

if [[ $1 == "--help" || $# -gt 5 ]]; then
	helpMessage
	exit 0;
fi

# Check for required input
if [[ -z $1 ]]; then
	printf "This script requires a github repo url or target directory name\n\n"
	usageMessage
	printf "Use --help for more info to see how this script is used.\n"
	exit 1;
fi

# Update / init pelican-themes as needed
printf "Running \"git submodule update --init --recursive\" on pelican-themes.\n"

# Go into the directory of the script to run git
cd $scriptDir

# Run the synchronous (blocking) command.
git submodule update --init --recursive

# return to original working directory
cd $CURRENT_DIR

# run sed on $1 to get dir name from git or get directory name
if [[ $1 == *"https://github.com/"* ]]; then
    projectDir=$(extract_github_url $1)
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
argv=("$@")
argc=$#

# $@ starts right after the script name, (after $0)
# This achives the same goal without the use of indirection parameter expansion
for (( i = 1; i < argc; i++ )); do
	param=${argv[i]}

	if [[ $param == "-i" ]]; then
		INTERACTIVE_MODE=1

	elif [[ $param == "-t" ]]; then

		#increment i to see what the theme is potentially
		i=$((i+1))

		param=${argv[i]}

		if [[ -n param ]]; then
			SELECTED_THEME=$param

			# Check if we have a valid theme in pelican-themes
			if [[ ! -d $PELICAN_THEME_DIR/$SELECTED_THEME ]]; then
				printf "\nTheme Not Found: $SELECTED_THEME is not a part of the pelican-themes repo\n"
				printf "\nCommon error: case sensitivity. The theme name must be exactly as show in pelican-themes\n"
				printf "\nUse --help for more info\n"
				exit 2;
			fi

			printf "THEME SELECTED: %s\n" $SELECTED_THEME

		else
			printf "[-t] expects a theme directory from pelican-themes\n"
			printf "\nUse --help for more info\n"
			exit 3;
		fi

	elif [[ $param == "--help" ]]; then
		helpMessage
		exit 4;

	else
		printf "Unknown option: %s\n" $param
		exit 5;
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
	printf "No theme selected, falling back to base_theme\n"
	# Copies basic theme from our own library
	rsync -r --ignore-existing $scriptDir/custom_themes/$SELECTED_THEME $projectDir/themes
else
	printf "Selected Theme: %s\n" $SELECTED_THEME
	# Copies theme from offical pelican-themes repo
	rsync -r --ignore-existing $scriptDir/pelican-themes/$SELECTED_THEME $projectDir/themes
fi

# Set theme to base_theme
chmod o+w $projectDir/pelicanconf.py

# Check if there was already a THEME variable, modify it if exists
if grep -q "THEME[  ]*=[  ]*" $projectDir/pelicanconf.py; then
	sed -i "s/THEME[  ]*=[  ]*[\'|\"].*[\'|\"]/THEME=\"themes\/$SELECTED_THEME\"/" $projectDir/pelicanconf.py 
else
	# Note: you need at least one new line between the command
	# and the start of the heredoc
	cat << EOI >> $projectDir/pelicanconf.py


# Inserted by pelican_setup.sh

THEME="themes/$SELECTED_THEME"
OUTPUT_PATH="docs" # Github Pages Standard
EOI

fi

# Reset file permissions
chmod o-w $projectDir/pelicanconf.py

# Add gitignore to projectdir
# Copy the gitignore file (if doesn't already exit)
if [[ ! -f $projectDir/.gitignore ]]; then
	cp $scriptDir/base_project/.gitignore $projectDir
fi

# Git add all files
cd $projectDir
git add .

printf "\n\nYour project is now available at: %s\n" $projectDir/
