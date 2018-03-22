"""
Script to check spellings of words in the web page. Also allows the users
to add words to the dictionary.
"""

import sys
from html.parser import HTMLParser
import string
import re

ARG_ERROR = 1
SPELL_ERROR = 2


class OurHTMLParser(HTMLParser):
    def __init__(self):
        self.is_in_script_tag = False
        super(OurHTMLParser, self).__init__(convert_charrefs=False)

    def is_word(self, strg, search=re.compile(r'[^a-zA-Z-]').search):
        return not bool(search(strg))

    def handle_data(self, data):
        web_page_words = data.split()

        for web_page_word in web_page_words:
            if web_page_word == "":
                continue

            if len(web_page_word) == 1 and is_symbol(web_page_word):
                continue

            if not self.is_word(web_page_word):
                continue

            # strip other punctuations
            word = web_page_word.strip(string.punctuation).strip()
            if is_number(word):
                continue
            lower_word = word.lower()
            if lower_word not in d:
                valid = False
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
                        global saw_error
                        valid = True
                        saw_error = True
                        print("ERROR: " + word + line_msg())
                    else:
                        print("Invalid response, Please try again!")


parser = OurHTMLParser()

if len(sys.argv) != 4:
    print("USAGE: html_spell.py fileToProcess mainDictionary customDictionary")
    exit(ARG_ERROR)

file_nm = sys.argv[1]
main_dict = sys.argv[2]
custom_dict = sys.argv[3]
line_no = 0
saw_error = False
d = set()
added_words = set()

# Loading words from main Dictionary into the python set data structure
with open(main_dict, 'r') as f:
    for line in f:
        d.add(line.split()[0].lower())

# Loading words from custom Dictionary into the python set data structure
with open(custom_dict, 'r') as f:
    for line in f:
        d.add(line.split()[0].lower())


def line_msg():
    return " at line number " + str(line_no)


def is_number(word):
    try:
        float(word)
        return True
    except ValueError:
        return False


def is_symbol(char):
    if char in string.punctuation:
        return True
    else:
        return False


with open(file_nm, "r", ) as f:
    for line in f:
        line_no += 1
        parser.feed(line)

with open(custom_dict, 'a+') as f:
    f.writelines(i + '\n' for i in added_words)
    added_words.clear()

if saw_error:
    exit(SPELL_ERROR)
else:
    exit(0)
