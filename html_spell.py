"""
Script to check proper nesting and matching of html tags.
Right now, this only cheecks tags that stand alone on a line.
More checks will be added later.
"""

import sys
from html.parser import HTMLParser
import re

ARG_ERROR = 1
SPELL_ERROR = 2

line_no = 0
saw_error = False


def line_msg():
    return " at line number " + str(line_no)


class OurHTMLParser(HTMLParser):
    def __init__(self):
        self.is_in_script_tag = False
        super(OurHTMLParser, self).__init__(convert_charrefs=False)

    def handle_data(self, data):
        """
        Here we can look for long lines or other such problems.
        """
        global saw_error
        # print(data)
        if len(data) > MAX_LINE:
            print("WARNING: long line found" + line_msg())

# when you see an error, set:
#            saw_error = True

parser = OurHTMLParser()

if len(sys.argv) < 2:
    print("Must supply file name to process.")
    exit(ARG_ERROR)
else:
    file_nm = sys.argv[1]

file = open(file_nm, "r")
for line in file:
    line_no += 1
    parser.feed(line)

if saw_error:
    exit(SPELL_ERROR)
else:
    exit(0)
