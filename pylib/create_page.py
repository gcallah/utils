from pylib.html_tags import details, par, link

indent1 = "            "  # type: str
indent2 = "                    "  # type: str


def html_start_stuff(page_title):
    link_line = '<link href="style.css" rel="stylesheet" type="text/css"/>\n'
    start_stuff = "<!DOCTYPE html>\n"
    start_stuff += "<html>\n"
    start_stuff += "    <head>\n"
    start_stuff += "        <meta charset=\"UTF-8\">\n"
    start_stuff += "        " + link_line
    start_stuff += "        <title>\n"
    start_stuff += "        " + page_title + "\n"
    start_stuff += "        </title>\n"
    start_stuff += "    </head>\n"
    start_stuff += "    <body>\n"
    start_stuff += "        <h1>\n"
    start_stuff += "        " + page_title + "\n"
    start_stuff += "        </h1>\n"
    return start_stuff


def html_end_stuff():
    end_stuff = "    </body>\n"
    end_stuff += "</html>\n"
    return end_stuff


def create_subtopics(outf, subtopics, level):
    s = ""
    for topic in subtopics:
        inner = ""
        if topic.subtopics is not None:
            inner += create_subtopics(outf, topic.subtopics, level + 1)
        s += details(topic.title, level=level, inc_par=True, inc_fig=True,
                     inner_details=inner)
    return s


def create_page(inf, outf, page_nm, subtopics=None,
                link_insert=None, doc_txt=None, hw_txt=None):
    for line in inf:
        outf.write(line)
        if "<title>" in line:
            outf.write(indent1 + page_nm + "\n")
        if "<h1>" in line:
            outf.write(indent2 + page_nm + "\n")
# after close h1, we will create subtopics and link:
        if "</h1>" in line:
            if subtopics is not None:
                outf.write(create_subtopics(outf, subtopics, 1))
# include documentation from source where indicated
        if "<!-- Include the documentation" in line:
            if doc_txt is not None:
                outf.write("<!--include " + doc_txt + " -->\n")
# include documentation from source where indicated
        if "<!-- Include the text material here!" in line:
            if hw_txt is not None:
                outf.write("<!--include " + hw_txt + " -->\n")
# include link to source code where indicated
        if "<!-- Include source code" in line:
            if link_insert is not None:
                outf.write(par(link(link_insert, "Source code")))
