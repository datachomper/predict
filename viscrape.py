#!/usr/bin/python

# Scrapes vegasinsider.com for NFL lines, scores, and matchups

from BeautifulSoup import BeautifulSoup
import urllib2

year = 2010
week = 2

page = urllib2.urlopen('http://www.vegasinsider.com/nfl/scoreboard/scores.cfm/week/%d/season/%d'%(week,year))
soup = BeautifulSoup(page)

for box in soup('td', 'sportPicksBorder'):
	out = []

	# Find the (Abbreviated) teams in the game
	road = box.table.tbody.findAll('tr')[3].findAll('td')[0].a.string
	home = box.table.tbody.findAll('tr')[4].findAll('td')[0].a.string
	out.append(home)
	out.append(road)

	# Find the odds and determine which is the line
	rline = box.table.tbody.findAll('tr')[3].findAll('td')[1].string.strip('&nbsp;')
	hline = box.table.tbody.findAll('tr')[4].findAll('td')[1].string.strip('&nbsp;')

	# They put both the line and the over/under in random places
	# Assuming the over/under is always greater than the line, we take
	# the smallest to be the line
	line = -float(rline) if (abs(float(rline)) < abs(float(hline))) else float(hline)
	out.append(line)

	# Grab the scores if the games have been completed
	status = box.find('span', 'sub_title_red').contents[0].strip()
	if status == "Final Score":
		try:
			rscore = int(box.table.tbody.findAll('tr')[3].findAll('td')[6].font.b.string.strip().strip('&nbsp;'))
			hscore = int(box.table.tbody.findAll('tr')[4].findAll('td')[6].font.b.string.strip().strip('&nbsp;'))
		except AttributeError:
			# Seems to be safe to ignore this error for now I think it's a false positive
			# print box.table.tbody.findAll('tr')[3].findAll('td')[6]
			pass

		out.append(hscore)
		out.append(rscore)

	print out
