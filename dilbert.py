#!/usr/bin/env python

"""
Dilbert RSS Feed Generator
Requirements: BeautifulSoup, PyRSS2Gen
http://github.com/fredley/dilbert-rss

"""

import urllib2, datetime, sys, re
import PyRSS2Gen
from BeautifulSoup import BeautifulSoup

def getDetails(url, baseURL):
    page = urllib2.urlopen(url).read()
    soup = BeautifulSoup(page)
    date = soup.findAll('date')[0].text
    pubDate = datetime.datetime.strptime(date, "%A %B %d,%Y")
    img = soup.findAll('div', {'class': 'img-comic-container' })[0].find('img')['src']

    results = {}
    results['item'] = PyRSS2Gen.RSSItem(
        title = 'Dilbert comic for ' + pubDate.strftime("%B %d, %Y"),
        description = "<a href='" + url + "'><img src='" + str(img) + "' /></a>",
        pubDate = pubDate,
        link = url,
        guid = PyRSS2Gen.Guid(url)
    )
    results['prev_href'] = soup.findAll('div', {'class': re.compile('nav-left')})[0].find('a')['href']
    return results

url = 'http://dilbert.com'
page = urllib2.urlopen(url).read()
soup = BeautifulSoup(page)
nextUrl = soup.findAll('div', {'class': re.compile('comic-item-container') })[0].find('a')['href']
strips = []

for i in range(0,10):
    details = getDetails(nextUrl,url)
    strips.append(details['item'])
    nextUrl = url + details['prev_href']

# Construct RSS
rss = PyRSS2Gen.RSS2(
    title = "Dilbert Daily Strip",
    link = "http://dilbert.com",
    description = "An unofficial RSS feed for dilbert.com.",
    lastBuildDate = datetime.datetime.now(),
    items = strips)

if len(sys.argv) > 1:
    outfile = sys.argv[1]
else:
    outfile = "dilbert.xml"
rss.write_xml(open(outfile, "w"))

