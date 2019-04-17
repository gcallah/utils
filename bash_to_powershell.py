import sys

try:
    fileName = sys.argv[1]
except IndexError:
    print("Please provide a file to convert")
    sys.exit()

newFileName = str(fileName).split(".sh")[0] + "_converted.ps1"

fileContent = open(fileName, "r")
convertedFile = open(newFileName, "w+")

insideFunction = False


def convertConditions(s):
    s = s.replace("[", "(", 1)
    s = s[::-1].replace("]", ")")[::-1]
    s = s.replace("[", "")
    s = s[::-1].replace("]", "")[::-1]
    s = s.replace("=", "-eq")
    s = convertOperators(s)
    return s


def convertOperators(s):
    s = s.replace("==", "-eq")
    s = s.replace("!=", "-ne")
    s = s.replace("&&", "-and")
    s = s.replace("||", "-or")
    return s


def convertFunctionArguments(s):
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
                    s = s[:start-1] + "$args[" + s[start:start+len(arg)] + \
                        "]" + s[start+len(arg):]
                    i += 5
                    arg = None
                variableFound = False
        i += 1
    if variableFound and s[start:].isnumeric():
        s = s[:start-1] + "args[" + s[start:start+len(arg)] + \
            "]" + s[start+len(arg):]
    return s


for line in fileContent:
    line = line.strip()
    if line == "set -e":
        line = "$erroractionpreference = \"stop\""
    elif line.startswith("export "):
        line = line.replace("export ", "$", 1)
    elif line.startswith("pwd"):
        line = line.replace("pwd", "Get-Location")
    elif line.startswith("touch"):
        line = line.replace("touch", "echo $null >>")
    elif line.startswith("rm"):
        line = line.replace("rm", "Remove-Item")
    elif line.startswith("diff"):
        line = line.replace("diff", "Compare-Object")
    elif line.startswith("tail"):
        line = line.replace("tail -n", "Get-Content -Tail ")
        # when -n parameter is not specified (default is -n10)
        line = line.replace("tail", "Get-Content -Tail 10")
    elif line.startswith("grep"):
        line = line.replace("grep", "Select-String")
    elif line.startswith("find"):
        line = line.replace("find", "Get-ChildItem")
    elif "python3" in line:
        line = line.replace("python3", "python")
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
        line += ")"
    elif line.startswith("done"):
        line = line.replace("done", "}")
    elif line.startswith("do"):
        line = line.replace("do", "{")

    if insideFunction:
        if "$" in line:
            line = convertFunctionArguments(line)
        elif "}" in line:
            insideFunction = False

    line = convertOperators(line)
    line = line.replace("echo", "Write-Host")
    convertedFile.write(line + "\n")

fileContent.close()
convertedFile.close()
