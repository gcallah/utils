from pylib.html_tags import details, par, link

indent1 = "            "  # type: str
indent2 = "                    "  # type: str


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
                link_insert=None, temp_txt=None):
    for line in inf:
        outf.write(line)
        if "<title>" in line:
            outf.write(indent1 + page_nm + "\n")
        if "<h1>" in line:
            outf.write(indent2 + page_nm + "\n")
# after close h1, we will create subtopics and link:
        if "</h1>" in line:
            if link_insert is not None:
                outf.write(par(link(link_insert, "Source code")))
            if subtopics is not None:
                outf.write(create_subtopics(outf, subtopics, 1))
        if "<!-- Include" in line:
            if temp_txt is not None:
                outf.write("<!--include " + temp_txt + " -->\n")