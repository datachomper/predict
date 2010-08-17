#!/usr/bin/python
# A basic algorithm to bet /with/ the spread

import csv
boxes = csv.reader(open('2009.csv', 'r'), delimiter=',')

# Define a generic "game" class for storing game information
class Game:
	def __init__(self, week):
		self.week = int(week[0])
		self.home = week[5]
		self.winner = week[5]
		self.visitor = week[7]
		self.loser = week[7]
		self.ptsw = int(week[8])
		self.ptsl = int(week[9])
		if (week[14] == ''):
			self.spread = None
		else:
			self.spread = float(week[14])

		# Computed data
		i+1f self.spread != None:
			self.ptdiff = abs(self.ptsw - self.ptsl)
			self.push = False
			if self.spread > 0:
				self.beatspread = False
			elif abs(self.spread) == self.ptdiff:
				self.beatspread = False
				self.push = True
			elif self.ptdiff > abs(self.spread):
				self.beatspread = True
			else:
				self.beatspread = False

bank = 0

for week in boxes:
	# Ignore comments in csv file
	if not week[0].isdigit():
		continue

	g = Game(week)

	# Ignore games without spead data
	if g.spread == None:
		continue

	if g.push:
		bank += 0
		g.beatspread = "Push"
	elif g.beatspread:
		# Yay we won! :O)
		bank += 100
	else:
		# Aw, we lost :O(
		bank -= 110

	# Bet 110 with the spread
	print "Week %d: %s %d vs %s %d | %s | %s | $%s" % (
			g.week, g.winner, g.ptsw, g.loser, g.ptsl, g.spread, g.beatspread, bank)
