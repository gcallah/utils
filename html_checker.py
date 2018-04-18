"""
Script to check proper nesting and matching of html tags.
Right now, this only cheecks tags that stand alone on a line.
More checks will be added later.
"""

import sys
import urllib.request as req
from html.parser import HTMLParser
from urllib.parse import urlparse, urljoin
import re
import argparse

try:
    from typing import List,Set
except ImportError:
    print("WARNING: Typing module is not find")

ARG_ERROR = 1 # type: int
PARSE_ERROR = 2 # type: int
MAX_LINE = 80 # type: int

tag_stack = [] # type: List[str]
line_no = 0 # type: int
saw_error = False # type: bool

void_tags = {"area", "base", "br", "col", "hr", "img", "input", "link",
             "meta", "param"} # type: Set[str]

def line_msg(): # type: () -> str
    return " at line number " + str(line_no)

class OurHTMLParser(HTMLParser):
    def __init__(self): # type: () -> None
        self.is_in_script_tag = False
        super(OurHTMLParser, self).__init__(convert_charrefs=False)
    
    def handle_starttag(self, tag, attrs): # type: (str, object) -> None
        if tag == "script":
            self.is_in_script_tag = True

        if tag not in void_tags:
            tag_stack.append(tag)

    def handle_endtag(self, close_tag):# type: (str) -> None
        global saw_error # type :bool
        if len(tag_stack) == 0:
            print("ERROR: unmatched close tag "
                  + close_tag + "'" + line_msg())
            saw_error = True
        elif close_tag not in void_tags:
            open_tag = tag_stack.pop()
            if close_tag != open_tag:
                print("ERROR: " +
                      "Close tag '" + close_tag +
                      "' does not match open tag '"
                      + open_tag + "'" + line_msg())
                saw_error = True
        if close_tag is "script":
            self.is_in_script_tag = True

    def handle_data(self, data):# type: (str) -> None
        """
        Here we can look for long lines or other such problems.
        """
        global saw_error # type :bool
        # print(data)
        if len(data) > MAX_LINE:
            print("WARNING: long line found" + line_msg())
        if re.search('\x09', data):
            print("WARNING: tab character found" + line_msg()
                  + "; please uses spaces instead of tabs.")
        if re.search('[<>]', data) and not self.is_in_script_tag:
            print("ERROR: Use &gt; or &lt; instead of < or >"
                  + line_msg())
            saw_error = True

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("html_filename")
    
    args = arg_parser.parse_args()
    
    parser = OurHTMLParser()
    file_nm = args.html_filename

    file = open(file_nm, "r")
    for line in file:
        line_no += 1
        parser.feed(line)
    
    if saw_error:
        exit(PARSE_ERROR)
    else:
        exit(0)
