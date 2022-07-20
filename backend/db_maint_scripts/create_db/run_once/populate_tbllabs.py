import os, glob, re, shutil, hashlib, csv
import MySQLdb as mdb
from db_funcs import getssdbcon
from numpy import genfromtxt

con = getssdbcon()
cur = con.cursor()
with open('labs.csv', 'rb') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',')
	for row in spamreader:
		labId = row[0]
		labName = row[1]
		vcFileShare = row[2]
		localFileShare = row[3]
		print labId,labName,vcFileShare,localFileShare
		sql = "INSERT into tbllabs(labID,labName,vcFileShare,localFileShare) VALUES(%s,%s,%s,%s)"
		args = (labId,labName,vcFileShare,localFileShare)
		cur.execute(sql, args)
		con.commit()
print 'Execution complete'
print 'Hit return to exit'
raw_input()

