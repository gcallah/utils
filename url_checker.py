"""
Script to check validity of anchor tag links in an HTML file.
"""

from html.parser import HTMLParser
import argparse
import urllib.request as req
import socket

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
                    is_accessible(url, abs_link)
                except req.HTTPError as http_e:
                    code = http_e.getcode()
                    if code != 403:
                        print("[" + str(code) + "] URL " + url + " " +
                              str(http_e.reason).lower() + " in file " +
                              html_file)
                except req.URLError as url_e:  # DNS/Proxy issue
                    if isinstance(url_e.reason, socket.timeout):
                        print("Timed out for url " +
                            url + " in file " + html_file)
                    else:
                        errno = str(url_e.reason).split("]")[0].split()[-1]
                        if errno == "-2" or errno == "8":
                            url_e.reason = "Server cannot be reached"
                        print(str(url_e.reason) + " for url " +
                            url + " in file " + html_file)


def is_accessible(link, abs_link):
    """
    Function that accesses a url string and returns response status code.
    """

    if '{' in link:  # fancy Django link: we can't handle it!
        return True

    result_link = link
    possible_slash = ''
    if (not link.startswith('http')) and (not link.startswith('https')):
        if not link.startswith('/'):
            possible_slash = '/'
        result_link = abs_link + possible_slash + link

    req.urlopen(result_link, timeout=30).read().decode('utf-8')
    return True  # this needs to return false if not accesible!


if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("html_file",
                            help="html file to be parsed")
    arg_parser.add_argument("abs_link",
                            help="absolute link to be parsed")
    args = arg_parser.parse_args()
    html_file = args.html_file
    abs_link = args.abs_link
    parser = OurHTMLParser()

    try:
        file = open(html_file, "r", encoding="utf8")
        for line in file:
            LINE_NO += 1
            parser.feed(line)
    except IOError:
        print("Couldn't read " + html_file)
        exit(IO_ERROR)

    exit(0)
