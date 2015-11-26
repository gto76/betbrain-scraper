import re

MATCH_SEP = '\n'
KEY_VALUE_SEP = ';'
PROPERTY_SEP = '\n'

### PUBLIC:

# Converts dictionary of matches to string.
def matchesToString(matches):
  string = ""
  for name, match in matches.items():
    string += matchToString(name, match) + MATCH_SEP
  return string

### PRIVATE:

# Converts dictionary name to string. Output example:
# manchester-city swansea-city:1.29 6.50 12.00,1.78 2.23,2.15 1.82
def matchToString(name, match):
  out = "link" + KEY_VALUE_SEP + match.link + PROPERTY_SEP
  out += "time" + KEY_VALUE_SEP + match.time + PROPERTY_SEP
  out += "name" + KEY_VALUE_SEP + name + PROPERTY_SEP
  out += getBets(match)
  return out

def getBets(match):
  out = ""
  for bet, odds in match.bets.items():
    out += "bet" + KEY_VALUE_SEP + bet + PROPERTY_SEP
    out += "odds" + KEY_VALUE_SEP + ' '.join(odds) + PROPERTY_SEP
  return out

# Extracts team names from name string.
# def getTeams(name):
#   date = re.search("[-0-9]*$", name)
#   name = name[:date.start()]
#   teams = re.search("-v-", name)
#   team1 = name[:teams.start()]
#   team2 = name[teams.end():]
#   return (team1, team2)
    