#!/usr/bin/env python3 

"""
Process (CSV) quiz files of the form:
    Question, answer1, answer2....
Create includes for a test, and not a web form.
"""

import sys
import csv

QUESTION = 0 # type: int
FIRST_ANSWER = 1 # type: int
CORRECT = '^' # type: str

INDENT1 = "        " # type: str
INDENT2 = INDENT1 + INDENT1 # type: str
INDENT3 = INDENT2 + INDENT1 # type: str

quiz_file = None # type: str

if len(sys.argv) < 2:
    print("Must supply a quiz file.")
    exit(1)

quiz_file = sys.argv[1]
answers = 'abcdefghijklmnopqrstuvwxyz' # type: str

if len(sys.argv) > 2:
    delimiter = sys.argv[2] # type: str
else:
    delimiter = "," 

with open(quiz_file, "r") as f_in:
    freader = csv.reader(f_in, delimiter=delimiter)
    i = 1 # type: int
    for row in freader:
        print(INDENT1 + '<li>')
        print(INDENT2 + row[QUESTION])
        print(INDENT2 + '<ol type="a">')
        j = 0 # type: int
        for a in row[FIRST_ANSWER:]:
            correct = "" # type: str
            a = a.strip()
            if a.startswith(CORRECT):
                a = a[1:]
                correct = " *"
            print(INDENT3 + '<li>')
            print(INDENT3 + a + correct)
            print(INDENT3 + '</li>')
            j += 1

        print(INDENT2 + '</ol>')
        print(INDENT1 + '</li>')
        i += 1
