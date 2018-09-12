#!/usr/bin/env python3

"""
This file contains code to extract quiz question from Django controlled db.

Functions:
    read_records()
    write_records()
    main()
"""

import os
import sys
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()
from .devops.models import Question

desired_flds = ['text', 'correct', 'answerA', 'answerB', 'answerC',
                'answerD', 'answerE']

def read_records(mod_nm):
    recs = None
    if mod_nm is None:
        recs = Question.objects.values()
    else:
        recs = Question.objects.filter(module=mod_nm).values()
    # next two lines are just for debugging:
    for rec in recs:
            print(rec)
    return recs

def write_records(recs):
    """
        Args:
            filenm: where to output the CSV
            recs: the data to output 
        Returns:
            None (for now: we probably want success or error codes)
    """
        i = 1
        for record in recs:
            flds = record.items()
            print(str(i) + ". (1 point)")
            print(flds["text"])
            i += 1

def main():
    mod_nm = None
    if len(sys.argv) > 1:
        mod_nm = sys.argv[1]

    recs = read_records(mod_nm)
    write_records(recs)

if __name__ == '__main__':
    main()
