#!/usr/bin/python
"""
This program takes a list of topics to create and a
page template, and then creates a page for each topic,
following the template.
"""

import sys
from pathlib import Path
try:
    from typing import List, Any
except ImportError:
    print("WARNING: Typing module is not find")
from pylib.parse_site import parse_site
from pylib.create_page import create_page

HTML_PG = 0  # type: int
TITLE = 1  # type: int
OPEN_ERROR = 1  # type: int

HTML_EXT = "html"  # type: str
PTML_EXT = "ptml"  # type: str
ptml_dir = "html_src"  # type: str


def process_level(topic_list, level):
    """
    This function processes a level of the topics list
    and creates pages if they have a URL.
    It calls itself to process lower levels.
    """
    for topic in topic_list:
        if topic.url is not None:
            ptml_file = topic.url.replace(HTML_EXT, PTML_EXT)
            ptml_file = ptml_dir +  "/" + ptml_file
            my_file = Path(ptml_file)
            if not my_file.is_file():  # don't overwrite existing files!
                print("\nGoing to create " + ptml_file)
                with open(page_templ, 'r') as inf, \
                      open(ptml_file, 'w') as outf:
                    create_page(inf, outf, topic.title, topic.subtopics)
        elif topic.subtopics is not None:
            # if the topic had a url, we processed the subtopics above
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
except IOError:
    print("ERROR: Failed to open " + topics_file)
    exit(OPEN_ERROR)

process_level(topics, 1)
