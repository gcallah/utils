# a collection of functions for outputting HTML

INDENT1 = "    "
INDENT2 = INDENT1 + INDENT1
INDENT4 = INDENT2 + INDENT2

    
def par(text=None, indent=INDENT4):
    s = indent + '<p>\n'
    if text is not None:
        s += text + '\n'
    s += indent + '</p>\n'
    return s
    
def figure(src="", caption=None, indent=INDENT4):
    # by default we get an empty figure tag
    s = indent + '<figure>\n'
    s += indent + INDENT1 + '<img src="' + src + '" width="40%">\n'
    s += indent + INDENT1 + '<figcaption>\n'
    if caption is not None:
        s += indent + INDENT1 + caption + "\n"
    s += indent + INDENT1 + '</figcaption>\n'
    s += indent + '</figure>\n'
    return s

def details(sumtext, level=1, indent=INDENT4, inc_par=False, inc_fig=False,
           inner_details=None):
    indent += INDENT1 * (level - 1)
    s = indent + '<details>\n'
    inner_indent = indent + INDENT1   # add one level indentation
    s += inner_indent + '<summary class="sum' + str(level) + '">\n'
    s += inner_indent + sumtext + "\n"
    s += inner_indent + '</summary>\n'
    if inc_fig:
        s += figure(indent=inner_indent)
    if inc_par:
        s += par(indent=inner_indent)
    if inner_details is not None:
        s += inner_details
    s += indent + '</details>\n'
    return s

