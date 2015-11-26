#!/usr/bin/python3
#
# Usage: betbrain-premier.py [URL or FILE]
# Scrapes odds from passed betbrain page.

import sys
import os

from bs4 import BeautifulSoup
import urllib.request
from http.cookiejar import CookieJar

import parser
import printer

DEFAULT_URL = 'https://www.betbrain.com/football/england/premier-league/#!/matches/'

# If no arguments are present, it parses the default page.
# Argument can be an URL or a local file.
def main():
  html = getHtml(sys.argv)
  soup = BeautifulSoup(html, "html.parser")
  matches = parser.getMatches(soup)
  string = printer.matchesToString(matches)
  print(string)

def getHtml(argv):
  if len(argv) <= 1:
    return scrap(DEFAULT_URL)
  elif argv[1].startswith("http"):
    return scrap(argv[1])
  else:
    return readFile(argv[1])

# Returns html file located at URL.
def scrap(url):
  cj = CookieJar()
  opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
  try:
    return opener.open(url)
  except ValueError:
    print((os.path.basename(__file__)+": Invalid URL."))
    sys.exit(1)

def readFile(path):
  try:
    return open(path, encoding='utf8')
  except IOError:
    print((os.path.basename(__file__)+": Invalid filename."))
    sys.exit(1)

if __name__ == '__main__':
  main()
