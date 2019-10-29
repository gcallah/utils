#!/bin/bash
virtualenv -q -p /user/bin/python3.7 $1
$1/bin/pip install -r requirements.txt
