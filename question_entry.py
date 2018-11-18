"""
A little script to get and properly format questions for quizzes, homework,
etc.
"""

import sys
import random
try:
    from typing import TextIO, List  # noqa F401
except ImportError:
    print("WARNING: Typing module is not find")

DELIM = '#'  # type: str
CORR_MARK = '^'  # type: str


def ask(msg: str) -> str:
    print(msg, end='')
    ans = input()  # type: str
    return ans.strip()


def ask_int(msg: str) -> str:
    ans = "NAN"  # type: str
    while not ans.isdigit():
        ans = ask(msg)
    return ans


def add_item(item: str) -> str:
    return item + DELIM


if len(sys.argv) < 2:
    print("Must enter a directory for quizzes.")
    exit(1)


quiz_dir = sys.argv[1]  # type: str

# some projects just want one quiz per chapter:
sections = True
if len(sys.argv) > 2:
    if sys.argv[2] == "--nosections":
        sections = False

chap = ask_int("Enter chapter # for question: ")  # type: str
sect_txt = ""
if sections:
    section = ask_int("Enter section # for question: ")  # type: str
    sect_txt = "." + section
file_nm = quiz_dir + "/quiz" + chap + sect_txt + ".txt"  # type: str
f = open(file_nm, "a")  # type: TextIO

while True:
    answers = []  # type: List[str]

    question = ask("Enter question (blank to stop entering): ")  # type: str
    if len(question) < 1:
        break

    correct = ask("Enter correct answer (we will randomize!): ")  # type: str
    correct = CORR_MARK + correct
    answers.append(correct)

    new_bad = ""  # type: str
    while True:
        new_bad = ask("Enter a wrong answer (blank to stop entering): ")
        if len(new_bad) < 1:
            break
        else:
            answers.append(new_bad)

    s = ""  # type: str
    s += add_item(question)
    random.shuffle(answers)
    for answer in answers:
        s += add_item(answer)

    s = s[0:-1]
    f.write(s + "\n")
