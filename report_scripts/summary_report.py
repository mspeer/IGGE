import os, glob, re, shutil, hashlib
import MySQLdb as mdb
import pyodbc, base64
from io import BytesIO
from PIL import Image
import unicodedata
import datetime

con = mdb.connect('localhost','root','_pw_','iggeqadb')
cursor = con.cursor()
conx = pyodbc.connect('DSN=DashBoard')
cursorx = conx.cursor()

outputfile = 'D:\\Projects\\IGGE\\logfiles\\summary_report.txt'
outfile = open( outputfile, 'a')

outstring = "gameID|taskname|releasedate|BDW H-Series 4 + 3e|BDW U-Series 2+2|BDW U-Series 2+3|BDW Y-Series 2+2|HSW H-Series 4+3e|HSW U-Series 2+2|HSW U-Series 2+3|HSW Y-Series 2+2 \n"
outfile.write(outstring)

sql = "SELECT DISTINCT(gameID) FROM tblbenchmarks ORDER BY gameID ASC"
cursor.execute(sql)
if cursor.rowcount == 0:
	print "No gameID's found"
else:
	for gameID in cursor:
			game = gameID[0]
			sql = "SELECT benchmarkID, platformID, releasedate, num_screenshots, num_configs, taskname FROM tblbenchmarks WHERE gameID=%s"
			args = (gameID)
			cursor.execute(sql,[args])
			if cursor.rowcount == 0:
				print "No benchmarks found"
			else:
				css1 = css2 = css3 = css4 = css5 = css6 = css7 = css8 = '0'
				cconfig1 = cconfig2 = cconfig3 = cconfig4 = cconfig5 = cconfig6 = cconfig7 = cconfig8 = '0'
				for data in cursor:
					benchmarkID = str(data[0])
					platformID = data[1]
					releasedate = str(data[2])
					num_screenshots = str(data[3])
					num_configs = str(data[4])
					taskname = str(data[5])
					if platformID == 1:
						css1 = num_screenshots
						cconfig1 = num_configs
					elif platformID == 2:
						css2 = num_screenshots
						cconfig2 = num_configs
					elif platformID == 3:
						css3 = num_screenshots
						cconfig3 = num_configs
					elif platformID == 4:
						css4 = num_screenshots
						cconfig4 = num_configs
					elif platformID == 5:
						css5 = num_screenshots
						cconfig5 = num_configs
					elif platformID == 6:
						css6 = num_screenshots
						cconfig6 = num_configs
					elif platformID == 7:
						css7 = num_screenshots
						cconfig7 = num_configs
					elif platformID == 8:
						css8 = num_screenshots
						cconfig8 = num_configs
					else:
						print "platformID not in 1-8"

#				outstring = game + '|' + taskname + '|' +  bucketid + '|' +  bucketname + '|' +  deviceid + '|' +  recommendedrootpath + '|' +  str(n) + '\n'						
				outstring = game + '|' + taskname + '|' + releasedate + '|' + css1 + '|' + css2 + '|' + css3 + '|' + css4 + '|' + css5 + '|' + css6 + '|' + css7 + '|' + css8 + '\n'
				outfile.write(outstring)
				
#					print gameID[0], benchmarkID, platformID, releasedate, num_screenshots, num_configs
#sql = "SELECT benchmarkID, gameID, platformID, releasedate, num_screenshots, num_configs FROM tblbenchmarks"
#cursor.execute(sql)
#if cursor.rowcount == 0:
#	print "No benchmarks found"
#else:
#	for data in cursor:
#		benchmarkID = data[0]
#		gameID = data[1]
#		platformID = data[2]
#		releasedate = data[3]
#		num_screenshots = data[4]
#		num_configs = data[5]
#		print benchmarkID, gameID, platformID, releasedate, num_screenshots, num_configs
		
