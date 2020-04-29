#!/usr/bin/env python3
import sys
import random
import string

"""
Script to read in quiz questions from different files,
combines and randomizes the questions & choices

Generic Format / recognized formats
==============
<numbers><QUESTION_DELIM> <text>
<letters><CHOICE_DELIM> <text>
==============

Notes: All questions and choices are differentiate by whether the substring
        prior to their respective delimitors is purely consisting of:

        a.) If only digits, then script believes we hit a question
        b.) If only letters, then script believes we hit a choice
        (Any mixed substrings will be viewed as a choice)
        c.) If no delimiter is found, or thinks its not a question or choice,
        script will assume the text is part of the text we are building up
        (be it a question or choice)

        QUESTION_DELIM and CHOICE_DELIM are also used in the formatting
        the output

        ANSWER_MARKER is used to mark the correct answer (must be in front of
        choice letters)

        Avoid putting space between the question num or choice letter and its
        delimitor. Otherwise, it could get interpreted as just text rather than
        possible new item
"""

"""
Usage: quiz_combiner.py [filepath...]
Outputs results to stdout
"""

# constants, don't change / really no need for change
lower_alpha_list = list(string.ascii_lowercase)
ws_list = list(string.whitespace)
question_list = []
SCRIPT_NAME = sys.argv[0]
TYPE_QUESTION = "QUESTION"
TYPE_CHOICE = "CHOICE"


# the delimiter for question number
# Ex: <number><delimiter> <rest of line>
# There should be a whitespace between the question symbol and
# the actual question in the file
QUESTION_DELIM = "."

# the delimiter for choice letter
# Ex: <letter><delimiter> <rest of line>
# the delimiter for answer choice (letter)
CHOICE_DELIM = "."

# marks which choice is the correct answer, should be only 1 character
ANSWER_MARKER = "*"

DEBUG_MODE = False


class Question:
    """
        represents a question
    """

    class Choices:
        """
            represents a list of choices
            (max num choices = number of letters in lower_alpha_list)
        """
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
                # If it is the answer, then prepend the marker symbol
                if(choice[1] is True):
                    result += ANSWER_MARKER

                result = result + letter + CHOICE_DELIM + " " + choice[0]

            return result

    # __init__(str,list(str,bool)) -> None
    def __init__(self, question, choicesList):
        self.question = question
        self.choices = str(self.Choices(choicesList))

    def __str__(self):
        # each should have their own newline character
        return "{self.question}\n{self.choices}".format(self=self)


def is_int(input):
    """
        returns true if input string is only numbers
    """
    try:
        int(input)
        return True
    except ValueError:
        return False


def is_alpha_only(input):
    """
        returns true if the string is only letters
    """
    return len(input.translate(str.maketrans(
        '', '', string.whitespace + string.punctuation + string.digits))) > 0


def min_positive(numList):
    """
        Returns the smallest nonnegative number in given list
    """
    if(len(numList) == 0):
        return -1

    minNum = max(numList)

    for num in numList:
        if(num >= 0 and num < minNum):
            minNum = num

    return minNum


def script_output(message, withName=True):
    """
        Wrapper for print to include the script's name
    """
    if(withName is True):
        print(SCRIPT_NAME + ": " + message)
    else:
        print(message)


def usage():
    """
        Prints usage message
    """
    print("Usage: " + SCRIPT_NAME + " [filepath...]")


def validate_config():
    """
        Function to check if the configuration of this script
        is valid for this script
    """
    QD_len = len(QUESTION_DELIM.strip())
    CD_len = len(CHOICE_DELIM.strip())
    marker_len = len(ANSWER_MARKER.strip())

    if(QD_len != len(QUESTION_DELIM)):
        script_output("QUESTION_DELIM can't have trailing whitespace")
        return False

    if(CD_len != len(CHOICE_DELIM)):
        script_output("CHOICE DELIMITER can't have trailing whitespace")
        return False

    if(len(QUESTION_DELIM) == 0 or len(CHOICE_DELIM) == 0):
        script_output("DELIMITER(S) can't be an empty string")
        return False

    if(marker_len != len(ANSWER_MARKER) or marker_len > 1):
        script_output("ANSWER_MARKER must be at most len of 1 (no whitespace)")
        return False

    return True


def fill_question_list(file_lines):
    """
        Input: an list of [(str, TYPE_QUESTION/TYPE_CHOICE)]
        where the first entry is the filename associated with the set of lines
        file_lines categorized the lines into question and choice text

        This function creates instances of Question and puts them into the
        question_list, which can be worked on later
    """

    for line_set in file_lines:
        set_name = line_set[0] # For error messages

        # We assume and expect the first item to be a question
        i = 1 # i=0 is the filename for this set of lines
        NEXT_TYPE = TYPE_QUESTION
        prevQuestion = ""
        prevChoices = []

        # Loop through the lines
        while(i < len(line_set)):
            line_type = line_set[i][1]
            line_content = line_set[i][0]

            if(DEBUG_MODE):
                print("fill_QL() LT: " + line_type)
                print("fill_QL() LC: " + line_content)

            # Should only be true where only choices were found
            # and never actually got a question as first item
            if(NEXT_TYPE != line_type):
                print(
                    "ERROR: EXPECTED " + NEXT_TYPE + " BUT FOUND " 
                    + line_type + " in " + set_name)
                exit(1)

            # New question
            if(line_type == TYPE_QUESTION):
                # Store the previous question
                if(len(prevQuestion) > 0):
                    if(DEBUG_MODE):
                        print("** QUESTION: " + prevQuestion)
                        print("** CHOICES: " + str(prevChoices))
                    question_list.append(Question(prevQuestion, prevChoices))

                # New question setup
                prevQuestion = line_content
                prevChoices = []
            # New choice
            if(line_type == TYPE_CHOICE):
                choice_DI = line_content.find(CHOICE_DELIM)
                choiceText = line_content[choice_DI+len(CHOICE_DELIM):].lstrip()

                # Mark which choice is the answer and strip away the letter
                if(line_content[0] == ANSWER_MARKER):
                    prevChoices.append((choiceText, True))
                else:
                    prevChoices.append((choiceText, False))

            if(i+1 < len(line_set)):
                NEXT_TYPE = line_set[i+1][1]
            i += 1

        if(DEBUG_MODE):
            print("** PREV OUTSIDE: " + prevQuestion)
            print("** PREV OUTSIDE C: " + str(prevChoices))
        # If we processed anything, then we have a last item
        if(i > 0):
            question_list.append(Question(prevQuestion, prevChoices))


