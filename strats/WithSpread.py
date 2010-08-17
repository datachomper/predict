#!/usr/bin/python
from sim import Strategy
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
