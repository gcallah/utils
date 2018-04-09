import sys

def parseLine(line):
    # count stars
    star_count = 0
    for char in line:
        if char == '*':
            star_count += 1
        else:
            break

    # save section name
    splitted_line = line.split('^')
    section_name = splitted_line[0][star_count:]

    # save url and glyphicon if there is one
    # returns [star_count, section_name, url, glyphicon]
    if len(splitted_line) > 2:
        return [star_count, section_name, splitted_line[1], splitted_line[2]]
    elif len(splitted_line) > 1:
        if splitted_line[1].startswith("glyphicon"):
            return [star_count, section_name, None, splitted_line[1]]
        else:
            return [star_count, section_name, splitted_line[1], None]
    else:
        return [star_count, section_name, None, None]


def create_line_with_spaces(n, str):
    return ' ' * n + str

def create_nested_list(lines):
    if len(lines) == 0:
        print "UNEXPECTED ERROR: Empty list in recursion"
        sys.exit()
    start_star_count = lines[0][0]
    start_index = 0
    end_index = 0
    level = []
    while end_index < len(lines):
        if not lines[end_index][1].strip():
            end_index += 1
        if lines[end_index][2] is None:
            end_index += 1
            if lines[end_index][0] <= start_star_count:
                print "ERROR: Bad input format at %s" % lines[end_index][1]
                sys.exit()
            while end_index < len(lines) and lines[end_index][0] > start_star_count:
                end_index += 1
            level.append([lines[start_index][1], create_nested_list(lines[start_index + 1:end_index]), lines[start_index][3]])
        else:
            level.append(lines[end_index][1:4])
            end_index += 1
        start_index = end_index
    return level

input_fname = "sidebar_input_sample.txt"
output_fname = "sidebar_output_sample.txt"
with open(input_fname) as f:
    lines = f.readlines()
lines = [line.rstrip('\n') for line in lines]
lines = [line.rstrip('\r') for line in lines] # for windows machines

parsed_lines = [parseLine(line) for line in lines]

# create a nested list
nested = create_nested_list(parsed_lines[2:len(parsed_lines)-1])

# write generated sidebar
with open(output_fname, 'w+') as f:
    # write title
    f.write("<!-- Sidebar Holder -->\n<nav id=\"sidebar\">\n    <div id=\"sidebarCollapse\">\n        <div class=\"sidebar-header\">\n            <h1>%s</h1>\n            <strong>%s</strong>\n        </div>\n    </div>\n" % (lines[0][1], lines[1][1]))

    # write lists
    f.write("    <ul class=\"list-unstyled components\">\n")

    context_empty_spaces = 8 #add several empty spaces before the html code
    submenu_counter = 0
    for level in nested:
        f.write(create_line_with_spaces(context_empty_spaces, "<li>\n"))
        if isinstance(level[1], list):
            f.write(create_line_with_spaces(context_empty_spaces + 4, "<a href=\"#Submenu%d\" data-toggle=\"collapse\" aria-expanded=\"false\">\n" % submenu_counter))
            if level[2] is not None:
                f.write(create_line_with_spaces(context_empty_spaces + 8, "<i class=\"glyphicon %s\"></i>\n" % level[2]))
            f.write(create_line_with_spaces(context_empty_spaces + 8, level[0] + "\n"))
            f.write(create_line_with_spaces(context_empty_spaces + 4, "</a>\n"))
            f.write(create_line_with_spaces(context_empty_spaces + 4, "<ul class=\"collapse list-unstyled\" id=\"Submenu%d\">\n" % submenu_counter))
            submenu_counter += 1
            for sublevel in level[1]:
                f.write(create_line_with_spaces(context_empty_spaces + 8, "<li>\n"))
                f.write(create_line_with_spaces(context_empty_spaces + 12, "<a href=\"#Submenu%d\" data-toggle=\"collapse\" aria-expanded=\"false\">%s</a>\n" % (submenu_counter, sublevel[0])))
                f.write(create_line_with_spaces(context_empty_spaces + 12, "<ul class=\"collapse list-unstyled\" id=\"Submenu%d\">\n" % submenu_counter))
                submenu_counter += 1
                for subsublevel in sublevel[1]:
                    f.write(create_line_with_spaces(context_empty_spaces + 16, "<li><a href=\"%s\">%s</a></li>\n" % (subsublevel[1], subsublevel[0])))

                f.write(create_line_with_spaces(context_empty_spaces + 12, "</ul>\n"))
                f.write(create_line_with_spaces(context_empty_spaces + 8, "</li>\n"))
            f.write(create_line_with_spaces(context_empty_spaces + 4, "</ul>\n"))
        else:
            f.write(create_line_with_spaces(context_empty_spaces + 4, "<a href=\"%s\">\n" % level[1]))
            if level[2] is not None:
                f.write(create_line_with_spaces(context_empty_spaces + 8, "<i class=\"glyphicon %s\"></i>\n" % level[2]))
            f.write(create_line_with_spaces(context_empty_spaces + 8, level[0] + "\n"))
            f.write(create_line_with_spaces(context_empty_spaces + 4, "</a>\n"))

        f.write(create_line_with_spaces(context_empty_spaces, "</li>\n"))
    f.write("    </ul>\n</nav>\n")
