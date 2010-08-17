#!/usr/bin/python
import csv

boxes = csv.reader(open('2009.csv', 'r'), delimiter=',')
spreads = csv.reader(open('2009_spreads.csv', 'r'), delimiter=',')
out = csv.writer(open('withspreads.csv', 'w'), delimiter=',', quoting=csv.QUOTE_NONE)
x = {}

# Import Aaron's spreads into a dictionary of lists
for teams in spreads:
	x[teams[0]] = teams[1:]

for game in boxes:
	if game[0].isdigit():
		week = int(game[0])
		team = game[5]
		if week != 1 and week < 17:
			game.append(x[team][week-2])
			#game = game, x[team][week-1]
		else:
			game.append('')
	out.writerow(game)
