from models import Brother

def test2():
	f = open("dataouttodb.txt",'U')
	for line in f.readlines():
		fields = line.split("%")
		b = Brother()
		b.scroll = int(fields[1])
		b.pc = int(fields[2])
		b.fname = fields[3]
		b.lname = fields[4]
		b.name = fields[5]
		b.nickname = fields[6]
		b.big = fields[7]
		b.bigS = int(fields[8])
		b.curPos = ""
		b.save()

test2()