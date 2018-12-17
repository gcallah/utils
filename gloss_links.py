#!/usr/bin/python

import argparse
from subprocess import Popen, PIPE
from pylib.misc import filenm_from_key

ARG_ERROR = 1

"""
This program searches and outputs name of the file where glossary/keyword
appear. Check below on how to run the program.

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
        # \\b was used for word breaks. Single backflash is ignored by python.
        process = Popen(['grep', '-ioZ', '\\b' + keyword + '\\b',
                         filenm], stdout=PIPE)
        (output, err) = process.communicate()

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


def output_context(outdir, keyword_context, gloss_lists):
    """
        output context of a keyword
        Args: outdir, keyword, context
        Returns: None
    """
    for keyword in keyword_context:
        file_name = filenm_from_key(keyword)
        output_name = outdir + "/" + file_name + ".txt"
        with open(output_name, 'w') as files:
            # br tags since this will be added as html file.
            files.write(keyword + " found in: <br>")
            temp = keyword_context[keyword]
            for i in range(0, len(temp)):
                files.write("    " + temp[i])
                files.write("\n")
                files.write("<br>")

    # outputting names of files that dont't appear in glossary list
    # needed to avoid django include error
    for key in gloss_lists:
        file_name = filenm_from_key(key)
        output_name = outdir + "/" + file_name + ".txt"
        if key not in keyword_context:
            with open(output_name, 'w') as files:
                pass


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

    output_context(outdir, keyword_contexts, gloss_lists)
