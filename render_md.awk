#!/usr/bin/awk -f

# this file processes ptml files to include and render markdown files in them.


BEGIN {
    # Need to set the folder of markdown files
    markdown_path = ENVIRON["MARKDOWN_DIR"]
    RENDER = "python3 ./utils/render_md.py "

}

/<!-- *include/ {
    file = $2

    # file has a forward slash in it, leave it alone:
    if(!match($2, /\//)) {
        # if file is a markdown
        if (match(file, ".*\.md$")){
            is_markdown = 1
            if(markdown_path != ""){
                file = markdown_path "/" $2
            }
        }
    }
    i = 0
    # if it's a markdown file
    if(is_markdown==1){
        # render markdown first
        cmd = RENDER file
        while((cmd | getline) >0 ){
            print $0
            i++
        }
        close(cmd)
        if(i == 0){
            s = "<p>We attempted to render markdown file from " file " but failed.</p>"
            print s > "/dev/stderr"
            print s
        }
    }else{
        print $0
    }



    next
}

{ print }
