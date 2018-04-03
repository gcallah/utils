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
    splitted_line = line.split('^', 1)
    section_name = splitted_line[0][star_count:]

    # save url if there is one
    if len(splitted_line) > 1:
        url = splitted_line[1]
    else:
        url = None

    return [star_count, section_name, url]

def create_line_with_spaces(n, str):
    return ' ' * n + str

input_fname = "sidebar_input_sample.txt"
output_fname = "sidebar_output_sample.txt"
with open(input_fname) as f:
    lines = f.readlines()
lines = [line.rstrip('\n') for line in lines]
lines = [line.rstrip('\r') for line in lines] # for windows machines

parsed_lines = [parseLine(line) for line in lines]

# create a nested list
nested = []
i = 0
while i < len(parsed_lines):
	# filter empty lines
    if not parsed_lines[i][1].strip():
        i += 1
        continue
    level = []
    if parsed_lines[i][0] == 0:
    	# if the line has no url
    	# treat it as a collaspable and expand it
        if parsed_lines[i][2] is None:
            level = [parsed_lines[i][1]]
            sublevel = []
            j = i + 1
            if j >= len(parsed_lines):
                print "ERROR: Bad input at %s" % parsed_lines[i][1]
                sys.exit()
            while j < len(parsed_lines) and parsed_lines[j][0] > 0:
                if parsed_lines[j][0] != 1:
                    print "ERROR: Bad input at %s" % parsed_lines[j][1]
                    sys.exit()
                subsublevel = [parsed_lines[j][1], []]
                k = j + 1
                if k >= len(parsed_lines):
                    print "ERROR: Bad input at %s" % parsed_lines[j][1]
                    sys.exit()
                while k < len(parsed_lines) and parsed_lines[k][0] > 1:
                    if parsed_lines[k][0] != 2:
                        print "ERROR: Bad input at %s" % parsed_lines[k][1]
                        sys.exit()
                    subsublevel[1].append([parsed_lines[k][1], parsed_lines[k][2]])
                    k += 1
                sublevel.append(subsublevel)
                j = k
            level.append(sublevel)
            i = j
        # if the line does have a url
        # create a link tab
        else:
            level = [parsed_lines[i][1], parsed_lines[i][2]]
            i += 1
        nested.append(level)
    else:
        print "ERROR: Bad input at %s" % parsed_lines[i][1]
        sys.exit()

# write generated sidebar
with open(output_fname, 'w+') as f:
    # write title
    f.write("<!-- Sidebar Holder -->\n<nav id=\"sidebar\">\n    <div id=\"sidebarCollapse\">\n        <div class=\"sidebar-header\">\n            <h1>DevOps</h1>\n            <strong>DO</strong>\n        </div>\n    </div>\n")

    # write lists
    f.write("    <ul class=\"list-unstyled components\">\n")

    context_empty_spaces = 8 #add several empty spaces before the html code
    submenu_counter = 0
    for level in nested:
        f.write(create_line_with_spaces(context_empty_spaces, "<li>\n"))
        if isinstance(level[1], list):
            f.write(create_line_with_spaces(context_empty_spaces + 4, "<a href=\"#Submenu%d\" data-toggle=\"collapse\" aria-expanded=\"false\">\n" % submenu_counter))
            #f.write(create_line_with_spaces(context_empty_spaces + 8, "<i class=\"glyphicon glyphicon-duplicate\"></i>\n"))
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
            #f.write(create_line_with_spaces(context_empty_spaces + 8, "<i class=\"glyphicon glyphicon-home\"></i>\n"))
            f.write(create_line_with_spaces(context_empty_spaces + 8, level[0] + "\n"))
            f.write(create_line_with_spaces(context_empty_spaces + 4, "</a>\n"))

        f.write(create_line_with_spaces(context_empty_spaces, "</li>\n"))
    f.write("    </ul>\n</nav>\n")
