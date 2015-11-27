import re
import collections

from bs4 import BeautifulSoup
from itertools import zip_longest

BASE_URL = "https://www.betbrain.com"

class Match:
  def __init__(self):
    self.bets = collections.OrderedDict()

### PUBLIC:

# Returns dictionary with match name for key and Match object
# for value:
#   crystal-palace-fc-v-sunderland -> {link: http://.., time:
#   12:09.., {AH: [4.40, 3.75, 1.93], ...}}
def getMatches(soup):
  matches = collections.OrderedDict()
  betNames = getBetNames(soup)
  bettingCategories = soup.findAll("div", "SubTabContent")
  for bettingCategory in bettingCategories:
    detailsOfMatches = bettingCategory.findAll("a", "MDInfo")
    bets = bettingCategory.findAll("ol", "OddsList ThreeWay")
    for matchDetails, bet in zip_longest(detailsOfMatches, bets, fillvalue=''):
      addMatch(matches, matchDetails, bet, betNames)
  return matches

### PRIVATE:

# Returns list of different betting categories: ["Away Home",
# "Asian Handicap", ...]
def getBetNames(soup):
  names = []
  betNamesContainers = soup.findAll("div", "SMItemContainer")
  for betNameContainer in betNamesContainers:
    name = betNameContainer.find("a", "OSLink")
    if not name:
      name = betNameContainer.find("a", "MMHeader")
    name = re.sub('Switch to the ', '', name['title'])
    name = re.sub(' detailed bet type', '', name)
    names.append(name)
  return names

# Adds match to the dictionary.
def addMatch(matches, matchDetails, bet, betNames):
  match = getMatch(matches, matchDetails)
  match.link = getLink(matchDetails)
  match.name = getName(matchDetails)
  match.time = getTime(matchDetails)
  odds = getOdds(bet)
  if not odds:
    return
  betsName = getBetsName(match, betNames)
  match.bets[betsName] = odds

# Returns existin match from matches or creates new one.
def getMatch(matches, matchDetails):
  matchId = getMatchId(matchDetails)
  if matchId in matches:
    return matches[matchId]
  else:
    match = Match()
    matches[matchId] = match
    return match

# Returns match name in form: team1-team2-[optional time].
def getMatchId(matchDetails):
  return re.search("[^/]*/$", matchDetails["href"]).group(0).replace('/', '')

# Returns link to the matche's page.
def getLink(matchDetails):
  return BASE_URL + matchDetails["href"]

# Returns matche's name.
def getName(matchDetails):
  name = re.sub('See ', '', matchDetails["title"])
  return re.sub(' match page', '', name)

# Returns start date of the match.
def getTime(matchDetails):
  return matchDetails.find("span", "Setting DateTime").find(text=True)

# Returns bet's odds in list: [4.40, 3.75, 1.93].
def getOdds(bet):
  if not bet:
    return ''
  odds = []
  for oddData in bet.findAll("li"):
    odd = oddData.find("span", "Odds")
    if odd:
      odds.append(odd.find(text=True))
      continue
    param = oddData.find("span", "Param")
    if param:
      odds.append(param.find(text=True))
  return odds

# Returns the bet category: "Asian Handicap".
def getBetsName(match, betNames):
  for betName in betNames:
    if betName not in match.bets:
      return betName
