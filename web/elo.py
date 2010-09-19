#!/usr/bin/python

from django.core.management import setup_environ
import settings
setup_environ(settings)
from data.models import Box
from numpy import std, average

tally = {}
delta = []

def distance(x, y):
	if (x < 0) and (y > 0):
		return y + abs(x)
	if (y < 0) and (x > 0):
		return x + abs(y)
	return abs(x - y)

class Stat():
	def __unicode__(self):
		return self.rate

	def __init__(self):
		self.win = 0
		self.loss = 0
		self.rate = 1500

for week in range(1,19):
	matches = Box.objects.filter(week=week)
	print "Week:", week
	for match in matches:
		# Create a stat object for teams
		if not match.home in tally:
			tally[match.home] = Stat()
		if not match.road in tally:
			tally[match.road] = Stat()

		# Print match info
		print "%s:%d vs %s:%d" % (match.home, match.hscore, match.road, match.rscore)

		# The Casino's are much smarter than I am so we pre-seed our ratings
		# by reverse engineering their spread predictions
		if week == 1:
			tally[match.home].rate = 1500 - int((match.line * 100/7)/2)
			tally[match.road].rate = 1500 + int((match.line * 100/7)/2)

		# Find accuracy of curent ELO
		prediction = (tally[match.road].rate - tally[match.home].rate)*7/100
		diff = match.rscore - match.hscore
		d = distance(prediction, diff)

		print " > pre-game:  home: %d road: %d" % (tally[match.home].rate, tally[match.road].rate)
		print " > predicted %d, spread %d, actual %d, delta %d" % (prediction, match.line, diff, d)
		if week > 1:
			delta.append(d)

		# Take scores for current week and adjust ELO
		# We add 100 ELO for every 7 point difference
		# each team gets or loses half the total ELO points
		hrate = tally[match.home].rate - (diff * 100/7)/2
		rrate = tally[match.road].rate + (diff * 100/7)/2
		tally[match.home].rate = (tally[match.home].rate * week + hrate) / (week + 1)
		tally[match.road].rate = (tally[match.road].rate * week + rrate) / (week + 1)
		print " > post-game: home: %d road: %d" % (tally[match.home].rate, tally[match.road].rate)

print "------"
print delta
print "Accuracy: %d Std Dev: %d" % (average(delta), std(delta))
