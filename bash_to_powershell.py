import sys

try:
    fileName = sys.argv[1]
except:
    print("Please provide a file to convert")
    sys.exit()

newFileName = str(fileName).split(".sh")[0] + "_converted.sh"

fileContent = open(fileName, "r")
convertedFile = open(newFileName, "w+")

for line in fileContent:
    line = line.strip()
    if line == "set -e":
        line = "$erroractionpreference = \"stop\""
    elif line.startswith("export "):
        line.replace("export ", "$", 1)
    convertedFile.write(line + "\n")

fileContent.close()
convertedFile.close()
