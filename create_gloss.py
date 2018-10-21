#!/usr/bin/python
'''
Glossary Page Builder: Takes a text file list of key subject terms and their definitions (tab-delimited) 
and builds the glossary list as an HTML file. Has internal tags the key terms will be linked to.
'''

import os
import string
import re
import argparse
from pylib.html_tags import ulist
from collections import OrderedDict

ARG_ERROR = 1  # type: int
exit_error = False # type: bool
file_nm = None

INDENT1 = "        " # type: str
INDENT2 = INDENT1 + INDENT1 # type: str
INDENT3 = INDENT2 + INDENT1 # type: str

def check_file(*files): #check if file exists
    for file in files:
        if not os.path.isfile(file):
            print(file + " is not a file")
            exit(ARG_ERROR)

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("txt_file", help="text file to be parsed")
    args = arg_parser.parse_args()
    txt_file = args.txt_file
    

check_file(txt_file)
d = OrderedDict()  # type: Dict[str]

with open(txt_file, 'r') as f:
    line_no = 1
    try:
        #place terms/defs in dictionary
        for line in f:
            term = line.strip().split("\t") #tab delimited
            d[term[0]] = term[1]
            line_no += 1
    except IndexError: 
        print("Index error: check line " + str(line_no))

gloss_list = []
for key in d:
    gloss_item = '<a name=' + key + '>'
    gloss_item += '<span class="hilight">' + key + '</span>:'
    gloss_item += '</a> '
    gloss_item += d[key]
    gloss_list.append(gloss_item)

s = ulist(css_class="nested", l=gloss_list)
# write to standard out:
print(s)

if exit_error:
    exit(ARG_ERROR)
else:
    exit(0)
