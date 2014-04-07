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

	def __str__(self):
		return str(self.scroll)+": "+self.name