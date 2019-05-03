#!/usr/bin/env python3

"""
The aim of this script is to take a suitably marked up .cpp
file and turn it into a web page.
"""

import sys
import pylib.create_page as pyl
import pylib.html_tags as html


if len(sys.argv) < 2:
    print("Must supply a C++ file.")
    exit(1)

cpp_file = sys.argv[1]

print(pyl.html_start_stuff(cpp_file))
with open(cpp_file, 'r') as inp:
    in_comment = False
    for line in inp:
        print(html.par(line))

print(pyl.html_end_stuff())
