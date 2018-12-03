#!/usr/bin/python
"""
Script to check proper nesting and matching of html tags.
"""

from html.parser import HTMLParser
import re
import argparse

try:
    from typing import List, Set, Dict  # noqa F401
except ImportError:
    print("WARNING: Typing module is not found.")

ARG_ERROR = 1   # type: int
PARSE_ERROR = 2   # type: int
MAX_LINE = 80   # type: int

tag_stack = []   # type: List[str]
line_no = 0   # type: int
saw_error = False   # type: bool
tag_error = False   # type: bool
tag_check = False   # type: bool

void_tags = {"area", "base", "br", "col", "hr", "img", "input", "link",
             "meta", "param"}  # type: Set[str]

in_sig_tag = {"pre": False, "script": False, "a": False,
              "style": False}  # that's all for now!


def line_msg():  # type: () -> str
    """
    A little func to regularize reporting line #s for errors.
    """
    return " at line number " + str(line_no)


class OurHTMLParser(HTMLParser):
    """
    Our descendant of base HTMLParser class: we override just the methods we
    need to.
    """
    def __init__(self):  # type: () -> None
        super(OurHTMLParser, self).__init__(convert_charrefs=False)

    def handle_starttag(self, tag, attrs):  # type: (str, object) -> None
        """
        This is a callback function that is used by HTMLParser for start tags:
            it is called!
        """
        if tag in in_sig_tag:
            in_sig_tag[tag] = True
        if tag not in void_tags:
            tag_stack.append(tag)

    def handle_endtag(self, tag):  # type: (str) -> None
        global saw_error  # type :bool
        if not tag_stack:
            print("ERROR: unmatched close tag " + tag + "'" + line_msg())
            saw_error = True
        elif tag not in void_tags:
            open_tag = tag_stack.pop()
            if tag != open_tag:
                print("ERROR: " +
                      "Close tag '" + tag +
                      "' does not match open tag '" + open_tag
                      + "'" + line_msg())
                saw_error = True
            if tag in in_sig_tag:
                in_sig_tag[tag] = False

    def handle_data(self, data):  # type: (str) -> None
        """
        Here we can look for long lines or other such problems.
        """
        global saw_error  # type :bool
        if(not in_sig_tag["pre"] and not in_sig_tag["a"] and not
           in_sig_tag["script"]):
            if len(data) > MAX_LINE:
                print("WARNING: long line found" + line_msg())
                print(data)
        if re.search('\x09', data):
            print("WARNING: tab character found"
                  + line_msg() + "; please uses spaces instead of tabs.")
        if not in_sig_tag["script"] and re.search('[<>]', data):
            print("ERROR: Use &gt; or &lt; instead of < or >"
                  + line_msg())
            saw_error = True


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("html_filename")
    arg_parser.add_argument("-t", action="store_true")

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
