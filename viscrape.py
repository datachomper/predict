#!/usr/bin/python

from lxml.html import parse
import urllib
import StringIO

doc = parse('http://www.vegasinsider.com/nfl/scoreboard/scores.cfm/week/2/season/2010').getroot()
print type(doc)
# <td class="sportsPicksBorder">
for table in doc.cssselect('span.sub_title_red'):
	print table.text_content()
