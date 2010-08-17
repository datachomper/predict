#!/usr/bin/python
class Season:
	"""Stores the season's box data for processing by strategies"""

	def __init__(self, data):
		# Grep the csv data, this may need to
		# be abstracted if we use a DB later
		self.numweeks = 0
		self.week = {}

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

			try:
				self.week[game.week].append(game)
			except KeyError:
				self.week[game.week] = []
				self.week[game.week].append(game)

	def __iter__(self):
		return self

class Game:
	pass

class Simulator:
	"""Runs each prediction strategy, displays results"""
	def __init__(self, file):
		import csv
		self.strategies = []
		self.weeks = 17
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
		for x in range(1, self.weeks+1):
			title += "%6s|" % x
		title += " Total"
		print title

		# Print each strategy's weekly results
		for strategy in self.strategies:
			strategy.run()
			result = strategy.name.ljust(col1)
			for k,x in strategy.result.week.items():
				result += "%6s|" % x
			result += "%7s" % strategy.result.total
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

	def run(self):
		self.result.week = {}
		self.result.total = 0
		for week,games in self.data.week.items():
			weeklypurse = 0
			for game in games:
				# Ignore games without spread data
				if game.spread == None:
					continue

				ptdiff = abs(game.ptsw - game.ptsl)
				if game.spread > 0:
					# Favored team didn't beat spread
					weeklypurse -= 110
				elif abs(game.spread) == ptdiff:
					# A push returns your money
					weeklypurse += 0
				elif ptdiff > abs(game.spread):
					# Favored team beat spread
					weeklypurse += 100
				else:
					weeklypurse -= 110

			self.result.week[week] = weeklypurse
			self.result.total += weeklypurse

class AgainstSpread(Strategy):
	"""Bet against the spread for every game"""
	def __init__(self):
		self.name = "Against Spread"

	def run(self):
		self.result.week = {}
		self.result.total = 0
		for week,games in self.data.week.items():
			weeklypurse = 0
			for game in games:
				# Ignore games without spread data
				if game.spread == None:
					continue

				ptdiff = abs(game.ptsw - game.ptsl)
				if game.spread > 0:
					# Favored team didn't beat spread
					weeklypurse += 100
				elif abs(game.spread) == ptdiff:
					# A push returns your money
					weeklypurse += 0
				elif ptdiff > abs(game.spread):
					# Favored team beat spread
					weeklypurse -= 110
				else:
					weeklypurse += 100

			self.result.week[week] = weeklypurse
			self.result.total += weeklypurse

class AllWon(Strategy):
	"""Pretend we won every bet to show baseline"""
	def run(self):
		self.name = "All Won"
		self.result.week = {}
		self.result.total = 0
		for week,games in self.data.week.items():
			weeklypurse = 0
			for game in games:
				if game.spread == None:
					continue
				weeklypurse += 100

			self.result.week[week] = weeklypurse
			self.result.total += weeklypurse

class AllLost(Strategy):
	"""Pretend we lost every bet to show baseline"""
	def run(self):
		self.name = "All Lost"
		self.result.week = {}
		self.result.total = 0
		for week,games in self.data.week.items():
			weeklypurse = 0
			for game in games:
				if game.spread == None:
					continue
				weeklypurse -= 110

			self.result.week[week] = weeklypurse
			self.result.total += weeklypurse

# Bootstrap the simulator
sim = Simulator('2009.csv')

sim.register(WithSpread())
sim.register(AgainstSpread())
sim.register(AllWon())
sim.register(AllLost())

sim.weekly_totals()
