#!/usr/bin/python
#
# Usage: betbrain-premier.py 
# 

import sys
import re
import collections

from BeautifulSoup  import BeautifulSoup
from urllib2 import urlopen

BASE_URL = "https://www.betbrain.com/"
URL = "https://www.betbrain.com/football/england/premier-league/#!/matches/"

def main():
  # html = urlopen(URL).read()
  # soup = BeautifulSoup(html, "lxml")
  soup = BeautifulSoup(open("index.html"))
  matches = parseSoup(soup)
  string = matchesToString(matches)
  print(string)

def parseSoup(soup):
  # Key/value pair example: 
  #   crystal-palace-fc-v-sunderland -> [[4.40, 3.75, 1.93], ...]
  matches = collections.OrderedDict()
  for i in range(1, 4):
    subTab = soup.find("div", "SubTabContent SubTab"+str(i))
    details = subTab.findAll("a", "MDInfo")
    oddLists = subTab.findAll("ol", "OddsList ThreeWay")
    for detail, oddList in zip(details, oddLists):
      pair = getPair(detail)
      odds = getOdds(oddList)
      if pair in matches:
        matches[pair].append(odds)
      else:
        matches[pair] = [odds]
  return matches

def getPair(detail):
  return re.search("[^/]*/$", detail["href"]).group(0).replace('/', '')

def getOdds(oddList):
  odds = []
  for oddData in oddList.findAll("li"):
    odd = oddData.find("span", "Odds")
    if odd:
      odds.append(odd.find(text=True))
  return odds

def matchesToString(matches):
  string = ""
  for pair, odds in matches.items():
    string += matchToString(pair, odds) + '\n'
  return string

def matchToString(pair, odds):
  (team1, team2) = getTeams(pair)
  return team1 +":"+ team2 +";"+ oddsToString(odds)

def getTeams(pair):
  teams = re.search("-v-", pair)
  team1 = pair[:teams.start()]
  team2 = pair[teams.end():]
  return (team1, team2)

def oddsToString(odds):
  categoryOdds = []
  for odd in odds:
    categoryOdds.append(' '.join(odd))
  return ':'.join(categoryOdds)
    
if __name__ == '__main__':
  main()
