import re

MATCH_SEP = '\n'
TEAM_SEP = ' '
KEY_VALUE_SEP = ':'
ODDS_SEP = ' '
ODDS_CATEGORY_SEP = ';'

# Converts dictionary to string.
def matchesToString(matches):
  string = ""
  for pair, odds in matches.items():
    string += matchToString(pair, odds) + MATCH_SEP
  return string

# Converts dictionary pair to string. Output example:
# manchester-city swansea-city:1.29 6.50 12.00,1.78 2.23,2.15 1.82
def matchToString(pair, odds):
  (team1, team2) = getTeams(pair)
  return team1 +TEAM_SEP+ team2 +KEY_VALUE_SEP+ oddsToString(odds)

# Extracts team names from pair string.
def getTeams(pair):
  date = re.search("[-0-9]*$", pair)
  pair = pair[:date.start()]
  teams = re.search("-v-", pair)
  team1 = pair[:teams.start()]
  team2 = pair[teams.end():]
  return (team1, team2)

# Converts odds (list of lists) to string.
def oddsToString(odds):
  categoryOdds = []
  for odd in odds.odds:
    categoryOdds.append(ODDS_SEP.join(odd))
  return ODDS_CATEGORY_SEP.join(categoryOdds)
    