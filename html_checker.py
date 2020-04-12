#!/usr/bin/python
"""
Script to check proper nesting and matching of html tags.
"""

from html.parser import HTMLParser
from html_content_spec import content_spec, _ANY_CONTENT, _NO_CONTENT
import re
import argparse

try:
    from typing import List, Set, Dict  # noqa F401
except ImportError:
    print("WARNING: Typing module is not found.")

DEV_FEATURE_ON = False # type: bool

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

def is_tag_in_spec(tag): # (str) -> bool
    """
    func to see if the tag is in content_spec
    """
    if tag not in content_spec and tag not in content_spec["_EXCEPTIONS"]:
        print("WARNING: " + tag + " not found in content_spec")
        # Not necessarily an error, more like a warning
        # saw_error = True
        return False
    return True
        

def is_valid_content(tag, attrs): # type: (str, str) -> bool
    """
    Checks if the given tag is valid or can be placed within the parent tag
    """
    # print("IS_VALID_CONTENT ==========")
    # print("TAG: " + tag)
    # print("tag_stack: " + str(tag_stack))
    # print("tag_stack len: " + str(len(tag_stack)))

    # If we don't know about the tag, we will not do any checks
    # Just inform the user
    if not is_tag_in_spec(tag):
        return True

    if len(tag_stack) > 0 and tag not in content_spec["_EXCEPTIONS"]:

        doWhile = True
        parentIndex = -1
        parentModel = []

        # Processes content models that are transparent
        # Must get model from an older parent
        while doWhile or "transparent" in parent_model:
            doWhile = False

            parent_tag = tag_stack[parentIndex]

            if is_tag_in_spec(parent_tag) and parent_tag not in content_spec["_EXCEPTIONS"]:
                parent_model = content_spec[parent_tag]["content_model"]            
                parentIndex-=1
            else:
                # Parent tag not in spec or is part of exceptions, default to True
                return True

        tag_categories = content_spec[tag]["categories"]

        for model in parent_model:  
            for category in tag_categories:
                # If parent expects no children tags, then tag is illegal
                if model == _NO_CONTENT:
                    return False

                if model == _ANY_CONTENT or model == tag or model == category:
                    return True

        return False
    return True


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
            if DEV_FEATURE_ON:
                if is_valid_content(tag, attrs) == False:
                    print("ERROR: illegal tag" + line_msg() + ". "
                            + tag + " cannot be nested in " + tag_stack[-1])
                    saw_error = True
            tag_stack.append(tag)

    def handle_endtag(self, tag):  # type: (str) -> None
        global saw_error  # type :bool
        if not tag_stack:
            print("ERROR: unmatched close tag '" + tag + "'" + line_msg())
            saw_error = True
        elif tag not in void_tags:
            open_tag = tag_stack.pop()
            if tag != open_tag:
                print("ERROR: " +
                      "Close tag '" + tag +
                      "' does not match open tag '" + open_tag +
                      "'" + line_msg())
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
            print("WARNING: tab character found" + line_msg() +
                  "; please uses spaces instead of tabs.")
        if not in_sig_tag["script"] and re.search('[<>]', data):
            print("ERROR: Use &gt; or &lt; instead of < or >" + line_msg())
            saw_error = True


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("html_filename")
    arg_parser.add_argument("-t", action="store_true")
    arg_parser.add_argument("-d", action="store_true", help="turns on dev features")

    args = arg_parser.parse_args()

    parser = OurHTMLParser()
    file_nm = args.html_filename
    tag_check = args.t

    if args.d:
        DEV_FEATURE_ON = True

    file = open(file_nm, "r")
    for line in file:
        line_no += 1
        parser.feed(line)

    if saw_error:
        exit(PARSE_ERROR)
    else:
        exit(0)
