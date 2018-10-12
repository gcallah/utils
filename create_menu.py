#!/usr/bin/env python3 

import sys
from pylib.parse_site import parse_site, InputError, IndentError, Topic
from pylib.html_tags import sidebar, sidebar_links

try:
    from typing import List, Set, Any
except ImportError:
    print("WARNING: Typing module is not find")

TITLE = 0 # type: int
INPUT = 1 # type: int
OUTPUT = 2 # type: int
EMPTY_LIST = 1 # type: int
INDENT_MISMATCH = 2 # type: int
BAD_ARGS = 3 # type: int

INDENT = "    " # type: str

tot_submenus = 0 # type: int


def get_pad(level):
    return INDENT * level


def create_link(topic, level, is_url):
    global tot_submenus
    padding = get_pad(level + 1)
    sidebar_links(padding=padding,topic=topic,tot_submenus=tot_submenus, is_url=is_url)


def process_menu(topics, level):
    global tot_submenus
    s = ""
    padding = get_pad(level)
    if level == 1:
        s += "%s<ul class=\"list-unstyled components\">\n" % padding
    else:
        s += ("%s<ul class=\"collapse list-unstyled\" id=\"Submenu%d\">\n"
              % (padding, tot_submenus))
        tot_submenus += 1

    for topic in topics:
        if topic.url is not None:
            s += create_link(topic, level, True)
        else:
            if topic.subtopics is not None:
                s += create_link(topic, level, False)
                s += process_menu(topic.subtopics, level + 1)
    s += "%s</ul>\n" % padding
    return s
        

if len(sys.argv) < 3:
    print("ERROR: Please specify input file name and output file name.")
    sys.exit(BAD_ARGS)

input_fname = sys.argv[INPUT]  # type: str
output_fname = sys.argv[OUTPUT]  # type: str

title = None
course_items = None

try:
    (title, course_items) = parse_site(input_fname)
except InputError as ie:
    print("ERROR: Input error at %s: %s" % (ie.value, ie.msg))
    sys.exit()

# for debugging:
# for course_item in course_items:
#     print(course_item)

if len(course_items) == 0:
    print("WARNING: Empty input file.")
    sys.exit()

# title is required
if title.level != 0:
    print("ERROR: Title indent level is: " + str(title.level))
    sys.exit()
elif title.short_title is None:
    print("ERROR: Short title is required for navbar title.")
    sys.exit()

s = sidebar(title=title.title, short_title=title.short_title, menu_txt=process_menu(course_items, 1))

# write generated sidebar
with open(output_fname, 'w+') as f:
    f.write(s)
