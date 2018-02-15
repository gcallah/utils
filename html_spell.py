"""
Script to check spellings of words in the webpage. Also allows the users
to add words to the dictionary.
"""

import sys
from html.parser import HTMLParser
import re
line_no = 0

d = []
addedWords = []
dictionary = open("English.txt", "r")
words = dictionary.readlines()

for word in words:
    d.append(word.split()[0].lower())

def line_msg():
    return " at line number " + str(line_no)


class OurHTMLParser(HTMLParser):
    def __init__(self):
        self.is_in_script_tag = False
        super(OurHTMLParser, self).__init__(convert_charrefs=False)

    def handle_data(self, data):
        webPageWords = data.split()

        for webPageWord in webPageWords:
            lowerWord = webPageWord.lower()
            if lowerWord not in d and lowerWord not in addedWords:
                response = input("Do you want to add the word "+ webPageWord+ "?(y/n)")

                if response == 'y':
                    addedWords.append(lowerWord)

        d.append(addedWords)
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

