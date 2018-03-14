#!/usr/bin/awk -f
# this file processes django template files to turn them into ptml files

BEGIN {
    in_content = 0
    INDENT1 = "    "
    INDENT2 = INDENT1 INDENT1
    INDENT3 = INDENT2 INDENT1
    in_comments = 1
    error = 0
    if(ARGC < 3) {
        print "Must pass file to process and title" > "/dev/stderr"
        error = 1
        exit 1
    }
    title = ARGV[2]
}

/{% block content %}/ {
    in_content = 1
    print "<!DOCTYPE html>"
    print "<html>"
    print INDENT1 "<head>"
    print "<!--include head.txt -->"
    print INDENT2 "<title>"
    print INDENT3 "" title
    print INDENT2 "</title>"
    print INDENT1 "</head>"
    print ""
    print INDENT1 "<body>"
    print INDENT2 "<div class=\"wrapper\">"
    print "<!--include navbar.txt -->"
    print INDENT3 "<div id=\"content\">"
    print INDENT3 "<h1>"
    print INDENT3 "" title
    print INDENT3 "</h1>"
    next
}

/{% endblock content %}/ {
    next
}

{ 
    if(in_content) {
        print INDENT3 $0
    }
}

END {
    if(!error) {
        print INDENT3 "</div>"
        print INDENT2 "</div>"
        print INDENT1 "</body>"
        print "</html>"
    }
}

