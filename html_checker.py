"""
Script to check proper nesting and matching of html tags.
"""

from html.parser import HTMLParser
import re
import argparse

try:
    from typing import List, Set, Dict
except ImportError:
    print("WARNING: Typing module is not find")

ARG_ERROR = 1 # type: int
PARSE_ERROR = 2 # type: int
MAX_LINE = 80 # type: int
SCRIPT = "script"

tag_stack = [] # type: List[str]
line_no = 0 # type: int
saw_error = False # type: bool
tag_error = False # type: bool
tag_check = False # type: bool

void_tags = {"area", "base", "br", "col", "hr", "img", "input", "link",
             "meta", "param"} # type: Set[str]

tags_priority = {"h1" : 4, "h2" : 3, "h3" : 2, "p" : 0} # type: Dict[str , int]

def line_msg(): # type: () -> str
    """
    A little func to regularize reporting line #s for errors.
    """
    return " at line number " + str(line_no)

class OurHTMLParser(HTMLParser):
    """
    Our descendant of base HTMLParser class: we override just the methods we
    need to.
    """
    def __init__(self): # type: () -> None
        self.is_in_script_tag = False
        super(OurHTMLParser, self).__init__(convert_charrefs=False)

    def handle_starttag(self, tag, attrs): # type: (str, object) -> None
        """
        This is a callback function that is used by HTMLParser for start tags:
            it is called!
        """
        if tag == SCRIPT:
            self.is_in_script_tag = True

        if tag not in void_tags:
            if tag_stack:
                err_tag = self.check_tag_priority(tag_stack, tag)
                # if (tag_error and not saw_error):
                if (tag_check and tag_error):
                    print("ERROR: tag priority mismatch, detected "
                          + tag + " tag within "
                          + err_tag + " tag " + line_msg())

            tag_stack.append(tag)

    def check_tag_priority(self, pre_tag_stack,
                           this_tag): # type: (List[str], str) -> str
        """
        What is this function going to do?
        """
        global tag_error
        for pre_tag in reversed(pre_tag_stack):
            if (pre_tag in tags_priority and this_tag in tags_priority):
                if tags_priority[this_tag] >= tags_priority[pre_tag]:
                    tag_error = True
                    return pre_tag
        return this_tag

    def handle_endtag(self, tag): # type: (str) -> None
        global saw_error # type :bool
        if not tag_stack:
            print("ERROR: unmatched close tag " + tag + "'" + line_msg())
            saw_error = True
        elif tag not in void_tags:
            open_tag = tag_stack.pop()
            if tag != open_tag:
                print("ERROR: " +
                      "Close tag '" + tag +
                      "' does not match open tag '"
                      + open_tag + "'" + line_msg())
                saw_error = True
        if tag is SCRIPT:
            self.is_in_script_tag = False

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
