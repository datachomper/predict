#!/usr/bin/python
class Season:
	"""Stores the season's box data for processing by strategies"""

	def __init__(self, data):
		# Grep the csv data, this may need to
		# be abstracted if we use a DB later
		self.numweeks = 0
		for line in data:
			if not line[0].isdigit():
				continue
			if int(line[0]) > self.numweeks:
				self.numweeks = int(line[0])
		self.week = [None] * self.numweeks

		for line in data:
			# Ignore comments
			if not line[0].isdigit():
				continue
			game = Game()
			game.week = int(line[0])
			game.winner = line[5]
			game.loser = line[7]
			if line[6] == '@':
				game.home = line[7]
				game.visitor = line[5]
			else:
				game.home = line[5]
				game.visitor = line[7]
			game.ptsw = int(line[8])
			game.ptsl = int(line[9])
			if line[14] == '':
				game.spread = None
			else:
				game.spread = float(line[14])

			self.week[game.week] = [None] * 3

	def __iter__(self):
		return self
# season.week[1].game[1]

class Game:
	pass

class Simulator:
	"""Runs each prediction strategy, displays results"""
	def __init__(self, file):
		import csv
		self.strategies = []
		self.weeks = 16
		# Import csv season data and strip comments
		self.data = Season(csv.reader(open(file, 'r'), delimiter=','))

	def register(self, strategy):
		self.strategies.append(strategy)
		strategy.load(self.data)

	def weekly_totals(self):
		# Find "names" column width
		col1 = 0
		for strat in self.strategies:
			if len(strat.name) > col1:
				col1 = len(strat.name)
		col1 += 1

		# Print title bar
		title = "".ljust(col1)
		for x in range(1,self.weeks+1):
			title += "%6s|" % x
		title += " Total"
		print title

		# Print each strategy's weekly results
		for strategy in self.strategies:
			result = strategy.name.ljust(col1)
			for x in strategy.result.week:
				result += "%6s|" % x
			result += "%6s" % strategy.result.total
			print result

class Strategy:
	"""Scaffolding class for prediction strategies"""
	def __init__(self):
		self.name = ""
		self.data = None

	def load(self, data):
		self.data = data
	
	def run(self):
		pass

	class result:
		def __init__(self):
			self.week = []
			self.total = 0

class WithSpread(Strategy):
	"""Bet with the spread for every game"""
	def __init__(self):
		self.name = "With Spread"
		self.result.week = [0,100,200,1000,4000,1000,-200,-56,1000,1000,10,555,13,140,15,1600]
		self.result.total = sum(self.result.week)

	def run(self):
		for week in self.data.weeks:
			for game in week:
				print "%s vs %s" % (game.home, game.visitor)

# Bootstrap
sim = Simulator('2009.csv')
a = WithSpread()
sim.register(a)
sim.weekly_totals()
