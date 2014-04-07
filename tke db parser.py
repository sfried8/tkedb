import csv
import sqlite3

conn = sqlite3.connect("development.db")
c=conn.cursor()
with open('tkedb.csv','rU') as csvfile:
	spamreader = csv.reader(csvfile)
	i=0
	for row in spamreader:
		i+=1
		if row[0] == "":
			row[0] = -1
		if row[1] == "":
			row[1] = -1
		if row[7] == "":
			row[7] = -1
		params = (i,row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7])
		command = "INSERT INTO brothers_brother VALUES (?,?,?,?,?,?,?,?,?);"
		c.execute(command,params)
	conn.commit()
	conn.close()


