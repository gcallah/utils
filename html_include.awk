#!/usr/bin/awk -f
# this file preprocesses HTML files to put in includes

BEGIN {
    # Need to set TEMPLATE_DIR in ENV
    template_path = ENVIRON["TEMPLATE_DIR"]
    quiz_path = ENVIRON["QUIZ_DIR"]
}

/<!--include/ {
    file = $2

    # if file starts with 'quiz' use quiz_path not template_path
    if (quiz_path != "" && match($2, /quiz)) {
        file = quiz_path "/" $2
    }
    else if (template_path != "") {
        file = template_path "/" $2
    }
    while((getline < file ) > 0 ) {
    	print $0
    }
    close(file)
    next
}

{ print }
