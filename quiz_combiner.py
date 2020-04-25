#!/usr/bin/env python3
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

lower_alpha_list = list(string.ascii_lowercase)
whitespace_list = list(string.whitespace)
question_list = []
TYPE_QUESTION = "QUESTION"
TYPE_CHOICE = "CHOICE"
# the delimiter for question #
# Ex: <number><delimiter> <rest of line>
# There should be a whitespace between the question symbol and the actual question
QUESTION_DELIMITER = "." 
# the delimiter for choice letter
# Ex: <letter><delimiter> <rest of line>
CHOICE_DELIMITER = "." # the delimiter for answer choice (letter)

class Question:
    '''
        represents a question
    '''

    class Choices:
        '''
            represents a list of choices 
            (max num choices = number of letters in lower_alpha_list)
        '''
        def __init__(self, choices):
            self.list = choices
        
        # Shuffles n-1 choices, leaving nth choice unshuffled
        def shuffle_choices(self):
            if(len(self.list) < 2):
                return

            numSample = len(self.list)-1
            temp = random.sample(self.list[:numSample], k=numSample)

            # Copy the results
            for i in range(len(temp)):
                self.list[i] = temp[i]

        # each time you print, the choices get shuffled
        def __str__(self):
            # shuffle the choices
            self.shuffle_choices()

            # Then format the results accordingly
            result = ""
            for choice, letter in zip(self.list, lower_alpha_list):
                # If it is the answer
                if(choice[1] == True):
                    result += "*"
                
                result = result + letter + CHOICE_DELIMITER + " " + choice[0]

            return result

    # __init__(str,list(str,bool)) -> None
    def __init__(self, question, choicesList): 
        self.question = question
        self.choices = str(self.Choices(choicesList))

    def __str__(self):
        #print(repr(self.choices))
        # each should have their own newline character
        return "{self.question}\n{self.choices}".format(self=self)

def is_int(input):
    try:
        int(input)
        return True
    except ValueError:
        return False

# Returns the smallest nonnegative number in given list
def min_positive(numList):
    if(len(numList) == 0):
        return -1

    minNum = max(numList)

    for num in numList:
        if(num >= 0 and num < minNum):
            minNum = num
    
    return minNum

