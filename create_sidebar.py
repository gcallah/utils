def parseLine(line):
	# count tabs
	tab_count = 0
	for char in line:
		if char == '\t':
			tab_count += 1
		else:
			break

	# save section name
	splitted_line = line.split('^', 1)
	section_name = splitted_line[0][tab_count:]

	# save url if there is one
	if len(splitted_line) > 1:
		url = splitted_line[1]
	else:
		url = None

	return [tab_count, section_name, url]

input_fname = "sidebar_input_sample.txt"
output_fname = "sidebar_output_sample.txt"
with open(input_fname) as f:
	lines = f.readlines()
lines = [line.rstrip('\n') for line in lines]
lines = [line.rstrip('\r') for line in lines] # for windows machines

parsed_lines = [parseLine(line) for line in lines]

# write generated sidebar
with open(output_fname, 'w+') as f:
	# write title
	f.write("<!-- Sidebar Holder -->\n<nav id=\"sidebar\">\n    <div id=\"sidebarCollapse\">\n        <div class=\"sidebar-header\">\n            <h1>DevOps</h1>\n            <strong>DO</strong>\n        </div>\n    </div>\n")
	
	# write lists
	f.write("    <ul class=\"list-unstyled components\">\n")
	
	# save some vars here to remind us to handle bad inputs
	# add more if you find more :)
	link_with_no_subtitle = True # a link with >0 tabcount but without a preceding subtitle

	context_empty_spaces = 8 # TO DO: add several empty spaces before your html code
	for parsed_line in parsed_lines:
		# filter empty lines
		if not parsed_line[1].strip():
			# TO DO: may throw an angry message here
			continue
		# TO DO: finish this section
		f.write("pass\n")

	f.write("    </ul>\n</nav>\n")