import os, glob, re, shutil, hashlib, csv
import MySQLdb as mdb
from db_funcs import getssdbcon
from numpy import genfromtxt

con = getssdbcon()
cursor = con.cursor()


with open('common_to gsws_name_mapping_with_rank.csv', 'rb') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',')
	for row in spamreader:
		rank = row[0]
		alias = row[1]
		gswsname = row[2]
		print alias
		sql = "UPDATE tbltitles SET rank=%s WHERE alias=%s"
		args = (rank,gswsname)
		cursor.execute(sql, args)
		con.commit()
print 'Execution complete'
print 'Hit return to exit'
raw_input()
