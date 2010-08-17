#!/usr/bin/python
from sim import Strategy
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

