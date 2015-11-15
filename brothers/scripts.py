from models import Brother
import io

def test2():
	f = io.open("dataouttodb2.txt",'r',-1,'utf-8')
	for line in f.readlines():
		fields = line.split("%")
		print fields
		b = Brother()
		b.scroll = int(fields[0])
		b.pc = int(fields[1])
		b.fname = fields[2]
		b.lname = fields[3]
		b.name = fields[4]
		b.nickname = fields[5]
		b.big = fields[6]
		b.bigS = int(fields[7])
		b.save()
		print b

def test():
	f = io.open("dataouttodb2.txt", 'w',-1,'utf-8')
	for b in Brother.objects.all():
		line = []
		line.append(b.scroll)
		line.append(b.pc)
		line.append(b.fname)
		line.append(b.lname)
		line.append(b.name)
		line.append(b.nickname)
		line.append(b.big)
		line.append(b.bigS)
		lineStr = u"%".join([unicode(x) for x in line])+"\n"
		f.write(lineStr)

	f.close()


test2()