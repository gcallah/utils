#!/usr/bin/env python3
# program to process SJC CVS file for faculty.

import csv
try:
    from typing import List
except ImportError:
    print("WARNING: Typing module is not find")

NAME = 0 # type: int
CAMPUS = 1 # type: int
DEPT = 2 # type: int
RANK = 3 # type: int
URL = 4 # type: int

with open("/home/gcallah/utils/faculty.csv", "r") as f_in:
    freader = csv.reader(f_in)
    with open("/home/gcallah/utils/out.csv", "w") as f_out:
        for row in freader:
           # nms = "Judy A. Cardoza"
            nms = row[NAME].split() # type: List[str]
            no_mi = [cln for cln in nms if "." not in cln] # type: List[str]
            if len(no_mi) < 2:
                print(no_mi)
                continue
            # print("No mi:" + str(no_mi))
            no_titles = no_mi # type: List[str]
            if len(no_mi) >= 2:
                no_titles = no_mi[0:2]
            # print("No titles:" + str(no_titles))
            fwriter = csv.writer(f_out)
            fwriter.writerow([no_titles[0], no_titles[1], row[CAMPUS],
                    row[DEPT], row[RANK], row[URL]])
