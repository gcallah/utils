import sys

try:
    fileName = sys.argv[1]
except:
    print("Please provide a file to convert")
    sys.exit()

newFileName = str(fileName).split(".sh")[0] + "_converted.sh"

fileContent = open(fileName, "r")
convertedFile = open(newFileName, "w+")

def replaceConditions(s):
    s = s.replace("[", "(", 1)
    s = s[::-1].replace("]", ")")[::-1]
    s = s.replace("[", "")
    s = s[::-1].replace("]", "")
    s = s.replace("=", "-eq")
    s = s.replace("==", "-eq")
    s = s.replace("!=", "-ne")
    s = s.replace("&&", "-and")
    s = s.replace("||", "-or")
    return s

for line in fileContent:
    line = line.strip()
    if line == "set -e":
        line = "$erroractionpreference = \"stop\""
    elif line.startswith("export "):
        line = line.replace("export ", "$", 1)
    elif line.startswith("touch"):
        line.replace("touch", "echo $null >>")
    elif line.startswith("if"):
        line = replaceConditions(line)
    elif line.startswith("elif"):
        line = "} \n" + line
        line = line.replace("elif", "elseif")
        line = replaceConditions(line)
    elif line.startswith("then"):
        line = "{"
    elif line.startswith("else"):
        line = "} \n" + line
        line = line.replace("else", "else {")
    elif line.startswith("fi"):
        line = "}"
    convertedFile.write(line + "\n")

fileContent.close()
convertedFile.close()
