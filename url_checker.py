"""
Script to check validity of anchor tag links in an HTML file.
"""

from html.parser import HTMLParser
import argparse
import urllib.request as req

ARG_ERROR = 1  # type: int
PARSE_ERROR = 2  # type: int
IO_ERROR = 3   # type: int

LINE_NO = 0  # type: int


def line_msg():  # type: () -> str
    return " at line number " + str(LINE_NO)


class OurHTMLParser(HTMLParser):
    """
    Our descendant of base HTMLParser class: we override just the methods we
    need to.
    """
    def __init__(self):  # type: () -> None
        super(OurHTMLParser, self).__init__(convert_charrefs=False)

    def handle_starttag(self, tag, attrs):  # type: (str, object) -> None
        """
        This is a callback function that is used by HTMLParser for start tags:
            it is called!
        """

        # Find anchor tags and href attr
        if (tag == 'a' and len(attrs) != 0):
            if attrs[0][0] == 'href':
                url = attrs[0][1]
                try:
                    print("Going to try " + url)
                    is_accessible(url)
                except req.HTTPError as http_e:
                    print(str(http_e.getcode()) + " for file " +
                          html_file + " at url " + url)
                except req.URLError:
                    print(req.URLError.reason + " for file " +
                          html_file + " at url " + url)


def is_accessible(link, abs_link="http://www.thedevopscourse.com"):
    """
    Function that accesses a url string and returns response status code.
    """
    possible_slash = ''
    if link.startswith('http') or link.startswith('https'):
        req.urlopen(link)
    else:
        if not link.startswith('/'):
            possible_slash = '/'
        result_link = abs_link + possible_slash + link
        req.urlopen(result_link)
    return True  # this needs to return false if not accesible!


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("html_file",
                            help="html file to be parsed")
    args = arg_parser.parse_args()
    html_file = args.html_file
    parser = OurHTMLParser()

    try:
        file = open(html_file, "r")
        for line in file:
            LINE_NO += 1
            parser.feed(line)
    except IOError:
        print("Couldn't read " + html_file)
        exit(IO_ERROR)

    exit(0)
