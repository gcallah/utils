from pylib.html_tags import details

indent1 = "            " # type: str
indent2 = "                    " # type: str

def create_subtopics(outf, subtopics, level):
    inner = ""
    for topic in subtopics:
        if topic.subtopics is not None:
            inner += create_subtopics(outf, topic.subtopics, level + 1)
        s += details(topic.title, level=level, inc_par=True, inc_fig=True,
                     inner_details=inner)
    return s

def create_page(inf, outf, page_nm, subtopics=None):
    for line in inf:
        outf.write(line)
        if "<title>" in line:
            outf.write(indent1 + page_nm + "\n")
        if "<h1>" in line:
            outf.write(indent2 + page_nm + "\n")
# after close h1, we will create subtopics:
        if "</h1>" in line and subtopics is not None:
            s = create_subtopics(outf, subtopics, 1)
            outf.write(s)
