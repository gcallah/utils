#!/usr/bin/python
"""
Creates an html page from a template file.
"""

import sys
from pylib.create_page import create_page

if len(sys.argv) < 2:
    print("Must supply a page name.")
    exit(1)

PAGE_NM = sys.argv[1] # type: str
sys.stderr.write(PAGE_NM + "\n")
create_page(sys.stdin, sys.stdout, PAGE_NM)
