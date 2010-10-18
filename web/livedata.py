#!/usr/bin/python

# This script takes advantage of a hidden api on the nfl.com
# website, which updates the score strip up on the top of the
# main nfl.com webpage ;O)
#
# Its in non-standard json format, so we have to massage it a bit to
# import the data

# Example data
#  ['Sun', '1:00', 'final overtime', None, 'MIA', '23', 'GB', '20', None, None, '54940', None, 'REG6', '2010']
#  ['Sun', '1:00', 'Final', None, 'SD', '17', 'STL', '20', None, None, '54946', None, 'REG6', '2010']
#  ['Sun', '1:00', 'final overtime', None, 'BAL', '20', 'NE', '23', None, None, '54942', None, 'REG6', '2010']
#  ['Sun', '1:00', 'Final', None, 'CLE', '10', 'PIT', '28', None, None, '54945', None, 'REG6', '2010']
#  ['Sun', '1:00', 'Final', None, 'KC', '31', 'HOU', '35', None, None, '54941', None, 'REG6', '2010']
#  ['Sun', '1:00', 'Final', None, 'DET', '20', 'NYG', '28', None, None, '54943', None, 'REG6', '2010']
#  ['Sun', '1:00', 'Final', None, 'ATL', '17', 'PHI', '31', None, None, '54944', None, 'REG6', '2010']
#  ['Sun', '1:00', 'Final', None, 'SEA', '23', 'CHI', '20', None, None, '54939', None, 'REG6', '2010']
#  ['Sun', '1:00', 'Final', None, 'NO', '31', 'TB', '6', None, None, '54947', None, 'REG6', '2010']
#  ['Sun', '4:05', '4', '05:26', 'NYJ', '17', 'DEN', '17', 'DEN', '0', '54948', None, 'REG6', '2010']
#  ['Sun', '4:05', '4', '07:14', 'OAK', '9', 'SF', '17', 'OAK', '0', '54949', None, 'REG6', '2010']
#  ['Sun', '4:15', '4', '04:05', 'DAL', '21', 'MIN', '24', 'MIN', '0', '54950', None, 'REG6', '2010']
#  ['Sun', '8:20', 'Pregame', None, 'IND', None, 'WAS', None, None, None, '54951', None, 'REG6', '2010']
#  ['Mon', '8:30', 'Pregame', None, 'TEN', None, 'JAC', None, None, None, '54952', None, 'REG6', '2010']

import re
from urllib import urlopen

url = "http://www.nfl.com/liveupdate/scorestrip/scorestrip.json"

raw = urlopen(url).read()

# Replace empty csv values with "None"
# Here we have to use a positive lookahead assertion "(?=,)"
# which means that we match any two commas together ",," and
# replace it with ",None,"
m = re.compile(",(?=,)")
formatted = m.sub(",None", raw)

# A well formatted JSON string can be eval'd into a python dictionary
data = eval(formatted)

for x in data['ss']:
	print x

