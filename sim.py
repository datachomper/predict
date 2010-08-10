#!/usr/bin/python
class Boxes:
	'''Stores the season's box data'''
	def __init__(self):
		self.week = None

class Simulator:
	'''Runs each prediction strategy, displays results'''
	def __init__(self, file):
		import csv
		self.strategies = []
		self.weeks = 16
		# Import csv season data and strip comments
		self.data = csv.reader(open(file, 'r'), delimiter=',')

	def register(self, strategy):
		self.strategies.append(strategy)

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
	'''Scaffolding class for prediction strategies'''
	def __init__(self):
		self.name = ""

	class result:
		def __init__(self):
			self.week = []
			self.total = 0

class WithSpread(Strategy):
	'''Bet with the spread for every game'''
	def __init__(self):
		self.name = "With Spread"
		self.result.week = [0,100,200,1000,4000,1000,-200,-56,1000,1000,10,555,13,140,15,1600]
		self.result.total = sum(self.result.week)

# Bootstrap
sim = Simulator('2009.csv')
a = WithSpread()
sim.register(a)
sim.weekly_totals()
