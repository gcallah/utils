"""
Script to check spellings of words in the webpage. Also allows the users
to add words to the dictionary.
"""

import sys
from html.parser import HTMLParser

ARG_ERROR = 1
SPELL_ERROR = 2

line_no = 0
saw_error = False

d = set()
addedWords = set()

with open('English.txt', 'r') as f:
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
        webPageWords = data.split()

        for webPageWord in webPageWords:
            word = webPageWord.strip("()[]{}").strip()
            if self.is_number(webPageWord):
                continue
            lowerWord = word.lower()
            if lowerWord not in d:
                valid = False
                while not valid:
                    response = input("Do you want to add the word "+ webPageWord+ "?(yes/no/skip)\n")
                    # 'yes' to improve dictionary
                    if response.lower() == 'yes':
                        addedWords.add(lowerWord)
                        d.add(lowerWord)
                        valid = True
                    # 'skip' strings which are unique (say checksum) but not errors
                    elif response.lower() == 'skip':
                        valid = True
                    # 'no' if it is really a typo
                    elif response.lower() == 'no':
                        global saw_error
                        valid = True
                        saw_error = True
                        print("ERROR: '%s' not found in dictionary" % lowerWord)
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

with open('English.txt', 'a+') as f:
    f.writelines(i+'\n' for i in addedWords)
    addedWords.clear()

if saw_error:
    exit(SPELL_ERROR)
else:
    exit(0)
