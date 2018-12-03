#!/usr/bin/python

import argparse
from subprocess import Popen, PIPE
ARG_ERROR = 1

"""
for testing run:
(python3 gloss_links.py test_data/gloss_key.txt test_data --lf
"test_data/gloss_links_inp1.txt" "test_data/gloss_links_inp2.txt")

"""


def process_file(filenm, keyword_context, gloss_list):
    """
    Parses each file for all the keyword and appends the
        keyword context dictionary.
    """
    for keyword in gloss_list:
        process = Popen(['grep', '-ioZ', keyword,
                         filenm], stdout=PIPE)
        (output, err) = process.communicate()
        # str_utf8 = output.decode("utf-8")
        # str_utf8 = re.sub(r'[^\w\s]','',str(str_utf8.strip())).split()
        if(len(output) > 0):
            if keyword not in keyword_context:
                keyword_context[keyword] = []
            keyword_context[keyword].append(filenm)


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
            for i in range(0, len(temp)):
                files.write("    " + temp[i])
                files.write("\n")


if __name__ == '__main__':
    # get command line params:
    (keyword_list, outdir, file_list) = process_args()

    gloss_lists = []
    keyword_contexts = {}
    # first get all the gloss keywords
    try:
        with open(keyword_list, 'r') as f:

            for line in f:
                # tab delimited
                key = line.strip().split("\t")
                gloss_lists.append(key[0])

    except IOError:
        print("Couldn't read " + keyword_list)
        exit(1)

    for filename in file_list:  # look for keywords in all files
        process_file(filename, keyword_contexts, gloss_lists)

    output_context(outdir, keyword_contexts)


"""
The code below is the previous version of gloss_links.
In this program search was done manually and a context was created for each
keyword as well. I have kept this code here in case it's needed in future.
"""

"""
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


import argparse
import re
ARG_ERROR = 1  # type: int


def process_file(filenm, keyword_context, gloss_list):
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
    try:
        with open(KEYWORD_FILE_LIST, 'r') as f:

            for line in f:
                # tab delimited
                key = line.strip().split("\t")
                GLOSS_LISTS.append(key[0])

    except IOError:
        print("Couldn't read " + KEYWORD_FILE_LIST)
        exit(1)

    for filename in FILE_LIST:  # look for keywords in all files
        process_file(filename, KEYWORD_CONTEXTS, GLOSS_LISTS)

    output_context(OUTDIR, KEYWORD_CONTEXTS)


## started this code for parsing html
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
