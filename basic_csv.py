#!/usr/bin/env python3

"""
Process (CSV) quiz files of the form:
    Question, answer1, answer2....
"""

import sys
import csv

if len(sys.argv) < 2:
    print("Must supply an input file.")
    exit(1)

input_file = sys.argv[1]

delimiter = ","  # type: str
if len(sys.argv) > 2:
    delimiter = sys.argv[2]

with open(input_file, "r") as f_in:
    freader = csv.reader(f_in, delimiter=delimiter)

    for row in freader:
        if len(row) < 2:  # allow blank lines; len of 1 makes no sense!
            continue

        for fld in row:
            print("Have a field of ", fld)
