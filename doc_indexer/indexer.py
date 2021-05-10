"""
This module will generate an index page for pydoc generated documentations
files in a particular directory.ç:w
"""
import os
import glob

import pylib.create_page as cp
import pylib.html_tags as tags

css_loc = os.getenv("CSS_LOC", "style.css")


def main():
    print(cp.html_start_stuff("Document Index", css=css_loc))
    links = []
    for name in glob.glob('*.html'):
        links.append(tags.link(name, name))
    print(tags.ulist(l=links))
    print(cp.html_end_stuff())

if __name__ == "__main__":
    main()