def parse_files(filenames):
    file_lines = [] # (string, type=(TYPE_QUESTION / TYPE_CHOICE))

    for file in filenames:
        with open(file, 'r') as input_stream:

            resultLine = ""
            CUR_TYPE = TYPE_QUESTION # Assume first is question

            # Scan until the first question or sign of a possible question
            delimitIndex = -1
            boundaryIndex = 0
            line = ""
            while(delimitIndex == -1):
                line = input_stream.readline()
                # EOF
                if(len(line) == 0):
                    return
                
                line = line.lstrip()

                # Skip blank lines
                if(len(line) == 0):
                    continue

                # Note: the QUESTION_DELIMITER should be followed by some whitespace right after it
                delimitIndex = line.rstrip().find(QUESTION_DELIMITER)
                boundaryIndex = min_positive([line.find(ws) for ws in whitespace_list])

                # If we found the delimiter, but it is way further down the string
                # then we assume it was just some string that happen to have the delimiter
                if(delimitIndex > boundaryIndex):
                    delimitIndex = -1

            # Tokenize the file
            while(len(line) > 0):
                stripedLine = line.lstrip()

                if(len(stripedLine) == 0 or stripedLine.isspace()):
                    line = input_stream.readline()
                    continue
                
                delimitIndex = stripedLine.rstrip().find(QUESTION_DELIMITER) # First "."
                boundaryIndex = min_positive([stripedLine.find(ws) for ws in whitespace_list])

                # Marks beginning of new state
                # delimitIndex < boundaryIndex avoid QUESTION_DELIMITER being found way past the beginning
                if(delimitIndex != -1 and delimitIndex < boundaryIndex):

                    if(len(resultLine) > 0):
                        file_lines.append((resultLine, CUR_TYPE))
    
                    # Reset
                    resultLine = ""                   

                    # The beginning of a question
                    if(is_int(stripedLine[:delimitIndex])):
                        CUR_TYPE = TYPE_QUESTION
                        resultLine = stripedLine[delimitIndex+len(QUESTION_DELIMITER):].lstrip()
                    # The beginning of a choice
                    else:
                        CUR_TYPE = TYPE_CHOICE
                        resultLine = stripedLine[delimitIndex+len(CHOICE_DELIMITER):].lstrip()   
                else:
                    # Assume continuation of CUR_TYPE
                    resultLine += stripedLine

                # Move to next line
                line = input_stream.readline()

            # Final item
            if(len(resultLine) > 0):
                file_lines.append((resultLine, CUR_TYPE))

    print(file_lines)

    i = 0
    NEXT_TYPE = TYPE_QUESTION
    prevQuestion = ""
    prevChoices = []
    while(i < len(file_lines)):
        line_type = file_lines[i][1]
        line_content = file_lines[i][0]
        if(NEXT_TYPE != line_type):
            print("ERROR: EXPECTED " + NEXT_TYPE + " BUT FOUND " + line_type)
            exit(1)
        
        # New question
        if(line_type == TYPE_QUESTION):
            # Store the previous question
            if(len(prevQuestion) > 0):
                print("**** QUESTION: " + prevQuestion)
                print("**** CHOICES: " + str(prevChoices))
                question_list.append(Question(prevQuestion, prevChoices))

            # New question setup
            prevQuestion = line_content
            prevChoices = []
        # New choice
        if(line_type == TYPE_CHOICE):
            # delimitIndex = min_positive([line_content.find(ws) for ws in whitespace_list])

            # choiceText = line_content[delimitIndex+1:]
    
            # Mark which choice is the answer and strip away the letter
            if(line_content[0] == '*'):
                prevChoices.append((line_content, True))
            else:
                prevChoices.append((line_content, False))
        
        if(i+1 < len(file_lines)):
            NEXT_TYPE = file_lines[i+1][1]
        i+=1

    print("PREV OUTSIDE: " + prevQuestion)
    print("PREV OUTSIDE C: " + str(prevChoices))
    # If we processed anything, then we have a last item
    if(i > 0):
        question_list.append(Question(prevQuestion, prevChoices))

        

    # # Processes per question (each separated by a newline)
    # while(line):
    #     # Skip over trailing newlines between questions
    #     while(line == "\n"):   # instead line.isspace()
    #         line = input_stream.readline()

    #     # First, get the points
    #     start = line.index(" ")
    #     points = line[start+1:]

    #     # Now the question
    #     question = ""
    #     line = input_stream.readline()
    #     while(line != "\n"):
    #         question += line
    #         line = input_stream.readline()

    #     # Then the choices
    #     answerChoices = []
    #     line = input_stream.readline()
    #     while(line != "\n"):
    #         textStart = line.index(" ")
    #         # Mark which choice is the answer and strip away the letter
    #         if(line[0] == '*'):
    #             answerChoices.append((line[textStart+1:], True))
    #         else:
    #             answerChoices.append((line[textStart+1:], False))

    #         line = input_stream.readline()

    #     # Append and make a new instance of a question obj
    #     question_list.append(Question(question, answerChoices, points))

    #     # Move to the next section
    #     line = input_stream.readline()

if __name__ == "__main__":
    # Read in the questions from files
    # Append questions to question_list
    quizFiles = sys.argv[1:]
    parse_files(quizFiles)

    # # Shuffle our list of questions
    # random.shuffle(question_list)

    # Output the results
    for questionNum in range(len(question_list)):
        print("{0}{1} {2}".format(questionNum+1, QUESTION_DELIMITER, str(question_list[questionNum])))
