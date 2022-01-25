#!/usr/bin/python3
"""
Script to check proper nesting and matching of html tags.
Using HTML5LIB: https://github.com/html5lib/html5lib-python

This conforms to the spec: https://html.spec.whatwg.org/
"""

import html5lib
import argparse


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("html_filename")

    args = arg_parser.parse_args()

    file_nm = args.html_filename

    with open(file_nm, "rb") as f:
        parser = html5lib.HTMLParser(strict=True)
        document = parser.parse(f)
