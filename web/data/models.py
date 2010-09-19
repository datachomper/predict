from django.db import models

class Box(models.Model):
	def __unicode__(self):
		return self.home+"vs"+self.road
	
	home = models.CharField(max_length=4)
	road = models.CharField(max_length=4)
	line = models.DecimalField(max_digits=3, decimal_places=1)
	week = models.IntegerField()
	year = models.IntegerField()
	hscore = models.IntegerField(null=True, blank=True)
	rscore = models.IntegerField(null=True, blank=True)
