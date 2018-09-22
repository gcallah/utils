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
    arg_parser.add_argument("file_name")
    args = arg_parser.parse_args()
    file_name = args.file_name

    check_file(file_name)

