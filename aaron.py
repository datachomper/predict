#!/usr/bin/python

# Scrapes vegasinsider.com for NFL lines, scores, and matchups
# Outputs the data in a format easily importable for Aaron's spreadsheet

from BeautifulSoup import BeautifulSoup
import urllib2
from datetime import date
import HTML

year = 2010
curr_week = (date.today() - date(2010, 9, 7)).days / 7

print "<html><head><link rel=\"stylesheet\" href=\"style.css\">"
print "<link rel=\"stylesheet\" href=\"../style.css\"></head>"

for week in range(1, curr_week+3):
	page = urllib2.urlopen('http://www.vegasinsider.com/nfl/scoreboard/scores.cfm/week/%d/season/%d'%(week,year))
	soup = BeautifulSoup(page)
	
	herp = []
	for box in soup('td', 'sportPicksBorder'):
		out = []
	
		# Find the (Abbreviated) teams in the game
		road = box.table.tbody.findAll('tr')[3].findAll('td')[0].a.string
		home = box.table.tbody.findAll('tr')[4].findAll('td')[0].a.string
		out.append(str(road))
	
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
		out.append(str(home))
	
		# Grab the scores if the games have been completed
		try:
			rscore = int(box.table.tbody.findAll('tr')[3].findAll('td')[6].font.b.string.strip().strip('&nbsp;'))
			hscore = int(box.table.tbody.findAll('tr')[4].findAll('td')[6].font.b.string.strip().strip('&nbsp;'))
			out.append(rscore)
			out.append(hscore)
		except AttributeError:
			# This error will be thrown if the game goes into overtime
			# But I don't feel like scraping the quarter rows so i'll just
			# grab the 5th quarter here.
			rscore = int(box.table.tbody.findAll('tr')[3].findAll('td')[7].font.b.string.strip().strip('&nbsp;'))
			hscore = int(box.table.tbody.findAll('tr')[4].findAll('td')[7].font.b.string.strip().strip('&nbsp;'))
			out.append(rscore)
			out.append(hscore)
		except IndexError:
			# This error will be thrown if the game doesn't have a score
			# We can safetly ignore it
			pass
	
		herp.append(out)

	print "<h2>Week", week,"</h2>"
	print HTML.table(herp, header_row=['road', 'line', 'home', 'rscore', 'hscore'], 
			attribs={'id': 'hor-minimalist-a'}, style="", cellpadding=0,
			border=0)
