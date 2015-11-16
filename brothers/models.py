from django.db import models

class Brother(models.Model):
	scroll = models.IntegerField()
	pc = models.IntegerField()
	fname = models.CharField(max_length=50)
	lname = models.CharField(max_length=50)
	name = models.CharField(max_length=50)
	nickname = models.CharField(max_length=50)
	big = models.CharField(max_length=50)
	bigS = models.IntegerField()
	active = models.BooleanField(default=False)
	wasPry = models.BooleanField(default=False)
	wasEpi = models.BooleanField(default=False)
	wasGra = models.BooleanField(default=False)
	wasHyp = models.BooleanField(default=False)
	wasCry = models.BooleanField(default=False)
	wasHeg = models.BooleanField(default=False)
	wasHis = models.BooleanField(default=False)


	def __str__(self):
		return str(self.scroll)+") "+self.name+" PC "+str(self.pc)

class Officer(models.Model):
	title = models.CharField(max_length=20)
	jewel_image = models.CharField(max_length=20)
	current = models.ForeignKey('Brother')
	def __str__(self):
		return self.title + " - "+self.current.name
