import os
import argparse

ARG_ERROR = 1  # type: int
file_name = None


def check_file(*files): #check if file exists
    for file in files:
        if not os.path.isfile(file):
            print(file + " is not a file")
            exit(ARG_ERROR)


if __name__ == '__main__':

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("text_file")
    arg_parser.add_argument("html_file")
    args = arg_parser.parse_args()
    text_file = args.text_file
    html_file = args.html_file

check_file(text_file,html_file)

text_path, html_path = (os.path.abspath(text_file)), (os.path.abspath(html_file))

