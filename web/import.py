#!/usr/bin/python

from django.core.management import setup_environ
import settings
setup_environ(settings)
from data.models import Box
import csv

boxes = csv.reader(open('../boxes2010.csv', 'r'), delimiter=',')

for game in boxes:
	# Ignore comments
	if not game[0].isdigit():
		continue

	# Check to see if this game exists or not
	try:
		b = Box.objects.get(week=game[0],home=game[1],road=game[2])
	except:
		b = Box()

	b.year = 2010
	b.week = int(game[0])
	b.home = game[1]
	b.road = game[2]
	# Any of the following fields are optional
	try:
		b.line = game[3]
		b.hscore = int(game[4])
		b.rscore = int(game[5])
	except IndexError:
		pass
	b.save()
