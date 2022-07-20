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
		sql = "SELECT ssID FROM tblscreenshots WHERE benchmarkID=%s AND ssFilename=%s"
		args = (benchmarkID, ssfilename)
		cursor.execute(sql, args)
		if cursor.rowcount == 0:
			print  "No screen shot ID was found", benchmarkID, ssfilename
		elif cursor.rowcount > 1:
			print "More than one screen shot ID was found", benchmarkID, ssfilename
		else:
			for (ssID) in cursor:
				ssID = int(ssID[0])
			if english=="No":
				language = "Other"
			else:
				language = "English"
			if vis_verified=="y":
				vis_verified=True
			else:
				vis_verified=False
			sql = "UPDATE tblscreenshots SET vis_verified=%s, comment=%s, dimensions=%s, language=%s WHERE ssid=%s"
			args = (vis_verified,comment,dimension,language,ssID)
			print (sql, args)
			cursor.execute(sql, args)
			con.commit()

print "n: ", n

	


		
		

