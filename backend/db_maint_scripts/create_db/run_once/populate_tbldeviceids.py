import os, glob, re, shutil, hashlib, csv
import MySQLdb as mdb
from db_funcs import getssdbcon
from numpy import genfromtxt

con = getssdbcon()
cursor = con.cursor()


with open('deviceid_to_graphics_brand.csv', 'rb') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',')
	for row in spamreader:
		deviceid = row[0]
		graphicsbrand = row[1]
		print deviceid, graphicsbrand
		sql = "INSERT into tblDeviceIds(deviceid, graphicsbrand) VALUES(%s,%s)"
		args = (deviceid, graphicsbrand)
		cursor.execute(sql, args)
		con.commit()
print 'Execution complete'
print 'Hit return to exit'
raw_input()
