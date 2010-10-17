#!/usr/bin/python

# This script takes advantage of a hidden api on the nfl.com
# website, which updates the score strip up on the top of the
# main nfl.com webpage ;O)
#
# Its in non-standard json format, so we have to massage it a bit to
# import the data

import re
from urllib import urlopen

url = "http://www.nfl.com/liveupdate/scorestrip/scorestrip.json"

raw = urlopen(url).read()

# Replace empty csv values with "None"
# Twice, because I suck at regexp I guess and ",," doesn't match ",,,"
m = re.compile(",,")
formatted = m.sub(",None,", raw)
formatted = m.sub(",None,", formatted)

data = eval(formatted)

for x in data['ss']:
	print x
