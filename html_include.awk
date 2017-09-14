#!/usr/bin/awk -f
# this file preprocesses HTML files to put in includes

BEGIN {
}

/<!--include/ {
    file = $2

    # Need to set TEMPLATE_DIR in ENV
    template_path = ENVIRON["TEMPLATE_DIR"]
    if (template_path != "") {
        file = template_path "/" $2
    }

    while((getline < file ) > 0 ) {
    	print $0
    }
    close(file)
    next
}

{ print }
