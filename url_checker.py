"""
Script to check validity of a given file with a lists of URLs.
Prints request response back.
"""

import sys
import os
import string
import re
import argparse
import urllib.request as req
from urllib.parse import urlparse, urljoin

ARG_ERROR = 1 # type: int
PARSE_ERROR = 2 # type: int
IO_ERROR = 3  # type: int

def is_accessible(link): # type: (str) -> bool
    try:
        if link.startswith('http') or link.startswith('https'):     
            connection = req.urlopen(link)
            return connection.getcode()
        elif link.startswith('/'): 
            rel_link = "http://www.thedevopscourse.com" + link
            connection = req.urlopen(rel_link)
            return connection.getcode()
        else: 
            rel_link_two = "http://www.thedevopscourse.com/" + link
            connection = req.urlopen(rel_link_two)
            return connection.getcode()
    except req.HTTPError as e:
        return e.getcode()
    except req.URLError as e:
        return "Invalid URL. No response code because address doesn't exist."
    
def process_url_results(url_arr):
    for url in url_arr:
        print(is_accessible(url))

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("url_inp_file", help="text url input file to be parsed")
    args = arg_parser.parse_args()
    url_inp_file = args.url_inp_file

    url_list = []

    try:
        # get all the url links
        with open(url_inp_file,'r') as urls:
            for link in urls:
                link = link.strip()
                url_list.append(link)
    except IOError:
        print("Couldn't read " + url_inp_file)
        exit(IO_ERROR)    

    process_url_results(url_list)
    exit(0)
