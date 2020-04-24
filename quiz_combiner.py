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
question_list = []
TYPE_QUESTION = "QUESTION"
TYPE_CHOICE = "CHOICE"
# the delimiter for question #
# Ex: <number><delimiter> <rest of line>
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
                
                result = result + letter + ". " + choice[0]

            return result

    # __init__(str,list(str,bool)) -> None
    def __init__(self, question, choicesList): 
        self.question = question
        self.choices = str(self.Choices(choicesList))

    def __str__(self):
        # each should have their own newline character
        return "{self.question}\n{self.choices}".format(self=self)

def is_int(input):
    try:
        int(input)
        return True
    except ValueError:
        return False

def parse_files(filenames):
    file_lines = [] # (string, type[QUESTION, CHOICE])

    for file in filenames:
        with open(file, 'r') as input_stream:

            resultLine = ""
            CUR_TYPE = TYPE_QUESTION

            
            # # Scan until the first question
            # line = input_stream.readline()
            # while(line.find(". ") == -1):
            #     line = input_stream.readline()


            # Scan until the first question
            delimitIndex = -1
            boundaryIndex = 0
            while(delimitIndex == -1 and delimitIndex < boundaryIndex):
                line = input_stream.readline()
                delimitIndex = line.rstrip().find(QUESTION_DELIMITER) # First "."
                boundaryIndex = line.rstrip().find(" ") # First whitespace


            # Tokenize the file
            while(len(line) > 0):
                stripedLine = line.lstrip()
                print("=========== START")
                print("LINE: " + stripedLine)

                if(len(stripedLine) == 0 or stripedLine.isspace()):
                    line = input_stream.readline()
                    continue
                
                delimitIndex = stripedLine.rstrip().find(".") # First "."
                boundaryIndex = stripedLine.rstrip().find(" ") # First whitespace

                # Marks beginning of new state
                # delimitIndex < boundaryIndex avoid ". " being found way past the beginning
                if(delimitIndex != -1 and delimitIndex < boundaryIndex):
                    # print("CUR_TYPE: " + CUR_TYPE)
                    # print("RL: " + resultLine)
                    # Add what was built previously (Should be a question)
                    # if(CUR_TYPE == TYPE_QUESTION and len(resultLine) > 0):
                    #     file_lines.append((resultLine, CUR_TYPE))
                    if(len(resultLine) > 0):
                        file_lines.append((resultLine, CUR_TYPE))
    
                    # Reset
                    resultLine = ""                   
                    resultLine += stripedLine[delimitIndex+1:].lstrip()
                    # print("IS_INT: "+ str(is_int(stripedLine[:delimitIndex])))
                    # The beginning of a question
                    if(is_int(stripedLine[:delimitIndex])):
                        CUR_TYPE = TYPE_QUESTION

                    # The beginning of a choice
                    else:
                        CUR_TYPE = TYPE_CHOICE
                        resultLine = stripedLine.lstrip()
                        # print("ADD CHOICE: " + resultLine)
    
                        # Add to the list of tokenize lines
                        # file_lines.append((resultLine, CUR_TYPE))
                        # resultLine = ""     
                else:
                    # Assume this is part of the question text
                    resultLine += stripedLine
                    # CUR_TYPE = TYPE_QUESTION

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
            delimitIndex = line_content.find(" ")

            choiceText = line_content[delimitIndex+1:]
    
            # Mark which choice is the answer and strip away the letter
            if(line_content[0] == '*'):
                prevChoices.append((choiceText, True))
            else:
                prevChoices.append((choiceText, False))
        
        if(i+1 < len(file_lines)):
            NEXT_TYPE = file_lines[i+1][1]
        i+=1

    print("PREV OUTSIDE: " + prevQuestion)
    print("PREV OUTSIDE C: " + str(prevChoices))

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
        print("{0}. {1}".format(questionNum+1, str(question_list[questionNum])))
