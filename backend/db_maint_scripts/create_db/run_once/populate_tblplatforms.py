import os, glob, re, shutil, hashlib, csv
import MySQLdb as mdb
from db_funcs import getssdbcon
from numpy import genfromtxt

con = getssdbcon()
cursor = con.cursor()


with open('platform_to_bucket_map.csv', 'rb') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',')
	for row in spamreader:
		description = row[0]
		bucketid = row[1]
		bucketname = row[2]
		print description, bucketid, bucketname
		sql = "INSERT into tblplatforms(description,bucketid,bucketname) VALUES(%s,%s,%s)"
		args = (description,bucketid,bucketname)
		cursor.execute(sql, args)
		con.commit()
print 'Execution complete'
print 'Hit return to exit'
raw_input()
