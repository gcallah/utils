import urllib2
from bs4 import BeautifulSoup

try:
    from typing import Dict, Any
except ImportError:
    print("WARNING: Typing module is not find")

user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7' # type: str
headers = {'User-Agent': user_agent, }  # type: Dict[str, object]
request = urllib2.Request("https://devops.com", None, headers) # type: object
response = urllib2.urlopen(request, None, 5) # type: object
html = response.read() # type: object
soup = BeautifulSoup(html) # type: object
for tag in soup.find_all(attrs={"class": "slides"}):
    for atag in tag.find_all('a'):
        print atag['href']
        print atag.find('img')['src']