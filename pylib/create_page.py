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
                link_insert=None, doc_txt=None):
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
# include link to source code where indicated
        if "<!-- Include source code" in line:
            if link_insert is not None:
                outf.write(par(link(link_insert, "Source code")))