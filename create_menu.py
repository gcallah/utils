#!/usr/bin/python
"""
    Creates a menu from a tab-delimited text file.
"""

import sys
from pylib.parse_site import parse_site, InputError
from pylib.html_tags import sidebar, sidebar_links

TITLE = 0 # type: int
INPUT = 1 # type: int
OUTPUT = 2 # type: int
EMPTY_LIST = 1 # type: int
INDENT_MISMATCH = 2 # type: int
BAD_ARGS = 3 # type: int

INDENT = "    " # type: str

tot_submenus = 0 # type: int


def get_pad(level):
    """
        Get padding amount.
    """
    return INDENT * level


def create_link(topic, level, is_url):
    """
        Creates a link in the sidebar.
    """
    global tot_submenus
    padding = get_pad(level + 1)
    return sidebar_links(padding=padding, topic=topic,
                         tot_submenus=tot_submenus, is_url=is_url)


def process_menu(topics, level):
    """
        Processes a menu level.
    """
    global tot_submenus
    menu_txt = ""
    padding = get_pad(level)
    if level == 1:
        menu_txt += "%s<ul class=\"list-unstyled components\">\n" % padding
    else:
        menu_txt += ("%s<ul class=\"collapse list-unstyled\" id=\"Submenu%d\">\n"
                     % (padding, tot_submenus))
        tot_submenus += 1

    for topic in topics:
        if topic.url is not None:
            menu_txt += create_link(topic, level, True)
        else:
            if topic.subtopics is not None:
                menu_txt += create_link(topic, level, False)
                menu_txt += process_menu(topic.subtopics, level + 1)
    menu_txt += "%s</ul>\n" % padding
    return menu_txt


if len(sys.argv) < 2:
    print("ERROR: Please specify input file name.")
    sys.exit(BAD_ARGS)

input_fname = sys.argv[INPUT]  # type: str

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

if not course_items:
    print("WARNING: Empty input file.")
    sys.exit()

# title is required
if title.level != 0:
    print("ERROR: Title indent level is: " + str(title.level))
    sys.exit()
elif title.short_title is None:
    print("ERROR: Short title is required for navbar title.")
    sys.exit()

s = sidebar(title=title.title, short_title=title.short_title,
            menu_txt=process_menu(course_items, 1))

# write generated sidebar
print(s, end="")
