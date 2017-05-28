#!/usr/bin/env python3 

"""
Process (CSV) quiz files of the form:
    Question, answer1, answer2....
"""

import sys
import csv

QUESTION = 0
FIRST_ANSWER = 1
CORRECT = '^'

INDENT1 = "    "
INDENT2 = INDENT1 + INDENT1
INDENT3 = INDENT2 + INDENT1
INDENT4 = INDENT2 + INDENT2

quiz_file = None

if len(sys.argv) < 2:
    print("Must supply a quiz file.")
    exit(1)

quiz_file = sys.argv[1]
answer_key = ''
answers = 'abcdefghijklmnopqrstuvwxyz'

with open(quiz_file, "r") as f_in:
    freader = csv.reader(f_in)
    print(INDENT1 + '<details>')
    print(INDENT2 + '<summary class="sum1">')
    print(INDENT3 + 'Quiz')
    print(INDENT2 + '</summary>')
    print(INDENT2 + '<ol>')
    
    i = 1
    for row in freader:
        print(len(row))
        if len(row) < 2:  # allow blank lines; len of 1 makes no sense!
            print("Skipping row")
            continue

        print(INDENT3 + '<li>')
        print(INDENT4 + row[QUESTION])
        print(INDENT3 + '</li>')
        print(INDENT3 + '<ol type="a">')
        j = 0
        for a in row[FIRST_ANSWER:]:
            a = a.strip()
            if a.startswith(CORRECT):
                a = a[1:]
                answer_key += str(i) + '. ' + answers[j] + "; "
            print(INDENT4 + '<li>')
            print(INDENT4 + '<input type="radio" name="q'
                  + str(i) + '" value="' + answers[j] + '">')
            print(INDENT4 + a)
            print(INDENT4 + '</li>')
            j += 1

        print(INDENT3 + '</ol>')
        i += 1

    print(INDENT2 + '</ol>')
    print(INDENT2 + '<details>')
    print(INDENT3 + '<summary class="sum2">')
    print(INDENT4 + 'Answers')
    print(INDENT3 + '</summary>')
    print(INDENT3 + '<p>')
    print(INDENT4 + answer_key)
    print(INDENT3 + '</p>')
    print(INDENT2 + '</details>')
    print(INDENT1 + '</details>')
