#!/usr/bin/python
from sim import Strategy
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

