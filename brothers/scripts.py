from models import Brother

def test2():
	bros = Brother.objects.all()
	for b in bros:
		if b.fname == "Tom":
			print (b.name)
			b.fname = "Thomas"
			b.name = b.name.replace("Tom","Thomas")
			b.save()
	print("hello")

test2()