#!/usr/bin/env python3 

import sys
from pylib.parse_course import *

try:
    from typing import List,Set, Any
except ImportError:
    print("WARNING: Typing module is not find")

TITLE = 0 # type: int
INPUT = 1 # type: int
OUTPUT = 2 # type: int
EMPTY_LIST = 1 # type: int
INDENT_MISMATCH = 2 # type: int
BAD_ARGS = 3 # type: int

def create_line_with_spaces(n:int, str:str) -> str:
    return ' ' * n + str

#What is the exact type for item?

def create_nested_list(items):
    if len(items) == 0:
        print("ERROR: Empty list in recursion")
        sys.exit(EMPTY_LIST)
    start_ind_level = items[0].ind_level # type: int
    if start_ind_level == 0:
        print("ERROR: Bad input at %s. Indent level should be at least 1 in contents."
              % items[0])
        sys.exit(EMPTY_LIST)
    start_index = 0 # type: int
    curr_index = 0 # type: int
    level = [] # type: List[List[object]]
    while curr_index < len(items) - 1:
        if items[curr_index].url is None:
            curr_index += 1
            if int(items[curr_index].ind_level) != start_ind_level + 1:
                print("ERROR: Indent level does not match context.")
                sys.exit(INDENT_MISMATCH)
            while (curr_index < len(items) and
                   items[curr_index].ind_level > start_ind_level):
                curr_index += 1
            level.append([items[start_index].title,
                          create_nested_list(items[start_index + 1:curr_index]),
                          items[start_index].url])
        else:
            level.append([items[curr_index].title,
                          items[curr_index].url, items[curr_index].glyphicon])
            curr_index += 1
        start_index = curr_index
    return level

#Mypy find an error here, so I delete the mypy code for this to make the type dynamic.
#But we still need to make sure what is the exact type for level_list

def create_submenu(level_list, context_empty_spaces:int, submenu_id:int, submenu_counter:int, f:Any)-> None:
    # if submenu_id is None, create a uncollapsable menu
    # else, create a collapsable menu
    if submenu_id is not None:
        f.write(create_line_with_spaces(context_empty_spaces,
                "<ul class=\"collapse list-unstyled\" id=\"Submenu%d\">\n"
                % submenu_id))
    else:
        f.write(create_line_with_spaces(context_empty_spaces,
                "<ul class=\"list-unstyled components\">\n"))
    for level in level_list:
        f.write(create_line_with_spaces(context_empty_spaces + 4, "<li>\n"))
        if isinstance(level[1], list):
            f.write(create_line_with_spaces(context_empty_spaces + 8,
                    "<a href=\"#Submenu%d\" data-toggle=\"collapse\" " +
                    "aria-expanded=\"false\">\n" % submenu_counter))  #Mypy tests shows that there is a type error
                    #Not all arguments converted during string formatting
                    
            if level[2] is not None:
                f.write(create_line_with_spaces(context_empty_spaces + 12,
                        "<i class=\"glyphicon %s\"></i>\n" % level[2]))
            f.write(create_line_with_spaces(context_empty_spaces + 12, level[0] + "\n"))
            f.write(create_line_with_spaces(context_empty_spaces + 8, "</a>\n"))
            submenu_counter += 1
            create_submenu(level[1], context_empty_spaces + 8,
                           submenu_counter - 1, submenu_counter, f)
        else:
            f.write(create_line_with_spaces(context_empty_spaces + 8,
                                            "<a href=\"%s\">\n" % level[1]))
            if level[2] is not None:
                f.write(create_line_with_spaces(context_empty_spaces + 12,
                        "<i class=\"glyphicon %s\"></i>\n" % level[2]))
            f.write(create_line_with_spaces(context_empty_spaces + 12, level[0] + "\n"))
            f.write(create_line_with_spaces(context_empty_spaces + 8, "</a>\n"))

        f.write(create_line_with_spaces(context_empty_spaces + 4, "</li>\n"))
    f.write(create_line_with_spaces(context_empty_spaces, "</ul>\n"))

if len(sys.argv) < 2:
    print("ERROR: Please specify input file name and output file name.")
    sys.exit(BAD_ARGS)
input_fname = sys.argv[INPUT] # type: str
output_fname = sys.argv[OUTPUT] # type: str

try:
    course_items = parse_course(input_fname)
except InputError as ie:
    print("ERROR: Bad input at %s. %s" % (ie.value, ie.message))
    sys.exit()

for course_item in course_items:
    course_item.print_item()

title_item = course_items[TITLE]
# title is required
if int(title_item.ind_level) != 0:
    print("ERROR: Title indent level is: " + str(title_item.ind_level))
    sys.exit()
elif title_item.short_title is None:
    print("ERROR: Short title is required for navbar title.")
    sys.exit()

# create a nested list with contents
nested = create_nested_list(course_items[1:])

# write generated sidebar
with open(output_fname, 'w+') as f:
    # write title
    f.write("<!-- Sidebar Holder -->\n<nav id=\"sidebar\">\n\
        <div id=\"sidebarCollapse\">\n        \
<div class=\"sidebar-header\">\n            \
<h1>\n            %s\n            </h1>\n            \
<strong>%s</strong>\n        \
</div>\n    </div>\n"
            % (title_item.title, title_item.short_title))

    # write contents
    context_empty_spaces = 4 # type: int
    submenu_id = None # type: int
    submenu_counter = 0 # type: int
    create_submenu(nested, context_empty_spaces, submenu_id, submenu_counter, f)

    f.write("</nav>\n")
