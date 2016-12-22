#!/usr/bin/env python3 

import sys
import csv
from subprocess import call

HTML_PG = 0
TITLE = 1
LECTURE_TEMPLATE = "../utils/LectureTempl.html"
LECTURE_SCRIPT = "../utils/create_lecture.py"


if len(sys.argv) < 2:
    print("Must supply a file of lectures to create.")
    exit(1)

with open(sys.argv[1], "r") as f_in:
    freader = csv.reader(f_in)
    for row in freader:
        print("Creating html page = " + row[HTML_PG] + "; title = " + row[TITLE])
        call(LECTURE_SCRIPT + " " + row[TITLE] +
             " <" + LECTURE_TEMPLATE +
             " >" + row[HTML_PG],
             shell=True)
