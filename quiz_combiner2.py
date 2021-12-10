
"""
Second version of quiz combiner: just shuffles questions.
"""
import sys
import random

NEW_Q_DELIM = "NewQuestion"


def usage():
    """
    Prints usage message
    """
    print("Usage: " + sys.argv[0] + " [filepath...]")


def read_questions(file_nm, questions):
    question = ""
    with open(file_nm, "r") as f:
        for ln in f:
            # print(f"{ln=}")
            if ln.startswith(NEW_Q_DELIM):
                if question:
                    questions.append(question)
                question = ""
            question += ln
    questions.append(question)
    return questions


def main():
    # Read in the questions from files
    quiz_files = sys.argv[1:]
    if(len(quiz_files) == 0):
        usage()
        exit(1)
    questions = []
    for f in quiz_files:
        read_questions(f, questions)

    random.shuffle(questions)
    for q in questions:
        print(f"{q}")


if __name__ == "__main__":
    main()
