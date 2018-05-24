#!/usr/bin/env python3 

import sys
from pathlib import Path
try:
    from typing import List, Any
except ImportError:
    print("WARNING: Typing module is not find")
from pylib.parse_site import parse_site, InputError, IndentError, Topic
from pylib.create_page import create_page

HTML_PG = 0  # type: int
TITLE = 1  # type: int
OPEN_ERROR = 1  # type: int

HTML_EXT = "html"  # type: str
PTML_EXT = "ptml"  # type: str
ptml_dir = "html_src"  # type: str


def process_level(topics, level):
    for topic in topics:
        if topic.url is not None:
            ptml_file = topic.url.replace(HTML_EXT, PTML_EXT)
            ptml_file = ptml_dir +  "/" + ptml_file
            my_file = Path(ptml_file)
            if not my_file.is_file():  # don't overwrwite existing files!
                print("\nGoing to create " + ptml_file)
                with open(page_templ, 'r') as inf, \
                      open(ptml_file, 'w') as outf:
                    create_page(inf, outf, topic.title, topic.subtopics)
        if topic.subtopics is not None:
            process_level(topic.subtopics, level + 1)


if len(sys.argv) < 3:
    print("Must supply a file of topics to create and a page template.")
    exit(1)

topics = [] # type: List[Any]
topics_file = sys.argv[1] # type: str
page_templ = sys.argv[2]  # type: str
if len(sys.argv) > 3:
    ptml_dir = sys.argv[3]

title = None
topics = None
try:
    (title, topics) = parse_site(topics_file)
except:
    print("ERROR: Failed to open " + topics_file)
    exit(OPEN_ERROR)

process_level(topics, 1)

