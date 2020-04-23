#!/usr/bin/python
"""
Script to read in quiz questions from different files, combines and randomizes the questions
"""

"""
Usage: quiz_combiner.py [file ...]
Outputs results to stdout
"""

import sys
import random
import string

lowerAlphaList = list(string.ascii_lowercase)
questionList = []

class Question:
    '''
        represents a question
    '''

    class Choices:
        '''
            represents a list of choices 
            (max num choices = number of letters in lowerAlphaList)
        '''
        def __init__(self, choices):
            self.list = choices
        
        # Shuffles n-1 choices, leaving nth choice unshuffled
        def shuffleChoices(self):
            numSample = len(self.list)-1
            temp = random.sample(self.list[:numSample], k=numSample)

            # Copy the results
            for i in range(len(temp)):
                self.list[i] = temp[i]

        # each time you print, the choices get shuffled
        def __str__(self):
            # shuffle the choices
            self.shuffleChoices()

            # Then format the results accordingly
            result = ""
            for choice, letter in zip(self.list, lowerAlphaList):
                # If it is the answer
                if(choice[1] == True):
                    result += "*"
                
                result = result + letter + ". " + choice[0]

            return result

    # __init__(str,list(str,bool),str) -> None
    def __init__(self, question, choicesList, points): 
        self.question = question
        self.choices = str(self.Choices(choicesList))
        self.points = points

    def __str__(self):
        # each should have their own newline character
        return "{self.points}{self.question}\n{self.choices}".format(self=self)


def parseFiles(filenames):
    for file in filenames:
        with open(file,'r') as inputStream:
            line = inputStream.readline()

            # Processes per question (each separated by a newline)
            while(line):
                # Skip over trailing newlines between questions
                while(line == "\n"):
                    line = inputStream.readline()

                # First, get the points
                start = line.index(" ")
                points = line[start+1:]
    
                # Now the question
                question = ""
                line = inputStream.readline()
                while(line != "\n"):
                    question += line
                    line = inputStream.readline()

                # Then the choices
                answerChoices = []
                line = inputStream.readline()
                while(line != "\n"):
                    textStart = line.index(" ")
                    # Mark which choice is the answer and strip away the letter
                    if(line[0] == '*'):
                        answerChoices.append((line[textStart+1:], True))
                    else:
                        answerChoices.append((line[textStart+1:], False))

                    line = inputStream.readline()

                # Append and make a new instance of a question obj
                questionList.append(Question(question, answerChoices, points))

                # Move to the next section
                line = inputStream.readline()

if __name__ == "__main__":
    # Read in the questions from files
    # Append questions to questionList
    quizFiles = sys.argv[1:]
    parseFiles(quizFiles)

    # Shuffle our list of questions
    random.shuffle(questionList)

    # Output the results
    for questionNum in range(len(questionList)):
        print("{0}. {1}".format(questionNum+1, str(questionList[questionNum])))