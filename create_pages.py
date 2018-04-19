#!/usr/bin/env python3 

import sys
from pylib.parse_course import parse_course
from subprocess import call
try:
    from typing import List
except ImportError:
    print("WARNING: Typing module is not find")
HTML_PG = 0 # type: int
TITLE = 1 # type: int
OPEN_ERROR = 1 # type: int
PAGE_SCRIPT = "../utils/create_page.py"   # type: str


if len(sys.argv) < 3:
    print("Must supply a file of pages to create and a page template.")
    exit(1)

pages = sys.argv[1]
page_templ = sys.argv[2]  # type: str

try:
    with open(pages, "r") as f_in:
        freader = csv.reader(f_in) 
        for row in freader:
            print("<a href=\"" + row[HTML_PG] + "\">\n    "
                  + row[TITLE] + "\n</a>\n")
            call(PAGE_SCRIPT + " \"" + row[TITLE] +
                 "\" <" + page_templ +
                 " >" + row[HTML_PG],
                 shell=True)
except:
    print("ERROR: Failed to open " + pages)
    exit(OPEN_ERROR)
