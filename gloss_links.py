#!/usr/bin/python
"""
for testing run:
(python3 gloss_links.py test_data/gloss_key.txt test_data --lf
"test_data/gloss_links_inp1.txt" "test_data/gloss_links_inp2.txt")

--------- for understanding code --------
Each file is opened only once now.
The data structure used in new version
is a bit complicated:
-> keyword_context is a dictionary where key
is key/glossary from gloss_list and value is another dictionary
-> in the nested dictionary key is name of
files and value is list of context for that file.
{keyword: {filenm:[context,...,contxt],..., filenm:
[context,...,contxt]},.....,keyword:
{filenm:[context,contxt],..., filenm:[context,context]}}
--------- for understanding code ---------
"""


import argparse
import re
ARG_ERROR = 1  # type: int


def process_file(filenm, keyword_context, gloss_list):
    """
    Args: filenm and contexts_per_file
    returns: None
    """

    try:
        with open(filenm, 'r') as txt:
            for keyword in gloss_list:
                for line in txt:
                    # splits into a list
                    if keyword in line:
                        # line=re.sub(r'[^\w\s]','',str(line.strip())).split()
                        line = line.strip().split(" ")
                        context = None
                        index_list = []

                        for index, word in enumerate(line):
                            word = re.sub(r'[^\w\s]', '', str(word))
                            if keyword == word:
                                index_list.append(index)

                        for index in index_list:
                            # if keyword appears more than once in a line
                            key_index = index

                            if 0 < key_index < len(line) - 1:
                                context = (line[key_index-1] + " " +
                                           line[key_index] + " " +
                                           line[key_index+1])

                            elif key_index == 0:
                                if len(line) > 1:
                                    context = (line[key_index] + " " +
                                               line[key_index+1])
                                else:
                                    context = line[key_index]

                            elif key_index == len(line) - 1:
                                context = (line[key_index - 1] + " " +
                                           line[key_index])

                            if keyword not in keyword_context:
                                keyword_context[keyword] = {}

                            file_per_keyword = keyword_context[keyword]
                            if filenm not in file_per_keyword:
                                keyword_context[keyword][filenm] = []

                            keyword_context[keyword][filenm].append(context)
                txt.seek(0)

    except IOError as ioe:
        print("Error opening file: %s; exception: %s", (filenm, str(ioe)))


def process_args():
    """
    Parses command line args and returns:
        keyword_file, file_list
    """
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("gloss_key")
    arg_parser.add_argument("outdir")
    arg_parser.add_argument(
        "--lf",  # you need to add "--lf" flag in command line
        nargs="*",
        type=str,
        default=[],
    )
    args = arg_parser.parse_args()
    return (args.gloss_key, args.outdir, args.lf)


def output_context(outdir, keyword_context):
    """
        output context of a keyword
        Args: outdir, keyword, context
        Returns: None
    """
    for keyword in keyword_context:
        output_name = outdir + "/" + keyword + ".txt"
        with open(output_name, 'w') as files:
            files.write(keyword + " found in: \n")
            temp = keyword_context[keyword]
            for filenm, context_list in temp.items():
                for context in context_list:
                    files.write("    " + filenm + ": " + context + "\n")
                files.write("\n")


if __name__ == '__main__':
    # get command line params:
    (KEYWORD_FILE_LIST, OUTDIR, FILE_LIST) = process_args()

    GLOSS_LISTS = []
    KEYWORD_CONTEXTS = {}
    # first get all the gloss keywords
    with open(KEYWORD_FILE_LIST, 'r') as gloss:
        for key in gloss:
            key = key.strip()
            GLOSS_LISTS.append(key)

    for filename in FILE_LIST:  # look for keywords in all files
        process_file(filename, KEYWORD_CONTEXTS, GLOSS_LISTS)

    output_context(OUTDIR, KEYWORD_CONTEXTS)

""""
from html.parser import HTMLParser
import urllib.request as urllib2

class MyHTMLParser(HTMLParser):

   #Initializing lists
   lsStartTags = list()
   lsEndTags = list()
   lsStartEndTags = list()
   lsComments = list()

   #HTML Parser Methods
   def handle_starttag(self, startTag, attrs):
       self.lsStartTags.append(startTag)

   def handle_endtag(self, endTag):
       self.lsEndTags.append(endTag)

   def handle_startendtag(self,startendTag, attrs):
       self.lsStartEndTags.append(startendTag)
"""




