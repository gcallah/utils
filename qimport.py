#!/usr/bin/env python3

"""
This file contains code to import quiz questions to Django controlled db.
It is required by the code that you provide the file path(from which the
questions need to extracted) as an argument.

Functions:
main() - This drives the code and calls the relevant function(s) for extraction
            of questions.
extract_questions() - Extracts the questions and its answers from a text file
                        and returns a list of commands that will help insert
                        the extracted values into database all at once.
"""

import os
import sys
import django
from itertools import zip_longest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from devops.models import Question  # noqa E402


def extract_questions(path_nm):

    Text = list()
    Correct = list()
    AnswerA = list()
    AnswerB = list()
    AnswerC = list()
    AnswerD = list()
    AnswerE = list()

    # counters for respective lists
    q_num, cor_ans, A, B, C, D, E = 0, 0, 0, 0, 0, 0, 0

    # opening the file
    with open(path_nm) as input_file:
        for line in input_file:
            line = line.rstrip()
            if line:
                # checking for question
                if line[1] == ')' or line[2] == ')':
                    Text.append(line[3:].lstrip())
                    q_num += 1
                    continue
                # checking for correct answer
                if line[0] == '*':
                    Correct.append(line[1])
                    cor_ans += 1

                    if line[1] == 'a':
                        AnswerA.append(line[4:])
                        A += 1

                    elif line[1] == 'b':
                        AnswerB.append(line[4:])
                        B += 1

                    elif line[1] == 'c':
                        AnswerC.append(line[4:])
                        C += 1

                    elif line[1] == 'd':
                        AnswerD.append(line[4:])
                        D += 1

                    else:
                        AnswerE.append(line[4:])
                        E += 1

                elif line[0] == 'a':
                    AnswerA.append(line[3:])
                    A += 1

                elif line[0] == 'b':
                    AnswerB.append(line[3:])
                    B += 1

                elif line[0] == 'c':
                    AnswerC.append(line[3:])
                    C += 1

                elif line[0] == 'd':
                    AnswerD.append(line[3:])
                    D += 1

                else:
                    AnswerE.append(line[3:])
                    E += 1
            else:
                continue

    # recs will be the final list of commands for insertion
    recs = list()

    # looping to create a list of commands with model 'Question'
    for i, j, k, l, m, n, o in zip_longest(range(q_num), range(cor_ans),
                                           range(A), range(B), range(C),
                                           range(D), range(E)):
        recs.append(Question(text=Text[i] if i else None,
                             correct=Correct[j] if j else None,
                             answerA=AnswerA[k] if k else None,
                             answerB=AnswerB[l] if l else None,
                             answerC=AnswerC[m] if m else None,
                             answerD=AnswerD[n] if n else None,
                             answerE=AnswerE[o] if o else None,
                             difficulty=1, qtype='MCHOICE'))

    return recs


def insert_records(recs):

    if not recs:
        print("No data to insert!")
    else:
        # statement that inserts records
        Question.objects.bulk_create(recs)


def main():
    path_nm = None
    if len(sys.argv) > 1:
        path_nm = sys.argv[1]
    else:
        print('Provide a file to read!')
        exit()
        # path_nm = 'data/DevOpsFinalQuiz.txt'

    # creating a list of all the commands for the data to be inserted
    recs = extract_questions(path_nm)

    # inserting all the question and answer options in the database at once
    insert_records(recs)


if __name__ == '__main__':
    main()
