#!/usr/bin/python3
#
# Usage: betbrain.py [URL or FILE] [OUTPUT-FILE]
# Scrapes odds from passed betbrain page and writes them to
# stdout, or file if specified.

import os
import sys
import urllib.request

from bs4 import BeautifulSoup
from http.cookiejar import CookieJar

import parser_betbrain
import printer

DEFAULT_URL = 'https://www.betbrain.com/football/england/premier-league/#!/matches/'

# If no arguments are present, it parses the default page.
# Argument can be an URL or a local file.
def main():
  html = getHtml(sys.argv)
  soup = BeautifulSoup(html, "html.parser")
  matches = parser_betbrain.getMatches(soup)
  string = printer.matchesToString(matches)
  output(string, sys.argv)

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
    error("Invalid URL: " + url)

def readFile(path):
  try:
    return open(path, encoding='utf8')
  except IOError:
    error("Invalid input filename: " + path)

def output(string, argv):
  if len(argv) <= 2:
    print(string)
  else:
    writeFile(argv[2], string)

def writeFile(path, string):
  try:  
    fo = open(path, "w", encoding='utf8')
    fo.write(string);
    fo.close()
  except IOError:
    error("Invalid output filename: " + path)

def error(msg):
  msg = os.path.basename(__file__)+": "+msg
  print(msg, file=sys.stderr)
  sys.exit(1)

if __name__ == '__main__':
  main()
