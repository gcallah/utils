#!/usr/bin/env python3 

import sys
from subprocess import call
from pylib.parse_course import parse_course, CourseItem
try:
    from typing import List
except ImportError:
    print("WARNING: Typing module is not find")

HTML_PG = 0  # type: int
TITLE = 1  # type: int
OPEN_ERROR = 1  # type: int
PAGE_SCRIPT = "../utils/create_page.py"   # type: str

HTML_EXT = "html"  # type: str
PTML_EXT = "ptml"  # type: str
PTML_DIR = "html_src"  # type: str

if len(sys.argv) < 3:
    print("Must supply a file of pages to create and a page template.")
    exit(1)

pages = []
pages_file = sys.argv[1]
page_templ = sys.argv[2]  # type: str

try:
    pages = parse_course(pages_file)
except:
    print("ERROR: Failed to open " + pages_file)
    exit(OPEN_ERROR)

for course_module in pages:
    if course_module.url is not None:
        pass

