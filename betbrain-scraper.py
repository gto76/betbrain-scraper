#!/usr/bin/python
#
# Usage: betbrain-premier.py [URL or FILE]
# Scrapes odds from passed betbrain page.

import sys
import re
import collections
import os

from bs4 import BeautifulSoup
import urllib.request
from http.cookiejar import CookieJar
from itertools import zip_longest

import util

DEFAULT_URL = 'https://www.betbrain.com/football/england/premier-league/#!/matches/'

class Match:
  def __init__(self):
    self.bets = collections.OrderedDict()

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
  soup = BeautifulSoup(html, "html.parser")
  matches = getMatches(soup)
  string = util.matchesToString(matches)
  print(string)

# Reads webpage.
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

# Returns dictionary of matches. Example of key/value pair:
#   crystal-palace-fc-v-sunderland -> [[4.40, 3.75, 1.93], ...]
def getMatches(soup):
  matches = collections.OrderedDict()
  bets = getBets(soup)
  for i in range(1, 4):
    subTab = soup.find("div", "SubTab"+str(i))
    details = subTab.findAll("a", "MDInfo")
    oddLists = subTab.findAll("ol", "OddsList ThreeWay")
    for detail, oddList in zip_longest(details, oddLists, fillvalue=''):
      addMatch(matches, detail, oddList, bets)
  return matches

# Returns list of different betting categories: ["AH", "OU", ...]
def getBets(soup):
  bbb = []
  bets = soup.findAll("div", "SMItemContainer")
  for bet in bets:
    b = bet.find("a", "OSLink")
    if not b:
      b = bet.find("a", "MMHeader")
    b = re.sub('Switch to the ', '', b['title'])
    b = re.sub(' detailed bet type', '', b)
    bbb.append(b)
  return bbb

# Adds match to the dictionary.
def addMatch(matches, detail, oddList, bets):
  name = getName(detail)
  
  if oddList:
    catOdds = getSingleCategoryOdds(oddList)
  else:
    catOdds = ''
  
  if name in matches:
    match = matches[name]
  else:
    match = Match()
    matches[name] = match

  bet = getBet(match, bets)
  match.bets[bet] = catOdds
  match.link = detail["href"]
  match.time = getTime(detail)

def getBet(match, bets):
  for bet in bets:
    if bet not in match.bets:
      return bet

# Returns match name in form: team1-team2-[optional time].
def getName(detail):
  return re.search("[^/]*/$", detail["href"]).group(0).replace('/', '')

# Returns start date of the match.
def getTime(detail):
  return detail.find("span", "Setting DateTime").find(text=True)

# Returns odds as list of lists: [4.40, 3.75, 1.93]
def getSingleCategoryOdds(oddList):
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
