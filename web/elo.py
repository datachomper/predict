#!/usr/bin/python

from django.core.management import setup_environ
import settings
setup_environ(settings)
from data.models import Box
from numpy import std, average
import sys
import types
import re
from urllib import urlopen

tally = {}
delta = []
rating = {}

def distance(x, y):
	if (x <= 0) and (y >= 0):
		return y + abs(x)
	if (y <= 0) and (x >= 0):
		return x + abs(y)
	if (y < 0) and (x < 0):
		return abs(abs(y) - abs(x))
	return abs(x - y)

class Stat():
	def __unicode__(self):
		return self.rate

	def __init__(self):
		self.win = 0
		self.loss = 0
		self.rate = 1500

# Grab year argument to the script
year = 2010
for arg in sys.argv[1:]:
	year = arg
	break

# Find number of weeks of data that are available
num_weeks_avail = Box.objects.filter(year=year).order_by('-week')[0].week

# Iterate over each week's games
for week in range(1, num_weeks_avail+1):
	matches = Box.objects.filter(week=week, year=year)
	print ""
	print "Week:", week
	for match in matches:
		# Create a stat object for teams
		if not match.home in tally:
			tally[match.home] = Stat()
		if not match.road in tally:
			tally[match.road] = Stat()

		# Create a rating listing so we can watch how the team's
		# ratings change week over week
		if not match.home in rating:
			rating[match.home] = []
		if not match.road in rating:
			rating[match.road] = []

		# Keep win/loss ratio tally per week
		winloss = Stat()

		# The Casino's are much smarter than I am so we pre-seed our ratings
		# by reverse engineering their spread predictions
		if week == 1:
			tally[match.home].rate = 1500 - int((match.line * 100/7)/2)
			tally[match.road].rate = 1500 + int((match.line * 100/7)/2)

		# Find accuracy of curent ELO
		prediction = (tally[match.road].rate - tally[match.home].rate)*7/100

		# Keep track of weekly ratings
		rating[match.home].append(('2009W'+str(week), str(tally[match.home].rate)))
		rating[match.road].append(('2009W'+str(week), str(tally[match.road].rate)))

		# We have three states, we're either pre-games, during-games, or post games
		if type(match.hscore) is types.NoneType:
			# No final score data yet, check if we're mid-games
			url = "http://www.nfl.com/liveupdate/scorestrip/scorestrip.json"
			raw = urlopen(url).read()
			
			print "%s(%d) vs %s(%d) : predicted %d : line %d" % (match.home, tally[match.home].rate, match.road, tally[match.road].rate, prediction, match.line)

			# If there is nfl json data, we're mid game
			if raw:
				# Replace empty csv values with "None"
				# Here we have to use a positive lookahead assertion "(?=,)"
				# which means that we match any two commas together ",," and
				# replace it with ",None,"
				m = re.compile(",(?=,)")
				formatted = m.sub(",None", raw)
				
				# A well formatted JSON string can be eval'd into a python dictionary
				data = eval(formatted)
				
				# Find this match's live data
				for x in data['ss']:
					# If this game is currently running
					if x[2] != 'Pregame':
						# We found our game
						if x[4] == match.road:
							# Add our predicted line to the home team score and compare
							hscore = int(x[7]) + match.line
							rscore = int(x[5])

							print "%s %s | %s %s" % (x[6], x[7], x[4], x[5])
							# Figure out which team to bet based off the prediction and line
							if (distance(prediction, match.line) <= 1):
								# Skip bets that are too close
								print "No Bet, too close"
							# Home team is favoed
							elif (abs(prediction) > abs(match.line) and (prediction < 0)):
								# Is the home team beating the vegas spread?
								if ((hscore - rscore) > 0) and (match.line < 0):
									# Bet the home team
									print "Bet", match.home, "and winning"
								else:
									print "Bet", match.home, "and losing"
							# Road team is favored
							else:
								# Is the home team beating the vegas spread?
								if ((rscore - hscore) > 0) and (match.line < 0):
									# Bet the home team
									print "Bet", match.road, "and winning"
								else:
									print "Bet", match.road, "and losing"

							# Home score is positive and I predicted home
							# we're winning, if not, we're losing
							#if ((hscore - rscore) > 0) and (match.line < 0):
							#	print "Winning spread\n"
							#else:
							#	print "Losing spread\n"
			
			continue

		# If we have the scores, calculate the results
		diff = match.rscore - match.hscore
		spreaddiff = diff - prediction
		d = distance(prediction, diff)
		if (match.hscore + match.line) > match.rscore :
			winloss.win += 1
		else:
			winloss.loss += 1
		
		# Figure out whether to bet or not
		print prediction, match.line
		print distance(prediction, match.line)
		if (distance(prediction, match.line) <= 1):
			bet = "no bet, too close"
		else:
			bet = "bet"

		# Print match info
		print "%s:%d vs %s:%d" % (match.home, match.hscore, match.road, match.rscore)
		print " > pre-game:  home: %d road: %d" % (tally[match.home].rate, tally[match.road].rate)
		print " > predicted %d, spread %d, actual %d, delta %d" % (prediction, match.line, diff, d)
		print " > %s" % (bet)
		if week > 1:
			delta.append(d)

		# Take scores for current week and adjust ELO
		# We add 100 ELO for every 7 point difference
		# each team gets or loses half the total ELO points
		hrate = tally[match.home].rate - (spreaddiff * 100/7)/2
		rrate = tally[match.road].rate + (spreaddiff * 100/7)/2
		tally[match.home].rate = (tally[match.home].rate * week + hrate) / (week + 1)
		tally[match.road].rate = (tally[match.road].rate * week + rrate) / (week + 1)
		print " > post-game: home: %d road: %d" % (tally[match.home].rate, tally[match.road].rate)

print "------"
print "Accuracy: %f Std Dev: %f" % (average(delta), std(delta))
