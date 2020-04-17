#!/usr/bin/python
"""
Script to read in quiz questions from different files, combines and randomizes the questions
"""

import sys
import random

questionList = []

class Question:

    # Class representing a question
    # __init__(str,str,str)
    def __init__(self, question, choices, points):
        # Note each are strings
        self.question = question
        self.choices = choices
        self.points = points

    def __str__(self):
        # each should have their own newline character
        return "{self.points}{self.question}{self.choices}".format(self=self)


def parseFiles(filenames):
    for file in filenames:
        print("Processing %s" % file)
        with open(file,'r') as inputStream:
            line = inputStream.readline()

            # Processes per question (each separated by a newline)
            while(line):
                # First, get the points
                start = line.index(" ")
                points = line[start+1:]
                print("POINTS: " + points)
    
                # Now the question
                question = ""
                line = inputStream.readline()
                while(line != "\n"):
                    question += line
                    line = inputStream.readline()
                print("QUESTION: " + question)

                # Then the choices
                choices = ""
                line = inputStream.readline()
                while(line != "\n"):
                    choices += line
                    line = inputStream.readline()
                print("CHOICES: " + choices)

                # Append and make a new instance of a question obj
                questionList.append(Question(question, choices, points))

                # Move to the next section
                line = inputStream.readline()

if __name__ == "__main__":
    quizFiles = sys.argv[1:]
    parseFiles(quizFiles)

    # Shuffle our list of questions
    random.shuffle(questionList)

    # Output the results
    for questionNum in range(len(questionList)):
        print("{0}. {1}".format(questionNum+1, str(questionList[questionNum])))