def parse_files(filenames):
    file_lines = []  # [[(string, type=(TYPE_QUESTION / TYPE_CHOICE))]...]

    for file in filenames:
        with open(file, 'r') as input_stream:
            # Set of lines for this particular file
            # First entry is the name of the file for error message
            line_set = [file]

            resultLine = ""
            CUR_TYPE = TYPE_QUESTION  # Assume first is question

            # Scan until the first question or sign of a possible question
            delimitIndex = -1
            boundaryIndex = 0
            line = ""
            while(delimitIndex == -1):
                line = input_stream.readline()
                # EOF
                if(len(line) == 0):
                    script_output("No questions found.")
                    script_output("Question number should be followed by: "
                                  + repr(QUESTION_DELIM), False)
                    return

                line = line.lstrip()

                # Skip blank lines
                if(len(line) == 0):
                    continue

                # Note: the QUESTION_DELIM should be followed by some
                # whitespace right after it (ideally)
                delimitIndex = line.rstrip().find(QUESTION_DELIM)
                boundaryIndex = min_positive([line.find(ws) for ws in ws_list])

                # If we found the delimiter, but it is way further down the
                # string then we assume it was just some string that happen to
                # have the delimiter
                if(delimitIndex > boundaryIndex):
                    delimitIndex = -1

            # Tokenize the file
            while(len(line) > 0):
                stripedLine = line.lstrip()

                # Skip blank lines
                if(len(stripedLine) == 0 or stripedLine.isspace()):
                    line = input_stream.readline()
                    continue

                # DI = delimit index
                question_DI = stripedLine.rstrip().find(QUESTION_DELIM)
                choice_DI = stripedLine.rstrip().find(CHOICE_DELIM)
                boundaryIndex = min_positive(
                    [stripedLine.find(ws) for ws in ws_list])

                if(DEBUG_MODE):
                    print("QDI: " + str(question_DI))
                    print("CDI: " + str(choice_DI))
                    print("BI: " + str(boundaryIndex))
                    print("stripLine: " + stripedLine.rstrip())
                    print("CUR RL: " + resultLine)

                # Found potential beginning of an item
                # delimitIndex < boundaryIndex avoid QUESTION_DELIM
                # being found way past the beginning
                if((question_DI != -1 and question_DI < boundaryIndex) or
                        (choice_DI != -1 and choice_DI < boundaryIndex)):

                    # If both delimiters are found in the same line,
                    # then we determine the type
                    # based on the contents of the substring prior to delimitor
                    # The beginning of a question
                    if(question_DI >= 0 and is_int(stripedLine[:question_DI])):
                        # Store what was previous
                        if(len(resultLine) > 0):
                            line_set.append((resultLine, CUR_TYPE))

                        CUR_TYPE = TYPE_QUESTION
                        text = stripedLine[question_DI+len(QUESTION_DELIM):]
                        resultLine = text.lstrip()
                    # The beginning of a choice
                    elif(choice_DI >= 0 and
                            is_alpha_only(stripedLine[:choice_DI])):
                        # Store what was previous
                        if(len(resultLine) > 0):
                            line_set.append((resultLine, CUR_TYPE))

                        CUR_TYPE = TYPE_CHOICE
                        resultLine = stripedLine.lstrip()
                    # If we were mistaken,
                    # then we assume its just part of the CUR_TYPE
                    else:
                        resultLine += stripedLine
                else:
                    # Assume continuation of CUR_TYPE
                    resultLine += stripedLine

                # Move to next line
                line = input_stream.readline()

            # Final item
            if(len(resultLine) > 0):
                line_set.append((resultLine, CUR_TYPE))

        file_lines.append(line_set)

    if(DEBUG_MODE):
        print(file_lines)

    # Now we create instances of Question given the tokenized file lines
    # file_lines should categorized lines of text into
    # TYPE_QUESTION, and TYPE_CATEGORIES
    fill_question_list(file_lines)


if __name__ == "__main__":
    # Validate our configuration
    if(validate_config() is False):
        exit(1)

    # Read in the questions from files
    # Append questions to question_list
    quizFiles = sys.argv[1:]
    if(len(quizFiles) == 0):
        usage()
        exit(0)

    parse_files(quizFiles)

    # Shuffle our list of questions
    random.shuffle(question_list)

    # Output the results
    for questionNum in range(len(question_list)):
        print("{0}{1} {2}".format(
            questionNum+1, QUESTION_DELIM, str(question_list[questionNum])))
