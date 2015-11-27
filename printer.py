import re

MATCH_SEP = '\n'
KEY_VALUE_SEP = ';'
PROPERTY_SEP = '\n'

### PUBLIC:

# Converts dictionary of matches to string.
def matchesToString(matches):
  string = ""
  for id, match in matches.items():
    string += matchToString(id, match) + MATCH_SEP
  return string

### PRIVATE:

# Converts match to string.
def matchToString(id, match):
  out = "link" + KEY_VALUE_SEP + match.link + PROPERTY_SEP
  out += "time" + KEY_VALUE_SEP + match.time + PROPERTY_SEP
  out += "name" + KEY_VALUE_SEP + match.name + PROPERTY_SEP
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
    