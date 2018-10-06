"""
Script to check spellings of words in a web page. Also allows the users
to add words to a custom dictionary.
"""

import json
import os
import subprocess
import requests
from html.parser import HTMLParser
import string
import re
import argparse

try:
    from typing import List, Set
except ImportError:
    print(
        "WARNING: Typing module is not found! Kindly install the latest "
        "version of python!")

ARG_ERROR = 1  # type: int
SPELL_ERROR = 2  # type: int

# Application keys for Oxford dictionary API
app_id = '4dcc2c67'
# Should we be storing API keys in a public repo? 
# We might want to investigate https://www.vaultproject.io/
app_key = 'c7d48867f7506e51e70507d85bc9cbe6'
language = 'en'


def is_word(s, search=re.compile(r'[^a-zA-Z-\']').search):
    return not bool(search(s))


def check_file(*files):
    for file in files:
        if not os.path.isfile(file):
            print(file + " is not a file")
            exit(ARG_ERROR)

def spellCheckFile(spellChecker, fn):
    """
    Description:
        Parses the file with name fn, using the passed-in spellChecker.
    Returns:
        None if the file was spell-checked without any hiccups
    Raises:
        If an irrecoverable error was encountered
    """
    code_tag_on = False  # type:bool
    line_num = 0
    try:
        spellChecker.reset()
        with open(fn, "r", ) as f:
            for line in f:
                if "<code>" in line:
                    code_tag_on = True
                if "</code>" in line:
                    code_tag_on = False
                    continue

                if not code_tag_on:
                    spellChecker.feed(line)
                line_num += 1
    except FileChangedException:
        return spellCheckFile(spellChecker, fn)

class FileChangedException(Exception):
    pass

class OurHTMLParser(HTMLParser):
    def handle_bad_word(self, word):
        """
        Description:
            A REPL loop allowing the user to handle their misspelt word.
        Returns:
            Nothing normally
        Raises:
            FileChangedException if the edit option was chosen
        """
        validResponse = False  # type: bool
        while not validResponse:
            response = input(
                "How would you like to handle the bad word {}?\n".format(word) +
                "1. Add as valid word to dictionary (1/a/add)\n" +
                "2. Skip error, because words is a unique string (2/s/skip)\n" +
                "3. Edit file, to fix the word (3/e/edit)\n"+ 
                "4. Close the spell-checker for this file (4/c/close)\n" +
                ">>")
            if response.lower() == 'add' or response.lower() == 'a' or response == '1':
                added_words.add(word)
                d.add(word)
                return None
            elif response.lower() == 'skip' or response.lower() == 's' or response == '2':
                return None
            elif response.lower() == 'edit' or response.lower() == 'e' or response == '3':
                # This opens up vim, at the first instance of the troublesome word, with all instances highlighted.
                subprocess.call(['vimdiff', '+{}'.format(line_num), '-c', '/ {} '.format(word), file_nm])
                raise FileChangedException
            elif response.lower() == 'close' or response.lower() == 'c' or response == '4':
                exit(0)
            else:
                print("Invalid response, Please try again!")

    def __init__(self):  # type: () -> None
        self.is_in_script_tag = False
        super(OurHTMLParser, self).__init__(convert_charrefs=False)

    def isWordInOxfordDictionary(self,lower_word):
        url = ('https://od-api.oxforddictionaries.com/api/v1/inflections/'
               + language + '/' + lower_word)
        r = requests.get(url, headers={'app_id': app_id, 'app_key': app_key})
        return r.status_code

    def checkWord(self, word):
        if '\'s' in word:
            word = word[:word.index('\'')]
        if word is "":
            return
        if not is_word(word):
            return
        if len(word) == 1:
            return
        if not strict_mode and word[0].isupper():
            return

        lower_word = word.lower()  # type: (str)

        if lower_word not in d and self.isWordInOxfordDictionary(lower_word) != 200:
            self.handle_bad_word(lower_word)  # raises if edit is chosen

    def handle_data(self, data):  # type: (str) -> None
        """
        Description:
            This is the core function of the parser, called on a line-by-line basis in parser.feed().
            We check if any of the words in the line are not in the oxford dictionary, or our local dictionary.
        Exceptions:
            Raises a FileChangedException if the file is edited in handle_bad_word, 
              so that the main execution thread can restart the file parsing process.
        """
        web_page_words = data.split()  # type: List[str]

        if web_page_words and web_page_words[0] == "{%" and web_page_words[len(web_page_words)-1] == "%}":
            return

        for web_page_word in web_page_words:
            word = web_page_word.strip(string.punctuation).strip() # strip other punctuations
            if "-" in web_page_word:
                for word in web_page_word.split("-"):
                    self.checkWord(word)
            else:
                self.checkWord(word)

line_num = 0
exit_error = False # type: bool
strict_mode = False # type: bool
file_nm = None
main_dict = None
custom_dict = None

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("file_nm", help="html file to be parsed")
    arg_parser.add_argument("main_dict", help="main dictionary file")
    arg_parser.add_argument("custom_dict", help="custom dictionary file")
    arg_parser.add_argument("-e", help="enable exit error", action="store_true")
    arg_parser.add_argument("-s", help="strict mode checks capitalized words",
                            action="store_true")
    args = arg_parser.parse_args()
    exit_error = args.e
    strict_mode = args.s
    file_nm = args.file_nm
    main_dict = args.main_dict
    custom_dict = args.custom_dict

check_file(file_nm, main_dict, custom_dict)
saw_error = False  # type: bool
d = set()  # type: Set[str]
added_words = set()  # type: Set[str]
parser = OurHTMLParser()

# Loading words from main Json Dictionary into the python set data structure
with open(main_dict, 'r') as f:
    d = set(json.load(f).keys())

# Loading words from custom Dictionary into the python set data structure
with open(custom_dict, 'r') as f:
    d.add(line.split()[0].lower() for line in f)

spellCheckFile(parser, file_nm)

with open(custom_dict, 'a+') as f:
    f.writelines(i + '\n' for i in added_words)
    added_words.clear()

if saw_error and exit_error:
    exit(SPELL_ERROR)
else:
    exit(0)
