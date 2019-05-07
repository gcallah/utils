#!/usr/bin/env python3

"""
The aim of this script is to take a suitably marked up .cpp
file and turn it into a web page.
"""

import sys
import re

import pylib.create_page as pyl
import pylib.html_tags as html

COMMENT_START = re.compile("^\s*/\*\s*$")
COMMENT_END = re.compile("^\s*\* \*/\s*$")


if len(sys.argv) < 2:
    print("Must supply a C++ file.")
    exit(1)

cpp_file = sys.argv[1]

print(pyl.ptml_start_stuff(cpp_file))
with open(cpp_file, 'r') as inp:
    # we will find ourselves in "regular" text (long comments)
    # or in code.
    text = ""
    in_reg_text = False
    for line in inp:
        if COMMENT_START.match(line):
            # print("STARTING COMMENT")
            if len(text):
                print(html.code_par(text))
            in_reg_text = True
            text = ""
            continue
        elif COMMENT_END.match(line):
            # print("ENDING COMMENT")
            in_reg_text = False
            print(html.par(text))
            text = ""
            continue
        if in_reg_text:
            text += line.replace("*", "")
        else:
            text += line

    if len(text):
        print(html.code_par(text))

print(pyl.html_end_stuff())
