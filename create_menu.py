#!/usr/bin/env python3 

import sys
from pylib.parse_course import parse_course
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
              % items[0].to_string())
        sys.exit(EMPTY_LIST)
    start_index = 0 # type: int
    curr_index = 0 # type: int
    level = []
    while curr_index < len(items):
        # make sure items of THIS level has the same indent level as the starting one
        if items[curr_index].ind_level != start_ind_level:
            print("ERROR: Bad input at %s. Indent level does not match context."
                  % items[curr_index].to_string())
            sys.exit(INDENT_MISMATCH)
        if items[curr_index].url is None:
            # handles empty menu here
            if (curr_index + 1 == len(items)
                or items[curr_index + 1].ind_level == start_ind_level):
                print("ERROR: Empty menu found at %s." % items[curr_index].to_string())
                sys.exit()
            curr_index += 1
            # make sure the item of NEXT level has the expected indent level
            if items[curr_index].ind_level != start_ind_level + 1:
                print("ERROR: Bad input at %s. Indent level does not match context."
                      % items[curr_index].to_string())
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

def create_submenu(level_list, context_empty_spaces:int, submenu_id:int, f:Any)-> int:
    # if submenu_id is None, create an uncollapsable menu
    # else, create a collapsable menu
    submenu_counter = 0 # type: int
    if submenu_id is not None:
        f.write(create_line_with_spaces(context_empty_spaces,
                "<ul class=\"collapse list-unstyled\" id=\"Submenu%d\">\n"
                % submenu_id))
    else:
        submenu_id = 0
        f.write(create_line_with_spaces(context_empty_spaces,
                "<ul class=\"list-unstyled components\">\n"))
    for level in level_list:
        f.write(create_line_with_spaces(context_empty_spaces + 4,
                                        "<li>\n"))
        if isinstance(level[1], list):
            submenu_counter += 1
            f.write(create_line_with_spaces(context_empty_spaces + 8,
                    "<a href=\"#Submenu%d\" data-toggle=\"collapse\"  \
aria-expanded=\"false\">\n" % (submenu_id + submenu_counter)))
            if level[2] is not None:
                f.write(create_line_with_spaces(context_empty_spaces + 12,
                        "<i class=\"glyphicon %s\"></i>\n" % level[2]))
            f.write(create_line_with_spaces(context_empty_spaces + 12,
                                            level[0] + "\n"))
            f.write(create_line_with_spaces(context_empty_spaces + 8,
                                            "</a>\n"))
            submenu_counter += create_submenu(level[1], context_empty_spaces + 8,
                           submenu_id + submenu_counter, f)
        else:
            f.write(create_line_with_spaces(context_empty_spaces + 8,
                                            "<a href=\"%s\">\n" % level[1]))
            if level[2] is not None:
                f.write(create_line_with_spaces(context_empty_spaces + 12,
                        "<i class=\"glyphicon %s\"></i>\n" % level[2]))
            f.write(create_line_with_spaces(context_empty_spaces + 12,
                                            level[0] + "\n"))
            f.write(create_line_with_spaces(context_empty_spaces + 8,
                                            "</a>\n"))
        f.write(create_line_with_spaces(context_empty_spaces + 4,
                                        "</li>\n"))
    f.write(create_line_with_spaces(context_empty_spaces, "</ul>\n"))
    return submenu_counter

if len(sys.argv) < 2:
    print("ERROR: Please specify input file name and output file name.")
    sys.exit(BAD_ARGS)
input_fname = sys.argv[INPUT]  # type: str
output_fname = sys.argv[OUTPUT]  # type: str

try:
    course_items = parse_course(input_fname)
except InputError as ie:
    print("ERROR: Bad input at %s. %s" % (ie.value, ie.message))
    sys.exit()

for course_item in course_items:
    course_item.print_item()

if len(course_items) == 0:
    print("WARNING: Empty input file.")
    sys.exit()

title_item = course_items[TITLE]
# title is required
if title_item.ind_level != 0:
    print("ERROR: Title indent level is: " + str(title_item.ind_level))
    sys.exit()
elif title_item.short_title is None:
    print("ERROR: Short title is required for navbar title.")
    sys.exit()

if len(course_items) > 1:
    # make sure content indent level start with 1
    if course_items[TITLE + 1].ind_level != 1:
        print("ERROR: Bad input at %s. Content indent level should start with 1." % course_items[TITLE + 1].to_string())
        sys.exit()

    # create a nested list with contents
    nested = create_nested_list(course_items[1:]) # type: List[object]
else:
    # if there is only one title line in the input file, just write the title
    nested = []

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
    create_submenu(nested, context_empty_spaces, submenu_id, f)

    f.write("</nav>\n")
