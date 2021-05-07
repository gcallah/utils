"""
This module will generate an index page for pydoc generated documentations
files in a particular directory.ç:w
"""
import glob
import pylib.create_page as cp
import pylib.html_tags as tags


def main():
    print(cp.html_start_stuff("Document Index"))
    links = []
    for name in glob.glob('*.html'):
        links.append(tags.link(name, name))
    print(tags.ulist(l=links))
    print(cp.html_end_stuff())

if __name__ == "__main__":
    main()
