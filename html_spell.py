"""
CLI Tool to check word spelling in an file.

Uses multiple sources of truth for spelling, checked in the following order:
  1. ./data/main-dict.txt, unioned with ./data/custom-dict.txt
  2. the oxford dictionary api

If a user decides that a word, not found in either source,
  ought not to count as a misspelling, they have the opportunity
  to add said word to the dictionary located in ./data/English.txt.

The tool was written to anticipate the following situations,
  and produce appropriate outcomes:
  * Hyphenated compound words, like "{word}-{hyphenated-compound-word}"
    --> Detection: hyphens exist in the string
    --> Solution: split on hyphens, each segment is spellchecked separately
  * Possessives, of the grammar "{word}'s"
    --> Detection: last two characters of string are "'s"
    --> Solution: split on ', word prior is checked.
  * Single-character words
    --> Detection: length is one.
    --> Solution: everything passes.
"""

import os
import subprocess
import urllib.request
from html.parser import HTMLParser
import string
import re
import argparse

try:
    from typing import List, Set  # noqa F401
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
OXFORD_URL = 'https://od-api.oxforddictionaries.com/api/v1/inflections/{}/{}'


class FileChangedException(Exception):
    pass


class SpellingException(Exception):
    pass


def is_word(s, search=re.compile(r'[^a-zA-Z-\']').search):
    return not bool(search(s))


def check_files_exist(*files):
    for file_name in files:
        if not os.path.isfile(file_name):
            print(file_name + " is not a file")
            exit(ARG_ERROR)


def saveAddedWords():
    with open(custom_dict, 'a+') as f:
        f.writelines(i + '\n' for i in added_words)
        added_words.clear()


def spellCheckFile(spell_checker, file_name):
    """
    Description:
        Parses the file with name file, using the passed-in spell_checker.
    Returns:
        Nothing
    """
    code_tag_on = False  # type:bool
    try:
        spell_checker.reset()
        spell_checker.line_num = 0
        with open(file_name, "r", ) as f:
            for line in f:
                spell_checker.line_num += 1
                if "<code>" in line:
                    code_tag_on = True
                if "</code>" in line:
                    code_tag_on = False
                    continue

                if not code_tag_on:
                    spell_checker.feed(line)
    except FileChangedException:
        # Redo spell check for the entire file
        return spellCheckFile(spell_checker, file_name)
    except SpellingException:
        saveAddedWords()
        exit(SPELL_ERROR)


class HTMLSpellChecker(HTMLParser):
    def __init__(self):  # type: () -> None
        self.is_in_script_tag = False
        self.line_num = 0
        super(HTMLSpellChecker, self).__init__(convert_charrefs=False)

    def handle_data(self, html_line):  # type: (str) -> None
        """
        Description:
            This is the core function of the parser,
              called on a line-by-line basis in parser.feed().
            We check if any of the words in the line are not
              in the oxford dictionary, or our local dictionary.
        Exceptions:
            Raises a FileChangedException if the file is edited, so the
              main execution thread can restart the file parsing process.
        """
        # Splits a line by space characters
        words = html_line.split()  # type: List[str]

        # Avoid lines that are just html templates
        if words and words[0] == "{%" and words[len(words)-1] == "%}":
            return

        for word in words:
            # strip punctuation
            word = word.strip(string.punctuation).strip()

            if "-" in word:
                # If there are hyphens in the word, we check each one
                for word in word.split("-"):
                    self.checkWord(word)
            else:
                self.checkWord(word)

    def handle_bad_word(self, word):
        """
        Description:
            A REPL loop allowing the user to handle their misspelt word.
        Returns:
            Nothing normally
        Raises:
            FileChangedException if the edit option was chosen
        """
        if not interactive_mode:
            raise SpellingException("Mis-spelled word: " + word)
        validResponse = False  # type: bool
        while not validResponse:
            response = input(
                "How would you like to handle the bad word {}?\n".format(word)
                + "1. Add as valid word to dictionary (1/a/add)\n"
                + "2. Skip error, because word is a unique string (2/s/skip)\n"
                + "3. Edit file, to fix the word (3/e/edit)\n"
                + "4. Exit the spell-checker for this file."
                + " Will result in a non-zero exit code. (4/c/close)\n"
                + ">>")
            response = response.lower()
            if response == 'add' or response == 'a' or response == '1':
                added_words.add(word)
                word_set.add(word)
                return None
            elif response == 'skip' or response == 's' or response == '2':
                return None
            elif response == 'edit' or response == 'e' or response == '3':
                # This opens up vim with all instances of the word highlighted.
                subprocess.call([
                    'vimdiff',
                    '+{}'.format(self.line_num),
                    '-c', 'match Search /{}/'.format(word), file_name
                ])
                raise FileChangedException
            elif response == 'close' or response == 'c' or response == '4':
                raise SpellingException("Mis-spelled word: " + word)
            else:
                print("Invalid response, Please try again!")

    def isWordInOxfordDictionary(self, lower_word):
        try:
            return urllib.request.urlopen(
                urllib.request.Request(
                    url=OXFORD_URL.format(language, lower_word),
                    headers={'app_id': app_id, 'app_key': app_key}
                )).getcode() == 200
        except urllib.error.URLError:
            return False

    def isPossessive(self, word):
        return '\'s' == word[len(word)-2:]

    def checkWord(self, word):
        """
        Description:
            Checks whether is a string is a valid word or not.
            If a word is spelt incorrectly, calls handle_bad_word.
            See module docstring to see what kinds of bad strings are caught.
        Returns:
            None
        Raises:
            Makes no attempt to catch exceptions from handle_bad_word.
        """
        if word is "":
            return
        if len(word) == 1:
            return
        if self.isPossessive(word):
            return self.checkWord(word[:len(word)-2])
        if not is_word(word):
            return
        if not strict_mode and word[0].isupper():
            return

        lower_word = word.lower()  # type: (str)

        if (lower_word not in word_set
                and not self.isWordInOxfordDictionary(lower_word)):
            self.handle_bad_word(lower_word)


interactive_mode = False  # type: bool
strict_mode = False  # type: bool
file_name = None
main_dict = None
custom_dict = None

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("file_name", help="html file to be parsed")
    arg_parser.add_argument("main_dict", help="main dictionary file")
    arg_parser.add_argument("custom_dict", help="custom dictionary file")
    arg_parser.add_argument(
        "-i", help="enable interactive spell-checking", action="store_true")
    arg_parser.add_argument("-s", help="strict mode checks capitalized words",
                            action="store_true")
    args = arg_parser.parse_args()
    interactive_mode = args.i
    strict_mode = args.s
    file_name = args.file_name
    main_dict = args.main_dict
    custom_dict = args.custom_dict

# Make sure all the files exist, before doing anything heavy
check_files_exist(file_name, main_dict, custom_dict)

# Load words from Dictionary files
word_set = set()
with open(main_dict, 'r') as f:
    for line in f:
        word_set.add(line.split()[0].lower())
with open(custom_dict, 'r') as f:
    for line in f:
        word_set.add(line.split()[0].lower())

# Execute the spellchecker
added_words = set()
parser = HTMLSpellChecker()
spellCheckFile(parser, file_name)

saveAddedWords()

exit(0)
