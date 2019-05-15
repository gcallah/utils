#!/usr/bin/env python3

"""
The aim of this script is to take a suitably marked up .cpp
file and turn it into a web page.
"""

import sys
import re
import pygments
import pygments.formatters
from pygments.lexers.c_cpp import CppLexer

import pylib.create_page as pyl
import pylib.html_tags as html

CODE_SPAN = '<span class="code">'
CLOSE_SPAN = '</span>'

COMMENT_START = re.compile(r"^\s*/\*\s*$")
COMMENT_END = re.compile(r"^\s*\* \*/\s*$")


class InlineHtmlFormatter(pygments.formatters.HtmlFormatter):
    """
    Use pygments to format html code inline.
    """
    def wrap(self, source, _outfile):
        return self._wrap_code(source)

    @staticmethod
    def _wrap_code(source):
        yield from source


def main():
    if len(sys.argv) < 2:
        print("Must supply a C++ file.")
        exit(1)

    cpp_file = sys.argv[1]
    cpp_lexer = CppLexer()

    print(pyl.ptml_start_stuff(cpp_file))
    with open(cpp_file, 'r') as inp:
        # we will find ourselves in "regular" text (long comments)
        # or in code.
        text = ""
        in_reg_text = False
        in_code_span = False
        consec_blanks = 0
        for line in inp:
            if COMMENT_START.match(line):
                if len(text):
                    # no extra line after code!
                    print(html.code_par(text), end="")
                in_reg_text = True
                text = ""
                continue
            elif COMMENT_END.match(line):
                in_reg_text = False
                print(html.par(text))
                text = ""
                continue
            if in_reg_text:
                line = line.replace("*", "")
                proc_line = ""
                for c in line:
                    if c == '`':  # back tick means code!
                        if in_code_span:
                            in_code_span = False
                            proc_line += CLOSE_SPAN
                        else:
                            in_code_span = True
                            proc_line += CODE_SPAN
                    else:
                        proc_line += c
                line = proc_line
            else:
                if not line.strip():
                    consec_blanks += 1
                if consec_blanks >= 2:
                    consec_blanks = 0
                    continue
            if not in_reg_text:
                line = pygments.highlight(line, cpp_lexer,
                                   InlineHtmlFormatter())
            text += line

        if len(text):
            print(html.code_par(text))

    print(pyl.html_end_stuff())


if __name__ == '__main__':
    main()
