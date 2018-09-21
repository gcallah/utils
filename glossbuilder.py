'''
Glossary Builder: Takes a text file list of key subject terms and their definitions (tab-delimited) 
and builds the glossary list as an HTML file. Has internal tags the key terms will be linked to.
'''

# filter by username, send in assignment to nyuclasses

import os
import string
import re
import argparse

ARG_ERROR = 1  # type: int
exit_error = False # type: bool
strict_mode = False # type: bool
file_nm = None

def check_file(*files): #check if file exists
    for file in files:
        if not os.path.isfile(file):
            print(file + " is not a file")
            exit(ARG_ERROR)

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("file_nm", help="html file to be parsed")
    arg_parser.add_argument("-e", help="enable exit error", action="store_true")
    arg_parser.add_argument("-s", help="strict mode checks capitalized words",
                            action="store_true")
    args = arg_parser.parse_args()
    exit_error = args.e
    strict_mode = args.s
    file_nm = args.file_nm

check_file(file_nm)
saw_error = False  # type: bool
d = dict()  # type: Dict[str]
code_tag_on = False  # type:bool

with open('definitions.txt', 'r') as f:
    for line in f:
       term = line.strip().split("  ")
       d[term[0]] = term[1]

#create glossary file and clear set d
with open('glossary.html', 'a+') as f:
    f.writelines(i + '\n' for i in d)
    d.clear()

if exit_error:
    exit(ARG_ERROR)
else:
    exit(0)