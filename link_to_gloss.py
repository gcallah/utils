"""
Glossary Linker: Takes in a directory of html files and
gloss terms, then modifies each file to include anchor links
on the first instance of a term.
"""

import argparse
import glob
import errno
import re
from collections import OrderedDict
from pylib.html_tags import str_to_valid_id

ARG_ERROR = 1  # type: int
IO_ERROR = 2  # type: int


def create_word_link(key_id, word, href_link):
    """
        Function that creates an anchor link for a word
        using given key_id and word
    """
    return '<a href="' + href_link + '#' + key_id + '">' + word + '</a>'

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("gloss_terms",
                            help="glossary terms to contain links")
    arg_parser.add_argument("html_dir_path",
                            help="html directory path to be parsed")
    arg_parser.add_argument("href_link",
                            help="relative anchor link to be referred to")
    args = arg_parser.parse_args()
    gloss_terms = args.gloss_terms
    html_dir_path = args.html_dir_path
    href_link = args.href_link 

# Create a dictionary for gloss terms
gloss_dict = OrderedDict()  # type: Dict[str]

try:
    with open(gloss_terms, 'r') as f:
        LINE_NO = 1
        try:
            # place terms/defs in dictionary
            for line in f:
                term = line.strip().split("\t")  # tab delimited
                gloss_dict[term[0]] = term[1]
                LINE_NO += 1
        except IndexError:
            print("Index error: check line " + str(LINE_NO))
except IOError:
    print("Couldn't read " + gloss_terms)
    exit(IO_ERROR)

# Read all files in a directory
path = html_dir_path + "/*.html"
files = glob.glob(path)

gloss_terms_found = []

for name in files:
    try:
        with open(name, "r+") as f:
            # find 1st gloss term and replace with anchor
            for line in f:
                for word in line.split():
                    if word in gloss_dict and word not in gloss_terms_found:
                        gloss_terms_found.append(word)
                        key_id = str_to_valid_id(word)
                        word_link = create_word_link(key_id, word, href_link)
                        data = open(name).read()
                        f.write(re.sub(word, word_link, data, count=1))
    except IOError as exc:
        if exc.errno != errno.EISDIR:  # Do not fail if a directory is found
            raise  # Propagate other kinds of IOError.
