#!/usr/bin/awk -f
# this file preprocesses HTML files to put in includes

BEGIN {
    # Don't need BEGIN for now!
}


/<body>/ {
    print
    print "<!--include menu.txt -->"
    next
}

{ print }
