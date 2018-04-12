import sys

def parseLine(line):
    if not line.strip():
        return [-1, "", None, None]

    # count stars
    star_count = 0
    for char in line:
        if char == '*':
            star_count += 1
        else:
            break
    # save title and section name
    splitted_line = line.split('^')
    if star_count == 0:
        # for title
        if len(splitted_line) != 2:
            print "ERROR: Bad input at %s. You must specify full-title and short-title." % line
            sys.exit()
        return [star_count, splitted_line[0], splitted_line[1]]
    else:
        section_name = splitted_line[0][star_count:]
        # save url and glyphicon if there is one
        # returns [star_count, section_name, url, glyphicon]
        if len(splitted_line) > 3:
            print "ERROR: Bad input at %s. At most 3 ^ separators are accepted." % line
            sys.exit()
        elif len(splitted_line) > 2:
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
    if start_star_count == 0:
        print "ERROR: Bad input at %s. Star count should be at least 1 in contents." % lines[0]
        sys.exit()
    start_index = 0
    end_index = 0
    level = []
    while end_index < len(lines):
        if not lines[end_index][1].strip():
            end_index += 1
        if lines[end_index][2] is None:
            end_index += 1
            if lines[end_index][0] != start_star_count + 1:
                print "ERROR: Bad input at %s. Number of stars does not match context." % lines[end_index][1]
                sys.exit()
            while end_index < len(lines) and lines[end_index][0] > start_star_count:
                end_index += 1
            level.append([lines[start_index][1], create_nested_list(lines[start_index + 1:end_index]), lines[start_index][3]])
        else:
            level.append(lines[end_index][1:4])
            end_index += 1
        start_index = end_index
    return level

def create_submenu(level_list, context_empty_spaces, submenu_id, submenu_counter, f):
	# if submenu_id is None, create a uncollapsable menu
	# else, create a collapsable menu
    if submenu_id is not None:
        f.write(create_line_with_spaces(context_empty_spaces, "<ul class=\"collapse list-unstyled\" id=\"Submenu%d\">\n" % submenu_id))
    else:
        f.write(create_line_with_spaces(context_empty_spaces, "<ul class=\"list-unstyled components\">\n"))
    for level in level_list:
        f.write(create_line_with_spaces(context_empty_spaces + 4, "<li>\n"))
        if isinstance(level[1], list):
            f.write(create_line_with_spaces(context_empty_spaces + 8, "<a href=\"#Submenu%d\" data-toggle=\"collapse\" aria-expanded=\"false\">\n" % submenu_counter))
            if level[2] is not None:
                f.write(create_line_with_spaces(context_empty_spaces + 12, "<i class=\"glyphicon %s\"></i>\n" % level[2]))
            f.write(create_line_with_spaces(context_empty_spaces + 12, level[0] + "\n"))
            f.write(create_line_with_spaces(context_empty_spaces + 8, "</a>\n"))
            submenu_counter += 1
            create_submenu(level[1], context_empty_spaces + 8, submenu_counter - 1, submenu_counter, f)
        else:
            f.write(create_line_with_spaces(context_empty_spaces + 8, "<a href=\"%s\">\n" % level[1]))
            if level[2] is not None:
                f.write(create_line_with_spaces(context_empty_spaces + 12, "<i class=\"glyphicon %s\"></i>\n" % level[2]))
            f.write(create_line_with_spaces(context_empty_spaces + 12, level[0] + "\n"))
            f.write(create_line_with_spaces(context_empty_spaces + 8, "</a>\n"))

        f.write(create_line_with_spaces(context_empty_spaces + 4, "</li>\n"))
    f.write(create_line_with_spaces(context_empty_spaces, "</ul>\n"))

# TO DO: should read file names from command line input
input_fname = sys.argv[-2]
output_fname = sys.argv[-1]
with open(input_fname) as f:
    lines = f.readlines()
lines = [line.rstrip('\n') for line in lines]
lines = [line.rstrip('\r') for line in lines] # for windows machines

parsed_lines = []
for line in lines:
    parsed_line = parseLine(line)
    # discard empty lines
    if parsed_line[0] > -1:
        parsed_lines.append(parsed_line)

title_line = parsed_lines[0]
# title is required
if title_line[0] != 0:
    print "ERROR: Bad input. No title found. Add a new line of <full-title>^<short-title> to the head of your input file."
    sys.exit()

# create a nested list with contents
nested = create_nested_list(parsed_lines[1:])

# write generated sidebar
with open(output_fname, 'w+') as f:
    # write title
    f.write("<!-- Sidebar Holder -->\n<nav id=\"sidebar\">\n    <div id=\"sidebarCollapse\">\n        <div class=\"sidebar-header\">\n            <h1>%s</h1>\n            <strong>%s</strong>\n        </div>\n    </div>\n" % (title_line[1], title_line[2]))

    # write contents
    context_empty_spaces = 4
    submenu_id = None
    submenu_counter = 0
    create_submenu(nested, context_empty_spaces, submenu_id, submenu_counter, f)

    f.write("</nav>\n")
