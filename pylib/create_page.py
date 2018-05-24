from pylib.html_tags import details
indent1 = "            " # type: str
indent2 = "                    " # type: str

def output_subtopics(outf, subtopics, level):
    for topic in subtopics:
        s = details(topic.title, level=level)
        outf.write(s)
        if topic.subtopics is not None:
            output_subtopics(outf, topic.subtopics, level + 1)

def create_page(inf, outf, page_nm, subtopics=None):
    for line in inf:
        outf.write(line)
        if "<title>" in line:
            outf.write(indent1 + page_nm + "\n")
        if "<h1>" in line:
            outf.write(indent2 + page_nm + "\n")
# after close h1, we will output subtopics:
        if "</h1>" in line and subtopics is not None:
            output_subtopics(outf, subtopics, 1)
