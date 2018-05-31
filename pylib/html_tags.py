# a collection of functions for outputting HTML

INDENT1 = "    "
INDENT2 = INDENT1 + INDENT1
INDENT4 = INDENT2 + INDENT2

def details(sumtext, level=1, indent=INDENT4):
    s = indent + '<details>\n'
    s += indent + INDENT1 + '<summary class="sum' + str(level) + '">\n'
    s += indent + INDENT1 + sumtext + "\n"
    s += indent + INDENT1 + '</summary>\n'
    s += indent + '</details>\n'
    return s
    
