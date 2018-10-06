import os
import argparse
ARG_ERROR = 1  # type: int
"""
So far: the indexer takes a keyword, and a list of files. Parses all the files
and prints all context of the keyword.

current limitation: if keyword finishes with a punctuation, doesn't match. If appears more than
once in a line, only shows once. 

Discuss: should i take list of files as list in command list? 

"""

def check_file(files): #check if file exists
    for file in files:
        if not os.path.isfile(file):
            print(file + " is not a file")
            exit(ARG_ERROR)

if __name__ == '__main__':

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("key")
    arg_parser.add_argument("list_files")
    args = arg_parser.parse_args()
    keyword = args.key
    list_files = args.list_files


list_files = list_files.strip('[]').split(',')
check_file(list_files)

keyword = keyword.lower()
index_dict = {}

for file in list_files:
    with open(file, 'r') as txt:

        for line in txt:
            line = line.lower()

            if keyword in line:
                line = line.strip().split(" ")
                context = None
                key_index = line.index(keyword)

                if 0 < key_index < len(line) - 1:

                    context = line[key_index-1] + " " + line[key_index] + " " + line[key_index+1]

                elif key_index == 0:
                    if len(line) > 1:
                        context = line[key_index] + " " + line[key_index+1]
                    else:
                        context = line[key_index]

                elif key_index == len(line) - 1:
                    context = line[key_index - 1] + " " + line[key_index]

                if file not in index_dict:
                    index_dict[file] = []

                index_dict[file].append(context)

for key, value in index_dict.items():
    print(keyword + " occurs in: ")
    for each_context in value:
        print("    " + key + ": " + each_context)



#python3 create_gloss_links.py "description" ["data_manip.html","index.html"]
