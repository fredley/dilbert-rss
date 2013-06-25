dilbert-rss
===========

Scrapes dilbert.com and generates an RSS feed.

Since dilbert.com nerfed their own RSS feed, I created a tool to replicate the old functionality. This is designed to be used on your own server, using `cron` to update it. I don't plan on hosting a replacement feed myself.

You will need to install `BeautifulSoup` and `PyRSS2Gen` using `pip` or otherwise to run this script. Just run it from the command line with `python dilbert.py` to generate `dilbert.xml`.
