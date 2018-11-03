"""
Glossary Linker: Takes in a directory of html files and 
modifies each file to include anchor links on the 
first instance of a term.
"""

import argparse

ARG_ERROR = 1  # type: int
IO_ERROR = 2  # type: int

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("html_dir", help="html directory to be parsed")
    args = arg_parser.parse_args()
    txt_file = args.html_dir