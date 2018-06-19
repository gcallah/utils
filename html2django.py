# This file converts between our html format and django template files.
# Pass the file to convert on the command line.
# Writes to stdout.

import sys

try:
    from typing import TextIO,List
except ImportError:
    print("WARNING!")

if len(sys.argv) < 2:
    print("Must supply an HTML file.")
    exit(1)

html_file = sys.argv[1] # type: str

# [Prof] - the file name has to come from command line
# f = open('C:/Users/VivekPC/Desktop/about.html',"r")
f = open(html_file, "r") # type: TextIO
input = f.readlines() # type: List[str]
f.close()

# Testing
# print input
# print '-'*60


# remove list items from <!DOCTYPE html> to next 22 lines (inclusive)
# [Prof] - we need to go until we start seeing text that wil appeR ON SCREEN
# [Prof] - These tags could include: <hn> - where n can be 1 - 5 or <p> or <figure> or <img>
pos1 = 0 # type: int
for i in range(len(input)):
    if "<!DOCTYPE html>" in input[i]:
        pos1 = i

pos2 = 0 # type: int
for i in range(len(input)):
    if "<h1>" in input[i] or "<p>" in input[i] or "<h2>" in input[i] \
        or "<h3>" in input[i] or "<h4>" in input[i] or "<h5>" in input[i]\
            or "<figure>" in input[i]:  # or "<img" in input[i]:
        pos2 = i
        break

# del input[0:22+1]

del input[pos1:pos2]

# Removing tag </html>
# [Prof] - remove from </body> onwards
pos3 = 0 # type: int
for line in range(len(input)):
  if  "</body>" in input[line]:
    pos3 = line

del input[pos3:]


output = []  # type: List[str]
output.append("""{% extends "base.html" %}""""\n")
output.append("""{% block content %}""""\n")
output.append("""<div class="module">""""\n")
for i in range(len(input)):
    output.append(input[i])

output.append("""{% endblock content %}""")
# mypy code find type error here: line is defined as int, but it need to be string in this expression
for line in output:
    print(line, end="")

