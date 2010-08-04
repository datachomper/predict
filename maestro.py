#!/usr/bin/python
import csv
from numpy import *

print " Year\t home/road wins"
avg = 0.0
v = empty(11)
for year in range(1999,2010):
	scores = csv.reader(open("{0}.csv".format(year), 'r'), delimiter=',')
	home = 0.0;
	season = 0.0;
	for x in scores:
		if x[6] != '@':
			home += 1
		if x[0].isdigit():
			season += 1
	
	print "",year, "\t %3.2f" % ((home/season)*100), '%'
	avg += ((home/season)*100)
	v[year-1999] = ((home/season)*100)
print " Avg: %3.2f" % v.mean()
print " Std Dev: %3.2f" % v.std()
