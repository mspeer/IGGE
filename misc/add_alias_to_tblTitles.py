<BU>import os, glob, re, shutil, hashlib, csv
import MySQLdb as mdb
from numpy import genfromtxt

con = mdb.connect('localhost','root','_PW_','iggeqadb')
cursor = con.cursor()
n = 0
with open('gsws_<BU>_scrub.csv', 'rb') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',')
	for row in spamreader:
		n = n + 1
		titleID = row[0]
		gameID = row[1]
		name = row[2]
		alias = row[3]
		benchmarkID = row[4]
		platform_desc = row[5]
		ssfilename = row[6]
		vis_verified = row[7]
		dimension = row[8]
		comment = row[9]
		english = row[10]
		if len(alias) > 0:
			gsws_goal = True
		else:
			gsws_goal = False
		sql = "UPDATE tbltitles SET alias=%s, gsws_goal=%s WHERE name=%s"
		args = (alias,gsws_goal, name)
		print (sql, args)
		cursor.execute(sql, args)
		con.commit()
print "n: ", n
