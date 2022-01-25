#!/usr/bin/python3

"""
This file contains code to extract quiz question from Django controlled db.

Functions:
    read_questions()
    write_questions()
    main()
"""

import os
import sys
import django
from django.apps import AppConfig


class QexportConfig(AppConfig):
    name = 'qexport'


PLATFORM = "brightspace"

ANSWER_COL_NAMES = {
        'a': 'answerA',
        'b': 'answerB',
        'c': 'answerC',
        'd': 'answerD',
        'e': 'answerE'
        }

OPT_PUNC = ". "

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

SECRET_KEY = os.getenv('SECRET_KEY')
# setting DB variables from mysite/settings.py:
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()
from devops.models import Question  # noqa E402


def read_questions(mod_nm):
    """
    reads questions for module 'mod_nm'
    """
    recs = None
    if mod_nm is None:
        recs = Question.objects.values()
    else:
        recs = Question.objects.filter(module=mod_nm).values()
    return recs


def write_questions(recs, format):
    """
        Args:
            recs: the data to output
        Returns:
            None (for now: we probably want success or error codes)
    """
    for q_no, qst in enumerate(recs, start=1):
        if format == "gradescope":
            print(qst["text"])
            print()

            # marking the correct answer by '*'
            for ch, col_name in ANSWER_COL_NAMES.items():
                check_area = '(X)' if ch == qst["correct"].lower() else '( )'
                # matching the index for 'options' &
                # 'ans_options' to get correct alphabet
                print(f"{check_area} {qst[col_name]}")
            print()

        elif format == "brightspace":
            print("NewQuestion,MC")
            print("QuestionText," + '"' + qst["text"] + '"')
            print("Points,1")

            for check, col_name in ANSWER_COL_NAMES.items():
                if check == qst["correct"].lower():
                    check_area = 'Option,100'
                else:
                    check_area = 'Option,0'
                print(check_area, ',', '"', qst[col_name], '"')


def main():
    mod_nm = None
    format = PLATFORM
    if len(sys.argv) > 1:
        mod_nm = sys.argv[1]
    if len(sys.argv) > 2:
        format = sys.argv[2]

    recs = read_questions(mod_nm)
    write_questions(recs, format)


if __name__ == '__main__':
    main()
