#!/usr/bin/env python3 

import sys
from subprocess import call
from typing import List

HTML_PG = 0 # type: int
TITLE = 1 # type: int
PAGE_SCRIPT = "../utils/create_page.py"   # type: str


if len(sys.argv) < 3:
    print("Must supply a file of pages to create and a page template.")
    exit(1)

page_templ = sys.argv[2]  # type: str

with open(sys.argv[1], "r") as f_in:
    freader = csv.reader(f_in) 
    for row in freader:
        print("<a href=\"" + row[HTML_PG] + "\">\n    "
              + row[TITLE] + "\n</a>\n")
        call(PAGE_SCRIPT + " \"" + row[TITLE] +
             "\" <" + page_templ +
             " >" + row[HTML_PG],
             shell=True)
