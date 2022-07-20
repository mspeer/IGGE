import os, glob, re, shutil, hashlib, csv
import MySQLdb as mdb
from numpy import genfromtxt

con = mdb.connect('localhost','root','_PW_','iggeqadb')
cursor = con.cursor()

outputfile = 'D:\\Projects\\IGGE\\python_scripts\\rrp_but_no_data.txt'
outfile = open( outputfile, 'a')

outstring = "taskid" + '|' + "taskname" + '|' +  "bucketid" + '|' +  "bucketname" + '|' +  "deviceid" + '|' +  "recommendedrootpath" + '|' +  "count" + '\n'
outfile.write(outstring)


with open('gsws_view_all.csv', 'rb') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',')
	for row in spamreader:
		taskid = row[0]
		taskguid = row[1]
		taskname = row[2]
		bucketid = row[3]
		bucketname = row[4]
		deviceid = row[5]
		graphicsbrand = row[6]
		recommendedrootpath = row[7]
		finisheddate = row[8]
		releasedate = row[9]
		
#		print taskid, taskname, bucketid, bucketname, deviceid, recommendedrootpath
		n = 0
		if os.path.exists(recommendedrootpath):
			fileList=os.listdir( recommendedrootpath)
			fileList.sort()
			if len(fileList) > 0:
				for file in fileList:
					try:
						if os.path.isfile(recommendedrootpath + file) and file != 'Thumbs.db':
							n = n + 1
					except:
						print "ERROR", taskid,taskguid,taskname,bucketid,bucketname,recommendedrootpath
			outstring = taskid + '|' + taskname + '|' +  bucketid + '|' +  bucketname + '|' +  deviceid + '|' +  recommendedrootpath + '|' +  str(n) + '\n'
		else:
			outstring = taskid + '|' + taskname + '|' +  bucketid + '|' +  bucketname + '|' +  deviceid + '|' +  recommendedrootpath + '|' +  'Path does not exist\n'
		print outstring
		outfile.write(outstring)
							
