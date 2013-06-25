"""
Dilbert RSS Feed Generator
Requirements: BeautifulSoup, PyRSS2Gen
http://github.com/fredley/dilbert-rss

"""

import urllib2, datetime, PyRSS2Gen
from BeautifulSoup import BeautifulSoup

def getDetails(url):
    page = urllib2.urlopen(url).read()
    soup = BeautifulSoup(page)
    date = soup.findAll('div', {'class': 'STR_DateStrip'})[0].text
    img = soup.findAll('div', {'class': 'STR_Image' })[0].find('img')['src']
    results = {}
    results['item'] = PyRSS2Gen.RSSItem(
        title = 'Comic for ' + date,
        description = "<a href='" + url + "'><img src='" + url + str(img) + "' /></a>",
        pubDate = datetime.datetime.strptime(date,"%B %d, %Y"),
        link = url,
        guid = PyRSS2Gen.Guid(url)
    )
    results['prev_href'] = soup.findAll('span', text='Previous')[0].parent.parent['href']
    return results

url = 'http://dilbert.com'
page = urllib2.urlopen(url).read()
soup = BeautifulSoup(page)
nextUrl = url + soup.findAll('div', {'class': 'STR_Image' })[0].find('a')['href']
strips = []

for i in range(0,10):
    details = getDetails(nextUrl)
    strips.append(details['item'])
    nextUrl = url + details['prev_href']

# Construct RSS
rss = PyRSS2Gen.RSS2(
    title = "Dilbert Daily Strip",
    link = "http://dilbert.com",
    description = "An unofficial RSS feed for dilbert.com.",
    lastBuildDate = datetime.datetime.now(),
    items = strips)

rss.write_xml(open("dilbert.xml", "w"))

