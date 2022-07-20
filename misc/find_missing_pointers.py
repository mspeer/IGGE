import pyodbc, base64
from io import BytesIO
from PIL import Image
import os, glob, re, shutil, hashlib
import MySQLdb as mdb

cnxn = pyodbc.connect('DSN=DashBoard')
cursorx = cnxn.cursor()
con = mdb.connect('localhost','root','_PW_','iggeqadb')
cursor = con.cursor()
n = 0
#path = "D:\Projects\IGGE\python_scripts\media"
#filename = "output.jpg"



#sql = "select tblTitles.titleID AS 'titleID', tblTitles.gameID AS 'gameID', tblTitles.name AS 'name', tblBenchmarks.benchmarkID AS 'benchmarkID', \
#	tblPlatforms.description AS 'platform_description', tblScreenshots.ssFilename AS 'ssFilename' \
#	FROM tblbenchmarks \
#		JOIN tblTitles ON tblbenchmarks.gameID = tblTitles.gameID \
#       JOIN tblPlatforms ON tblbenchmarks.platformID = tblPlatforms.platformID \
#       JOIN tblScreenshots ON tblbenchmarks.benchmarkID = tblScreenshots.benchmarkID"
sql = 'SELECT gameID AS gameID, titleID AS titleID FROM tblbenchmarks WHERE have_config=TRUE OR have_screenshots=TRUE'
cursor.execute(sql)
if cursor.rowcount == 0:
	print "No Records found"
else:
	for data in cursor:
		n = n + 1
		taskID = data[0]
#		print taskID
		sqlx = 'SELECT RecommendedRootPath AS recommendedrootpath FROM GswsResults WHERE TaskID=?'
		parmsx = (taskID)
		cursorx.execute(sqlx,parmsx)
		if cursorx.rowcount == 0:
				print "No RecommendedRootPath found", taskID
		else:
			for rrp in cursorx:
				rrp = rrp[0]
				print rrp

		

print "benchmarks processed:",n		
		
#cursor.execute("select distinct(RecommendedRootPath) AS recommendedpath FROM GswsResults ORDER BY recommendedpath DESC;")
#data = cursor.fetchall()
#for row in data:
#	print row
	




