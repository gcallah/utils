#!/bin/bash

# This is a shell script for common use functions

# To use this in other scripts / import the functions below
# Use the following command

# source ./lib/common_function.sh

# Extracts the github repo from the github url
# Parameters:
#   $1 = the variable you would like the function to set
#   $2 = the github url you would like to extract from
# Note: nameref variables require bash 4.3 or later
# extract_github_url()
# {
#     # nameref to variable pointed to by $1
#     declare -n output=$1
# 
#     # Check if its a github url
#     if [[ $2 == *"https://github.com/"* ]]; then
#         # Set the extracted result
#         output="$(echo $2 | sed 's/.*\/\([^\/]*\)\.git/\1/')"
#     else
#         echo "extract_github_url(): non-github url given"
#         return 1
#     fi
# }

# # Version 2 in case declare with nameref doesn't work
extract_github_url()
{
    # Check if its a github url
    if [[ $1 == *"https://github.com/"* ]]; then
        # Set the extracted result
        echo "$(echo $1 | sed 's/.*\/\([^\/]*\)\.git/\1/')"
    else
        echo "extract_github_url(): non-github url given"
        return 1
    fi
}

# runs a spinner infinitely
spin()
{
  spinner="/|\\-/|\\-"
  while :
  do
    for i in `seq 0 7`
    do
      echo -n "${spinner:$i:1}"
      echo -en "\010"
      sleep 1
    done
  done
}