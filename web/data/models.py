from django.db import models

class Box(models.Model):
	def __unicode__(self):
		return "%d.%d %s vs %s" % (self.year, self.week, self.home, self.road)
	
	NFL_TEAMS = (
		(u'Arizona', u'Arizona'),
		(u'Atlanta', u'Atlanta'),
		(u'Baltimore', u'Baltimore'),
		(u'Buffalo', u'Buffalo'),
		(u'Carolina', u'Carolina'),
		(u'Chicago', u'Chicago'),
		(u'Cincinnati', u'Cincinnati'),
		(u'Cleveland', u'Cleveland'),
		(u'Dallas', u'Dallas'),
		(u'Denver', u'Denver'),
		(u'Detroit', u'Detroit'),
		(u'Green Bay', u'Green Bay'),
		(u'Houston', u'Houston'),
		(u'Indianapolis', u'Indianapolis'),
		(u'Jacksonville', u'Jacksonville'),
		(u'Kansas City', u'Kansas City'),
		(u'Miami', u'Miami'),
		(u'Minnesota', u'Minnesota'),
		(u'N.Y. Giants', u'N.Y. Giants'),
		(u'N.Y. Jets', u'N.Y. Jets'),
		(u'New England', u'New England'),
		(u'New Orleans', u'New Orleans'),
		(u'Oakland', u'Oakland'),
		(u'Philadelphia', u'Philadelphia'),
		(u'Pittsburgh', u'Pittsburgh'),
		(u'San Diego', u'San Diego'),
		(u'San Francisco', u'San Francisco'),
		(u'Seattle', u'Seattle'),
		(u'St. Louis', u'St. Louis'),
		(u'Tampa Bay', u'Tampa Bay'),
		(u'Tennessee', u'Tennessee'),
		(u'Washington', u'Washington'),
	)

	home = models.CharField(max_length=4, choices=NFL_TEAMS)
	road = models.CharField(max_length=4, choices=NFL_TEAMS)
	line = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
	week = models.IntegerField()
	year = models.IntegerField()
	hscore = models.IntegerField(null=True, blank=True)
	rscore = models.IntegerField(null=True, blank=True)
