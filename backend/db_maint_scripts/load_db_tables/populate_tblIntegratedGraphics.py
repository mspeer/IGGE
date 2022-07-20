import os, glob, re, shutil, hashlib, csv
import MySQLdb as mdb
from numpy import genfromtxt

con = mdb.connect('localhost','root','_PW_','iggeqadb')
cursor = con.cursor()


with open('gsws_integratedgraphicsid.csv', 'rb') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',')
	for row in spamreader:
		igid = row[0]
		graphicsname = row[1]
		graphicsbrandnr = row[2]
		deviceid = row[3]
		bucketid = row[4]
		print graphicsname, graphicsbrandnr, deviceid
		sql = "INSERT into tblintegratedgraphics(graphicsname,graphicsbrandnr,deviceid,bucketid) VALUES(%s,%s,%s,%s)"
		args = (graphicsname, graphicsbrandnr, deviceid, bucketid)
		cursor.execute(sql, args)
		con.commit()

