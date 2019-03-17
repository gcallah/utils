import sys

fileName = sys.argv[1]
newFileName = str(fileName).split(".sh")[0] + "_converted.sh"

fileContent = open(fileName, "r")
convertedFile = open(newFileName, "w+")

for line in fileContent:
    line = line.strip()
    if line == "set -e":
        convertedFile.write("$erroractionpreference = \"stop\"\n")

fileContent.close()
convertedFile.close()
