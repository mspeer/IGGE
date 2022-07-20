import os, glob, re, shutil, hashlib
import MySQLdb as mdb

con = mdb.connect('localhost','root','_PW_','iggeqadb')
cursor = con.cursor()

logfile = 'D:\\Projects\\IGGE\\logfiles\\logfile.txt'
log = open( logfile, 'a')


sql = "select tblTitles.titleID AS 'titleID', tblTitles.gameID AS 'gameID', tblTitles.name AS 'name', tblBenchmarks.benchmarkID AS 'benchmarkID', \
	tblPlatforms.description AS 'platform_description', tblScreenshots.ssFilename AS 'ssFilename' \
	FROM tblbenchmarks \
		JOIN tblTitles ON tblbenchmarks.gameID = tblTitles.gameID \
        JOIN tblPlatforms ON tblbenchmarks.platformID = tblPlatforms.platformID \
        JOIN tblScreenshots ON tblbenchmarks.benchmarkID = tblScreenshots.benchmarkID"
cursor.execute(sql)
if cursor.rowcount == 0:
	print "No Records found"
else:
	for (titleID,gameID,name,benchmarkID,platform_description,ssFilename) in cursor:
		print titleID,gameID,name,benchmarkID,platform_description,ssFilename






