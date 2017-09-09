"""
Script to check proper nesting and matching of html tags.
Right now, this only cheecks tags that stand alone on a line.
More checks will be added later.
"""

import sys
from html.parser import HTMLParser

ARG_ERROR = 1
MATCH_ERROR = 2
MAX_LINE = 80

tag_stack = []
line_no = 0
saw_error = False
void_tags = {"area", "base", "br", "col", "hr", "img", "input", "link", "meta", "param"}


class OurHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag not in void_tags:
            tag_stack.append(tag)

    def handle_endtag(self, close_tag):
        if close_tag not in void_tags:
            open_tag = tag_stack.pop()
            if close_tag != open_tag:
                print("Close tag '" + close_tag + "' does not match open tag '"
                      + open_tag + "' at line number " + str(line_no))
                saw_error = True

    def handle_data(self, data):
        """
        Here we can look for long lines or other such problems.
        """
        if len(data) > MAX_LINE:
            print("WARNING: long line found at line number " + str(line_no))


parser = OurHTMLParser()

if len(sys.argv) < 2:
    print("Must supply file name to process.")
    exit(ARG_ERROR)
else:
    file_nm = sys.argv[1]

file = open(file_nm, "r") 
for line_no, line in enumerate(file): 
    parser.feed(line)

if saw_error:
    exit(MATCH_ERROR)
else:
    exit(0)
