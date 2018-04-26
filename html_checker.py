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
    from typing import List,Set,Dict
except ImportError:
    print("WARNING: Typing module is not find")

ARG_ERROR = 1 # type: int
PARSE_ERROR = 2 # type: int
MAX_LINE = 80 # type: int

tag_stack = [] # type: List[str]
line_no = 0 # type: int
saw_error = False # type: bool
tag_error = False # type: bool
tag_check = False # type: bool

void_tags = {"area", "base", "br", "col", "hr", "img", "input", "link",
             "meta", "param"} # type: Set[str]

tags_priority = {"h1" : 4, "h2" : 3, "h3" : 2, "p" : 0} # type: Dict[str , int]

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
            if (len(tag_stack) > 0):
                err_tag = self.check_tag_priority(tag_stack, tag)
                # if (tag_error and not saw_error):
                if (tag_check and tag_error):
                    print("ERROR: tag priority mismatch, detected "
                            + tag + " tag within " + 
                            err_tag + " tag " + line_msg())

            tag_stack.append(tag)

    def check_tag_priority(self, pre_tag_stack, this_tag): # type: (List[str], str) -> str
        global tag_error 
        for pre_tag in reversed(pre_tag_stack):
            if (pre_tag in tags_priority and this_tag in tags_priority):
                if(tags_priority[this_tag] >= tags_priority[pre_tag]):
                    tag_error = True
                    return pre_tag
        return this_tag

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
    arg_parser.add_argument("-t", action = "store_true")

    args = arg_parser.parse_args()
    
    parser = OurHTMLParser()
    file_nm = args.html_filename
    tag_check = args.t

    file = open(file_nm, "r")
    for line in file:
        line_no += 1
        parser.feed(line)
    
    if saw_error:
        exit(PARSE_ERROR)
    else:
        exit(0)
