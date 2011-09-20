#!/usr/bin/python

# Scrapes vegasinsider.com for NFL lines, scores, and matchups

from BeautifulSoup import BeautifulSoup
import urllib2
from datetime import date


year = 2010
# Set this date to the tuesday prior to the first regular season game
curr_week = (date.today() - date(2011, 9, 6)).days / 7

for week in range(1, curr_week+2):
	page = urllib2.urlopen('http://www.vegasinsider.com/nfl/scoreboard/scores.cfm/week/%d/season/%d'%(week,year))
	soup = BeautifulSoup(page)

	for box in soup('td', 'sportPicksBorder'):
		out = []
		out.append(str(week))
		line = ''
	
		# Find the (Abbreviated) teams in the game
		road = box.table.tbody.findAll('tr')[3].findAll('td')[0].a.string
		home = box.table.tbody.findAll('tr')[4].findAll('td')[0].a.string
		out.append(str(home))
		out.append(str(road))
	
		# Find the odds and determine which is the line
		rline = box.table.tbody.findAll('tr')[3].findAll('td')[1].string.strip('&nbsp;')
		hline = box.table.tbody.findAll('tr')[4].findAll('td')[1].string.strip('&nbsp;')
	
		# They put both the line and the over/under in random places
		# Assuming the over/under is always greater than the line, we take
		# the smallest to be the line
		try:
			line = -float(rline) if (abs(float(rline)) < abs(float(hline))) else float(hline)
		except ValueError:
			try:
				line = float(hline)
			except ValueError:
				pass

		out.append(str(line))
	
		# Grab the scores if the games have been completed
		try:
			rscore = int(box.table.tbody.findAll('tr')[3].findAll('td')[6].font.b.string.strip().strip('&nbsp;'))
			hscore = int(box.table.tbody.findAll('tr')[4].findAll('td')[6].font.b.string.strip().strip('&nbsp;'))
			out.append(str(hscore))
			out.append(str(rscore))
		except AttributeError:
			# This error will be thrown if the game goes into overtime
			# But I don't feel like scraping the quarter rows so i'll just
			# grab the 5th quarter here.
			rscore = int(box.table.tbody.findAll('tr')[3].findAll('td')[7].font.b.string.strip().strip('&nbsp;'))
			hscore = int(box.table.tbody.findAll('tr')[4].findAll('td')[7].font.b.string.strip().strip('&nbsp;'))
			out.append(str(hscore))
			out.append(str(rscore))
		except IndexError:
			# This error will be thrown if the game doesn't have a score
			# We can safetly ignore it
			pass
	
		print ",".join(out)
