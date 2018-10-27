"""
Script to check validity of a given file with a lists of URLs.
Prints request response back.
"""

import argparse
import urllib.request as req

ARG_ERROR = 1 # type: int
PARSE_ERROR = 2 # type: int
IO_ERROR = 3  # type: int

def is_accessible(link): # type: (str) -> bool
    """
    Function that accesses a url string and returns response status code.
    """
    try:
        if link.startswith('http') or link.startswith('https'):
            connection = req.urlopen(link)
            print(connection.getcode())
        elif link.startswith('/'):
            rel_link = "http://www.thedevopscourse.com" + link
            connection = req.urlopen(rel_link)
            print(connection.getcode())
        else:
            rel_link_two = "http://www.thedevopscourse.com/" + link
            connection = req.urlopen(rel_link_two)
            print(connection.getcode())
    except req.HTTPError as http_e:
        print(http_e.getcode())
    except req.URLError:
        print("Invalid URL. No response code because address doesn't exist.")

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("url_inp_file", help="text url input file to be parsed")
    args = arg_parser.parse_args()
    URL_INP_FILE = args.url_inp_file

    URL_LIST = []

    try:
        # get all the url links
        with open(URL_INP_FILE, 'r') as urls:
            for url_link in urls:
                url_link = url_link.strip()
                URL_LIST.append(url_link)
    except IOError:
        print("Couldn't read " + URL_INP_FILE)
        exit(IO_ERROR)

    for url in URL_LIST:
        is_accessible(url)

    exit(0)
