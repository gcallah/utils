from pylib.html_tags import details, par, link

indent1 = "            "  # type: str
indent2 = "                    "  # type: str


def ptml_start_stuff(page_title):
    """
    For serving static web sites where we pre-process our html.
    """
    start_stuff = "<!DOCTYPE html>\n"
    start_stuff += "<html>\n"
    start_stuff += "    <head>\n"
    start_stuff += "<!--include head.txt -->\n"
    start_stuff += "        <title>\n"
    start_stuff += "        " + page_title + "\n"
    start_stuff += "        </title>\n"
    start_stuff += "    </head>\n"
    start_stuff += "    <body>\n"
    start_stuff += "<!--include logo.txt -->\n"
    start_stuff += "<!--include menu.txt -->\n"
    start_stuff += "        <h1>\n"
    start_stuff += "        " + page_title + "\n"
    start_stuff += "        </h1>\n"
    return start_stuff


def html_end_stuff():
    end_stuff = "    </body>\n"
    end_stuff += "</html>\n"
    return end_stuff


def create_subtopics(subtopics, level):
    s = ""
    for topic in subtopics:
        inner = ""
        if topic.subtopics is not None:
            inner += create_subtopics(topic.subtopics, level + 1)
        s += details(topic.title, level=level, inc_par=True, inc_fig=True,
                     inner_details=inner)
    return s


def create_page(inf, page_nm, subtopics=None,
                link_insert=None, doc_txt=None, hw_txt=None, lint_txt=None):
    page = ""
    for line in inf:
        page += line
        if "<title>" in line:
            page += indent1 + page_nm + "\n"
        if "<h1>" in line:
            page += indent2 + page_nm + "\n"
# after close h1, we will create subtopics and link:
        if "</h1>" in line:
            if subtopics is not None:
                page += create_subtopics(subtopics, 1)
# include documentation from source where indicated
        if "<!-- Include the documentation" in line:
            if doc_txt is not None:
                page += "<!--include " + doc_txt + " -->\n"
# include documentation from source where indicated
        if "<!-- Include the text material here!" in line:
            if hw_txt is not None:
                page += "<!--include " + hw_txt + " -->\n"
# include lint report for source where indicated
        if "<!-- Include the linting report here!" in line:
            if lint_txt is not None:
                page += "<!--include " + lint_txt + " -->\n"
# include link to source code where indicated
        if "<!-- Include source code" in line:
            if link_insert is not None:
                page += par(link(link_insert, "Source code"))
    return page
