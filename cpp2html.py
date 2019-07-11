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
        in_italics = False
        in_bold = False
        prev_is_star = False
        consec_blanks = 0
        num_hashtags = 0;
        in_header = False;
        header_number = 0;
        for line in inp:
            first_star = True
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
                # line = line.replace("*", "")
                proc_line = ""
                for c in line:
                    if c == '`':  # back tick means code!
                        if not in_code_span:
                            in_code_span = True
                            proc_line += CODE_SPAN
                        else:
                            in_code_span = False
                            proc_line += CLOSE_SPAN
                    elif c == '*':  # * means italics! ** means bold!
                        if first_star:
                            first_star = False
                        elif prev_is_star:
                            if not in_bold:
                                in_bold = True
                                proc_line += "<b>"
                            else:
                                in_bold = False
                                proc_line += "</b>"
                            prev_is_star = False
                        else:
                            prev_is_star = True
                    elif c == '#':   #headers. # = h1, ## = h2, etc.
                        if not in_header:
                            num_hashtags += 1
                        else:
                            num_hashtags -= 1
                            if num_hashtags == 0:
                                proc_line += "</h" + str(header_num) + ">"
                                in_header = False
                                header_num = 0
                    else:
                        if not in_header:
                            if num_hashtags > 0:
                                proc_line += "<h" + str(num_hashtags) + ">"
                                in_header = True
                                header_num = num_hashtags
                        if prev_is_star:
                            if not in_italics:
                                in_italics = True
                                proc_line += "<i>"
                            else:
                                in_italics = False
                                proc_line += "</i>"
                            prev_is_star = False
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
