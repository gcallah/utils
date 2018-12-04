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


def create_word_link(key_id, word, href_link="http://www.thedevopscourse.com/devops/gloss"):
    """
        Function that creates an anchor link for a word
        using given key_id and word
    """
    return '<a href="' + href_link + '#' + key_id + '">' + word + '</a>'

if __name__ == '__main__':
    ARG_PARSER = argparse.ArgumentParser()
    ARG_PARSER.add_argument("gloss_terms",
                            help="glossary terms to contain links")
    ARG_PARSER.add_argument("html_dir_path",
                            help="html directory path to be parsed")
    ARGS = ARG_PARSER.parse_args()
    GLOSS_TERMS = ARGS.gloss_terms
    HTML_DIR_PATH = ARGS.html_dir_path

# Create a dictionary for gloss terms
GLOSS_DICT = OrderedDict()  # type: Dict[str]

try:
    with open(GLOSS_TERMS, 'r') as f:
        LINE_NO = 1
        try:
            # place terms/defs in dictionary
            for line in f:
                term = line.strip().split("\t")  # tab delimited
                GLOSS_DICT[term[0]] = term[1]
                LINE_NO += 1
        except IndexError:
            print("Index error: check line " + str(LINE_NO))
except IOError:
    print("Couldn't read " + GLOSS_TERMS)
    exit(IO_ERROR)

# Read all files in a directory
PATH = HTML_DIR_PATH + "*.html"
FILES = glob.glob(PATH)

GLOSS_TERMS_FOUND = []

for name in FILES:
    try:
        with open(name, "r+") as f:
            # find 1st gloss term and replace with anchor
            for line in f:
                for word in line.split():
                    if word in GLOSS_DICT and word not in GLOSS_TERMS_FOUND:
                        GLOSS_TERMS_FOUND.append(word)
                        key_id = str_to_valid_id(word)
                        word_link = create_word_link(key_id, word, 
                            href_link="http://www.thedevopscourse.com/devops/gloss")
                        data = open(name).read()
                        f.write(re.sub(word, word_link, data, count=1))
    except IOError as exc:
        if exc.errno != errno.EISDIR:  # Do not fail if a directory is found
            raise  # Propagate other kinds of IOError.
