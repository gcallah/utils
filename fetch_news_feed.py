#!/usr/bin/env python

import urllib2
from bs4 import BeautifulSoup

try:
    from typing import Dict, Any, List
except ImportError:
    print("WARNING: Typing module is not found")

user_agent = ("Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) "
              "Gecko/2009021910 Firefox/3.0.7")  # type: str
headers = {'User-Agent': user_agent, }  # type: Dict[str, object]
request = urllib2.Request("https://devops.com", None, headers)  # type: object
response = urllib2.urlopen(request, None, 5)  # type: object
html = response.read()  # type: object
soup = BeautifulSoup(html)  # type: object
news = {}  # type: Dict[Any, Any]

for tag in soup.find_all(attrs={"class": "slides"}):
    for atag in tag.find_all('a'):
        print(atag['href'])
        print(atag.find('img')['src'])
        news[atag['href']] = atag.find('img')['src']

index_page = BeautifulSoup(open("../index.html"), "html.parser")
count = 0  # type: int

for tag in index_page.find_all(attrs={"class": "carItem"}):
    tag['onclick'] = ("window.location.href='"
                      + list(news.keys())[count] + "'")  # type :List[str]
    tag['src'] = news[list(news.keys())[count]]
    count += 1

with open("../index.html", "w") as file:
    file.write(index_page.prettify().encode('utf-8').strip())
