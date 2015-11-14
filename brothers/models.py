from django.db import models

class Brother(models.Model):
	scroll = models.IntegerField()
	pc = models.IntegerField()
	fname = models.CharField(max_length=50)
	lname = models.CharField(max_length=50)
	name = models.CharField(max_length=50)
	nickname = models.CharField(max_length=50)
	big = models.CharField(max_length=50)
	bigS = models.IntegerField(max_length=50)
	curPos = models.CharField(max_length=3)
	active = models.BooleanField(default=False)
	wasPry = models.BooleanField(default=False)
	wasEpi = models.BooleanField(default=False)
	wasGra = models.BooleanField(default=False)
	wasHyp = models.BooleanField(default=False)
	wasCry = models.BooleanField(default=False)
	wasHeg = models.BooleanField(default=False)
	wasHis = models.BooleanField(default=False)


	def __str__(self):
		return str(self.scroll)+": "+str(self.pc)+self.name