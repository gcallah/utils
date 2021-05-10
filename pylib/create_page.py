import pylib.html_tags as htags

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
    start_stuff += htags.heading(page_title)
    return start_stuff


def html_start_stuff(title, css="style.css"):
    """
    For web sites where we don't pre-process our html.
    Should be combined with above function!
    """
    start_stuff = "<!DOCTYPE html>\n"
    start_stuff += "<html>\n"
    start_stuff += htags.head(title=title, css=css)
    start_stuff += "    <body>\n"
    start_stuff += htags.heading(title)
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
        s += htags.details(topic.title, level=level,
                           inc_par=True, inc_fig=True, inner_details=inner)
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
        if "<!-- Include the extracted documentation" in line:
            if doc_txt is not None:
                page += "<!--include " + doc_txt + " -->\n"
# include documentation from source where indicated
        if "<!-- Include the code review here!" in line:
            if hw_txt is not None:
                page += "<!--include " + hw_txt + " -->\n"
# include lint report for source where indicated
        if "<!-- Include the linting report here!" in line:
            if lint_txt is not None:
                page += "<!--include " + lint_txt + " -->\n"
# include link to source code where indicated
        if "<!-- Include source code" in line:
            if link_insert is not None:
                page += htags.par(htags.link(link_insert, "Source code"))
    return page


def main():
    print("Let's create some html!")
    print("Here's the top o' page stuff:")
    print(html_start_stuff("Test Page!", css="../style.css"))
    print("Here's the bottom o' page stuff:")
    print(html_end_stuff())


if __name__ == "__main__":
    main()
