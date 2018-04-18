"""
Script to check spellings of words in the web page. Also allows the users
to add words to the dictionary.
"""

import sys
from html.parser import HTMLParser
import string
import re
import os.path

try:
    from typing import List,Set
except ImportError:
    print("WARNING: Typing module is not found! Kindly install the latest version of python!")

ARG_ERROR = 1 # type: int
SPELL_ERROR = 2 # type: int


class OurHTMLParser(HTMLParser):
    def __init__(self): # type: () -> None
        self.is_in_script_tag = False
        super(OurHTMLParser, self).__init__(convert_charrefs=False)

    def handle_data(self, data): # type: (str) -> None
        web_page_words = data.split() # type: List[str]

        for web_page_word in web_page_words:
            # strip other punctuations
            word = web_page_word.strip(string.punctuation).strip() # type :str
            if not is_word(web_page_word):
                continue
            if len(web_page_word) == 1:
                continue
            lower_word = word.lower() # type: (str)
            if lower_word not in d:
                valid = False # type: bool
                while not valid:
                    response = input("Do you want to add %s to dictionary?("
                                     "yes/no/skip)\n" % word)
                    # 'yes' to improve dictionary
                    if response.lower() == 'yes':
                        added_words.add(lower_word)
                        d.add(lower_word)
                        valid = True
                    # 'skip' unique strings (checksum/names) but not errors
                    elif response.lower() == 'skip':
                        valid = True
                    # 'no' if it is really a typo
                    elif response.lower() == 'no':
                        global saw_error # type :bool
                        valid = True
                        saw_error = True
                        print("ERROR: " + word + line_msg())
                    else:
                        print("Invalid response, Please try again!")


if len(sys.argv) != 4:
    print("USAGE: html_spell.py fileToProcess mainDictionary customDictionary")
    exit(ARG_ERROR)

if not os.path.isfile(sys.argv[1]):
    print(sys.argv[1] + "is not a file")
    exit(ARG_ERROR)

if not os.path.isfile(sys.argv[2]):
    print(sys.argv[2] + "is not a file")
    exit(ARG_ERROR)

if not os.path.isfile(sys.argv[3]):
    print(sys.argv[3] + "is not a file")
    exit(ARG_ERROR)

file_nm = sys.argv[1]
main_dict = sys.argv[2]
custom_dict = sys.argv[3]
line_no = 0 # type :int
saw_error = False # type: bool
d = set() #type: Set[str]
added_words = set() #type: Set[str]
code_tag_on = False #type:bool
parser = OurHTMLParser()


# Loading words from main Dictionary into the python set data structure

with open(main_dict, 'r') as f:
    for line in f:
        d.add(line.split()[0].lower())

# Loading words from custom Dictionary into the python set data structure
with open(custom_dict, 'r') as f:
    for line in f:
        d.add(line.split()[0].lower())


def is_word(s, search=re.compile(r'[^a-zA-Z-\']').search):
    return not bool(search(s))


def line_msg():# type: () -> str
    return " at line number " + str(line_no)


with open(file_nm, "r", ) as f:
    for line in f:
        if "<code>" in line:
            code_tag_on = True

        if "</code>" in line:
            code_tag_on = False
            continue

        if not code_tag_on:
            parser.feed(line)
        line_no += 1

with open(custom_dict, 'a+') as f:
    f.writelines(i + '\n' for i in added_words)
    added_words.clear()

if saw_error:
    exit(SPELL_ERROR)
else:
    exit(0)

