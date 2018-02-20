"""
Script to check spellings of words in the webpage. Also allows the users
to add words to the dictionary.
"""

import sys
from html.parser import HTMLParser

ARG_ERROR = 1
SPELL_ERROR = 2
DICT_FILE = "English.txt"

line_no = 0
saw_error = False

d = set()
added_words = set()

with open(DICT_FILE, 'r') as f:
    for line in f:
        d.add(line.split()[0].lower())


def line_msg():
    return " at line number " + str(line_no)


class OurHTMLParser(HTMLParser):

    def __init__(self):
        self.is_in_script_tag = False
        super(OurHTMLParser, self).__init__(convert_charrefs=False)

    def is_number(self, word):
        try:
            float(word)
            return True
        except ValueError:
            return False

    def handle_data(self, data):
        web_page_words = data.split()

        for web_page_word in web_page_words:
            word = web_page_word.strip("()[]{}").strip()
            if self.is_number(word):
                continue
            lower_word = word.lower()
            if lower_word not in d:
                valid = False
                while not valid:
                    response = input("Do you want to add %s to dictionary?(yes/no/skip)\n" % word)
                    # 'yes' to improve dictionary
                    if response.lower() == 'yes':
                        added_words.add(lower_word)
                        d.add(lower_word)
                        valid = True
                    # 'skip' strings which are unique (say checksum or names) but not errors
                    elif response.lower() == 'skip':
                        valid = True
                    # 'no' if it is really a typo
                    elif response.lower() == 'no':
                        global saw_error
                        valid = True
                        saw_error = True
                        print("ERROR: '%s' not found in dictionary" % lower_word)
                    else:
                        print("Invalid response, Please try again!")


parser = OurHTMLParser()

if len(sys.argv) < 2:
    print("Must supply file name to process.")
    exit(ARG_ERROR)
else:
    file_nm = sys.argv[1]

file = open(file_nm, "r",)
for line in file:
    line_no += 1
    parser.feed(line)

with open(DICT_FILE, 'a+') as f:
    f.writelines(i + '\n' for i in added_words)
    added_words.clear()

if saw_error:
    exit(SPELL_ERROR)
else:
    exit(0)
