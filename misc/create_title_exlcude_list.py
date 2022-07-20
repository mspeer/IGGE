import os, glob, re, shutil, hashlib
import MySQLdb as mdb

con = mdb.connect('localhost','root','_PW_','iggeqadb')
cursor = con.cursor()


excludefile = 'D:\\Projects\\IGGE\\python_scripts\\excludefile.txt'
excludes = open( excludefile, 'a')

sql = "SELECT name FROM tbltitles"
cursor.execute(sql)
for (title) in cursor:
#	print title
	excludes.write(title[0] + '\n')

