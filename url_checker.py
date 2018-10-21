"""
Script to check validity of a given URL.
Returns request response back.
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
MAX_LINE = 80 # type: int

line_no = 0 # type: int
saw_error = False # type: bool
url_error = False # type: bool

def check_file(*files): #check if file exists
    for file in files:
        if not os.path.isfile(file):
            print(file + " is not a file")
            exit(ARG_ERROR)

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
    
def process_out_file(url_arr):
    out_valid_urls = []
    for url in url_arr:
        out_valid_urls.append(str(is_accessible(url)))
    return out_valid_urls

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("url_inp_file", help="text url input file to be parsed")
    arg_parser.add_argument("url_out_file", help="text url valid output file")
    args = arg_parser.parse_args()
    url_inp_file = args.url_inp_file
    url_out_file = args.url_out_file

    check_file(url_inp_file)
    url_list = []
    # get all the url links
    with open(url_inp_file,'r') as urls:
        for link in urls:
            link = link.strip()
            url_list.append(link)
    
    out_list = process_out_file(url_list)
    with open(url_out_file,'w') as out_f:
        for valid_response in out_list:
            out_f.write(valid_response+"\n")

    if saw_error:
        exit(PARSE_ERROR)
    else:
        exit(0)
