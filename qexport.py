#!/usr/bin/env python3

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
    if format == "nyu":
        i = 1
        for question in recs:
            print(str(i) + ". (1 point)")
            print(question["text"])
            print()

            # list of answer options
            answers = ['answerA', 'answerB', 'answerC', 'answerD', 'answerE']
            ans_options = [question[i] for i in answers]

            # separate list for answer option bullets
            options = ["a.", "b.", "c.", "d.", "e."]

            # marking the correct answer by '*'
            correct = question["correct"].lower() + "."
            options[options.index(correct)] = "*" + options[options.index(correct)]
            for option in ans_options:
                if option:
                    # matching the index for 'options' &
                    # 'ans_options' to get correct alphabet
                    print(options[ans_options.index(option)] + " " + option)
                else:
                    break
            i += 1
            print()
    if format == "gradescope":
        i = 1
        for question in recs:
            print(question["text"])
            print()

            # list of answer options
            answers = ['answerA', 'answerB', 'answerC', 'answerD', 'answerE']
            ans_options = [question[i] for i in answers]

            # separate list for answer option bullets
            options = ["a", "b", "c", "d", "e"]

            # marking the correct answer by '*'
            correct = question["correct"].lower()
            options[options.index(correct)] = "(X)"
            for option in range(len(options)):
                if options[option] != "(X)":
                    options[option] = "( )"
            for option in ans_options:
                if option:
                    # matching the index for 'options' &
                    # 'ans_options' to get correct alphabet
                    print(options[ans_options.index(option)] + " " + option)
                else:
                    break
            i += 1
            print()


def main():
    mod_nm = None
    format = None
    if len(sys.argv) > 1:
        mod_nm = sys.argv[1]
        format = sys.argv[2]

    recs = read_questions(mod_nm)
    write_questions(recs, format)


if __name__ == '__main__':
    main()
