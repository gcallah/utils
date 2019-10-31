#!/bin/bash

if [[ -n $1 ]]; then
	mkdir -p "$1"
else
	echo "must enter in directory name"
fi


#virtualenv -q -p /user/bin/python3.7 $1
#$1/bin/pip install -r requirements.txt
