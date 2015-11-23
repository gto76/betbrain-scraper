#!/usr/bin/python
#
# Usage: betbrain-premier.py [URL or FILE]
# Scrapes odds from passed betbrain page.

import sys
import re
import collections
import os

from BeautifulSoup import BeautifulSoup
import urllib2
from cookielib import CookieJar

import stringifier

DEFAULT_URL = 'https://www.betbrain.com/football/england/premier-league/#!/matches/'

# If no arguments present it parses the default page.
# Argument can be an URL or a local file.
def main():
  html = ""
  if len(sys.argv) <= 1:
    html = scrap(DEFAULT_URL)
  elif sys.argv[1].startswith("http"):
    html = scrap(sys.argv[1])
  else:
    html = readFile(sys.argv[1])
  soup = BeautifulSoup(html)
  matches = getMatches(soup)
  string = stringifier.matchesToString(matches)
  print(string)

# Reads webpage.
def scrap(url):
  cj = CookieJar()
  opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
  try:
    return opener.open(url)
  except ValueError:
    print os.path.basename(__file__)+": Invalid URL."
    sys.exit(1)

def readFile(path):
  try:
    return open(path)
  except IOError:
    print os.path.basename(__file__)+": Invalid filename."
    sys.exit(1)

# Returns dictionary of matches. Example of key/value pair:
#   crystal-palace-fc-v-sunderland -> [[4.40, 3.75, 1.93], ...]
def getMatches(soup):
  matches = collections.OrderedDict()
  for i in range(1, 4):
    subTab = soup.find("div", "SubTabContent SubTab"+str(i))
    details = subTab.findAll("a", "MDInfo")
    oddLists = subTab.findAll("ol", "OddsList ThreeWay")
    for detail, oddList in zip(details, oddLists):
      addMatch(matches, detail, oddList)
  return matches

# Adds match to the dictionary.
def addMatch(matches, detail, oddList):
  pair = getPair(detail)
  odds = getOdds(oddList)
  if pair in matches:
    matches[pair].append(odds)
  else:
    matches[pair] = [odds]

# Returns pair of teams.
def getPair(detail):
  return re.search("[^/]*/$", detail["href"]).group(0).replace('/', '')

# Returns odds as list of lists: [[4.40, 3.75, 1.93], ...]
def getOdds(oddList):
  odds = []
  for oddData in oddList.findAll("li"):
    odd = oddData.find("span", "Odds")
    if odd:
      odds.append(odd.find(text=True))
      continue
    param = oddData.find("span", "Param")
    if param:
      odds.append(param.find(text=True))
  return odds

if __name__ == '__main__':
  main()
