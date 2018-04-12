#!/usr/bin/env python3 

import sys

indent = "                " # type: str

if len(sys.argv) < 2:
    print("Must supply a page name.")
    exit(1)

page_nm = sys.argv[1] # type: str
sys.stderr.write(page_nm)
for line in sys.stdin:
    sys.stdout.write(line)
    if "<title>" in line:
        sys.stdout.write(indent + page_nm + "\n")
    if "<h1>" in line:
        sys.stdout.write(indent + page_nm + "\n")

