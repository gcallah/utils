"""
Glossary Linker: Takes in a directory of html files and 
modifies each file to include anchor links on the 
first instance of a term.
"""

import argparse
import sys
import glob
import errno
from collections import OrderedDict

ARG_ERROR = 1  # type: int
IO_ERROR = 2  # type: int

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("gloss_terms", help="glossary terms to contain links")
    arg_parser.add_argument("html_dir_path", help="html directory path to be parsed")
    args = arg_parser.parse_args()
    gloss_terms = args.gloss_terms
    html_dir_path = args.html_dir_path

# Create a dictionary for gloss terms
d = OrderedDict()  # type: Dict[str]

try:
    with open(gloss_terms, 'r') as f:
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
    print("Couldn't read " + gloss_terms)
    exit(IO_ERROR)

# Read all files in a directory
path = html_dir_path+"*.html"
files = glob.glob(path)

for name in files: 
    try:
        with open(name, "w+") as f: 
            # sys.stdout.write(f.read())
            # find 1st gloss term and replace with anchor
            for line in f:
                for word in line.split():
                    print(word)
    except IOError as exc:
        if exc.errno != errno.EISDIR: # ignore if dir not found.
            raise # Propagate other kinds of IOError.
