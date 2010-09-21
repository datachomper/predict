#!/usr/bin/python

# Scrapes vegasinsider.com for NFL lines, scores, and matchups
# Outputs the data in a format easily importable for Aaron's spreadsheet

from BeautifulSoup import BeautifulSoup
import urllib2
from datetime import date

year = 2010
curr_week = (date.today() - date(2010, 9, 7)).days / 7

for week in range(1, curr_week+3):
	print "Week %d"%(week)
	page = urllib2.urlopen('http://www.vegasinsider.com/nfl/scoreboard/scores.cfm/week/%d/season/%d'%(week,year))
	soup = BeautifulSoup(page)
	
	for box in soup('td', 'sportPicksBorder'):
		out = []
	
		# Find the (Abbreviated) teams in the game
		road = box.table.tbody.findAll('tr')[3].findAll('td')[0].a.string
		home = box.table.tbody.findAll('tr')[4].findAll('td')[0].a.string
		out.append(road)
	
		# Find the odds and determine which is the line
		rline = box.table.tbody.findAll('tr')[3].findAll('td')[1].string.strip('&nbsp;')
		hline = box.table.tbody.findAll('tr')[4].findAll('td')[1].string.strip('&nbsp;')
	
		# They put both the line and the over/under in random places
		# Assuming the over/under is always greater than the line, we take
		# the smallest to be the line
		try:
			line = -float(rline) if (abs(float(rline)) < abs(float(hline))) else float(hline)
			out.append(str(line))
		except ValueError:
			# Ignore it if we don't have any lines
			pass
		out.append(home)
	
		# Grab the scores if the games have been completed
		status = box.find('span', 'sub_title_red').contents[0].strip()
		if status == "Final Score":
			try:
				rscore = (box.table.tbody.findAll('tr')[3].findAll('td')[6].font.b.string.strip().strip('&nbsp;'))
				hscore = (box.table.tbody.findAll('tr')[4].findAll('td')[6].font.b.string.strip().strip('&nbsp;'))
			except AttributeError:
				# Seems to be safe to ignore this error for now I think it's a false positive
				# print box.table.tbody.findAll('tr')[3].findAll('td')[6]
				pass
	
			out.append(rscore)
			out.append(hscore)
	
		print '\t'.join(out)
