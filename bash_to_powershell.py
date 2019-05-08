import argparse


def parseArguments():
    # create argument parser
    parser = argparse.ArgumentParser()
    # positional mandatory arguments
    parser.add_argument("file",
                        help="Please provide a file to convert.",
                        type=str)
    # optional arguments
    parser.add_argument("-d", "--defaultParams",
                        help="Add default parameters for makefile.",
                        type=bool, default=False)
    # parse arguments
    args = parser.parse_args()
    return args

args = parseArguments()
fileName = args.file

newFileName = str(fileName).split(".sh")[0] + "_powershell.ps1"

fileContent = open(fileName, "r")
powershellFile = open(newFileName, "w+")

if args.defaultParams:
    powershellFile.write("$TEST_DIR = \"tests\"" + "\n")
    powershellFile.write("$TEST_DATA = \"test_data\"" + "\n")
    powershellFile.write("$LIB_DIR = \"pylib\"" + "\n")
    powershellFile.write("$CODE_DIR = \".\"" + "\n")
    powershellFile.write("$HTML_DIR = \".\"" + "\n")
    powershellFile.write("$DATA_DIR = $CODE_DIR + \"/data\"" + "\n")
    powershellFile.write("$DOCKER_DIR = \"docker\"" + "\n")
    powershellFile.write("\n")

insideDiff = False
insideFunction = False
stack = []


def convertConditions(s):
    s = s.replace("[", "(", 1)
    s = s[::-1].replace("]", ")")[::-1]
    s = s.replace("[", "")
    s = s[::-1].replace("]", "")[::-1]
    s = s.replace("=", "-eq")
    s = convertOperators(s)
    return s


def convertOperatorConditions(s, op):
    if op == "&&":
        newOp = "-and"
    elif op == "||":
        newOp = "-or"
    conditions = s.split(op)
    s = ""
    for condition in conditions[:-1]:
        s += "(" + condition + ") " + newOp + " "
    s += conditions[-1] + " | out-null"
    return s


def convertOperators(s):
    s = s.replace("true", "$true")
    s = s.replace("false", "$false")
    s = s.replace("==", "-eq")
    s = s.replace("!=", "-ne")
    if "&&" in s:
        s = convertOperatorConditions(s, "&&")
    if "||" in s:
        s = convertOperatorConditions(s, "||")
    return s


def convertDiffStatement(s):
    """
    This function converts the diff statement provided that it is
    in the following format: diff a b
    where a and b are two files to be compared
    """
    sList = s.split()
    file1, file2 = sList[1], sList[2]
    return "if ( -not (Compare-Object (Get-Content " + file1 + \
           ") (Get-Content " + file2 + ")) ) {"


def convertFunctionArgument(s, start, arg):
    return s[:start-1] + "$($args[" + \
           str(int(s[start:start+len(arg)])-1) + \
           "])" + s[start+len(arg):]


def findAndConvertFunctionArguments(s):
    i, arg = 0, None
    variableFound = False
    while i < len(s):
        if s[i] == "$":
            variableFound = True
            start = i+1
        elif variableFound:
            if s[start:i+1].isnumeric():
                arg = s[start:i+1]
            else:
                if arg:
                    s = convertFunctionArgument(s, start, arg)
                    i += 5
                    arg = None
                variableFound = False
        i += 1
    if variableFound and s[start:].isnumeric():
        s = convertFunctionArgument(s, start, arg)
    return s


for line in fileContent:
    line = line.strip()
    if line == "set -e":
        line = "$erroractionpreference = \"stop\""
    elif line.startswith("export "):
        line = line.replace("export ", "$", 1)
    elif line.startswith("pwd"):
        line = line.replace("pwd", "Get-Location")
    elif line.startswith("touch "):
        line = line.replace("touch ", "echo $null >>")
    elif line.startswith("tail"):
        line = line.replace("tail -n", "Get-Content -Tail ")
        # when -n parameter is not specified (default is -n10)
        line = line.replace("tail", "Get-Content -Tail 10")
    elif line.startswith("grep "):
        line = line.replace("grep ", "Select-String")
    elif line.startswith("find "):
        line = line.replace("find ", "Get-ChildItem")
    elif line.startswith("python3 ") or line.startswith("python "):
        line = line.replace("python3", "python")
        # handling "<" operator as it is not allowed in powershell
        if "<" in line:
            lineSplit = line.split(">")
            interchange = lineSplit[0]
            outputLocExists = False
            if len(lineSplit) > 1:
                outputLocExists = True
                outputLoc = lineSplit[1]
            lineSplit = interchange.split("<")
            line = lineSplit[1] + "| " + lineSplit[0]
            if outputLocExists:
                line += ">" + outputLoc
            line = "Get-Content" + line
    elif line.startswith("if"):
        line = convertConditions(line)
    elif line.startswith("elif"):
        line = "} \n" + line
        line = line.replace("elif", "elseif")
        line = convertConditions(line)
    elif line.startswith("then"):
        line = "{"
    elif line.startswith("else"):
        line = "} \n" + line
        line = line.replace("else", "else {")
    elif line.startswith("fi"):
        line = "}"
    elif "()" in line:
        line = "function " + line
        line = line.replace("()", "")
        insideFunction = True
    elif line.startswith("for"):
        line = line.replace("for ", "foreach ($")
        line = line.replace(";", "")
        if "*" in line:
            forStatement = line.split("in")
            temp, directory = forStatement[0], forStatement[1]
            # the Force parameter handles hidden files
            line = temp + "in " + "Get-ChildItem -Path " + \
                directory + " -Force"
        line += ")"
    elif line.startswith("done"):
        line = line.replace("done", "}")
    elif line.startswith("do"):
        line = line.replace("do", "{")
    elif line.startswith("cp "):
        line = line.replace("cp ", "Copy-Item ")
    elif line.startswith("mv "):
        line = line.replace("mv ", "Move-Item ")
    elif line.startswith("rm "):
        line = line.replace("rm ", "Remove-Item ")
    elif line.startswith("diff "):
        insideDiff = True
        line = convertDiffStatement(line)
    elif line.startswith("echo "):
        line = line.replace("echo ", "Write-Host ")

    if insideDiff and "}" in line:
        line = "}\n" + \
                "else {\n" + \
                "Write-Host \"Comparison failed.\"\n" + \
                "}\n" + \
                line
        insideDiff = False

    if insideFunction:
        if "$" in line:
            line = findAndConvertFunctionArguments(line)
        elif "{" in line:
            stack.append("{")
        elif "}" in line:
            if not stack:
                insideFunction = False
            else:
                stack.pop()

    line = convertOperators(line)
    powershellFile.write(line + "\n")

fileContent.close()
powershellFile.close()
