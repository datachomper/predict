#!/usr/bin/python

class Simulator:
	def __init__(self):
		self.strategies = []
		self.weeks = 16

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
	class result:
		pass
	pass

sim = Simulator()
a = Strategy()
sim.register(a)
a.name = "with spread"
a.result.week = [0,100,200,1000,4000,1000,-200,-56,1000,1000,10,555,13,140,15,1600]
a.result.total = sum(a.result.week)

sim.weekly_totals()

