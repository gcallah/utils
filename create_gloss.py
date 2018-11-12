#!/usr/bin/python
"""
Glossary Page Builder: Takes a text file list of key subject terms
and their definitions (tab-delimited) and builds the glossary
list as an HTML file. Has internal tags the key terms will be linked to.
"""

import argparse
from collections import OrderedDict
from pylib.html_tags import ulist, include_tag

ARG_ERROR = 1  # type: int
IO_ERROR = 2  # type: int
exit_error = False  # type: bool
file_nm = None

INDENT1 = "        "  # type: str
INDENT2 = INDENT1 + INDENT1  # type: str
INDENT3 = INDENT2 + INDENT1  # type: str

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("txt_file", help="text file to be parsed")
    args = arg_parser.parse_args()
    txt_file = args.txt_file


d = OrderedDict()  # type: Dict[str]

try:
    with open(txt_file, 'r') as f:
        line_no = 1
        try:
            # place terms/defs in dictionary
            for line in f:
                term = line.strip().split("\t")  # tab delimited
                d[term[0]] = term[1]
                line_no += 1
        except IndexError:
            print("Index error: check line " + str(line_no))
except IOError:
    print("Couldn't read " + txt_file)
    exit(IO_ERROR)

gloss_list = []
for key in d:
    key_id = key   # for now: your new func goes here!
    gloss_item = '<span class="hilight" id="'
    gloss_item += key_id + '">' + key + '</span>: '
    gloss_item += d[key]
    gloss_item += "<br />"
    gloss_item += include_tag(key ".txt")
    gloss_list.append(gloss_item)

s = ulist(css_class="nested", l=gloss_list)  # noqa E741
# write to standard out:
print(s)

if exit_error:
    exit(ARG_ERROR)
else:
    exit(0)
