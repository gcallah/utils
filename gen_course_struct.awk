#!/usr/bin/awk -f

# This program generates the ptml files for a new course.
# It reads stdin for the course section names.

BEGIN {
    FS = "^"
    TEMPLATE = "./utils/templates/template.ptml"
    CREATE = "./utils/create_page.py"
}

/^$/ { }       # blank lines allowed

/^\;/ { }      # allows comments in the input

/^\t\t|        / {     # this is a bottom-level section
    title = $1
    print title
    print $2
    new_file = $2
    sub(/html/, "ptml", new_file)  # change the extension
    new_file = "html_src/" new_file
    if (system( "[ -f " new_file " ] ") == 0)
        print new_file " already exists."
    else {
        print "We are going to add " new_file
        if (system(CREATE " < " TEMPLATE " > " new_file) != 0) {
            print "Could not create " new_file
        }
    }
}

/^\t[^\t]/ {       # major section name: no file for now
}

/^[^\t ]/ {       # major section name: no file for now
}

