<BU>import os, sys, glob, re, shutil, hashlib
import MySQLdb as mdb
import pyodbc, base64
from io import BytesIO
from PIL import Image
import unicodedata
import datetime

con = mdb.connect('localhost','root','_PW_','iggeqadb')
cursor = con.cursor()
conx = pyodbc.connect('DSN=DashBoard')
cursorx = conx.cursor()

#local<BU>path = 'D:\\Projects\\IGGE\\<BU>localrepo'
#logfile = 'D:\\Projects\\IGGE\\logfiles\\logfile.txt'
#log = open( logfile, 'a')
platform_bucketed = ''

def md5Checksum(filePath):
	with open(filePath, 'rb') as fh:
		m = hashlib.md5()
		while True:
			data = fh.read(8192)
			if not data:
				break
	m.update(data)
	return m.hexdigest()

def logit(logfile,caller,statement):
	log = open( logfile, 'a' )
	dtstamp = str(datetime.datetime.now())
	log.write(dtstamp + "|" + caller + "|" + statement + '\n')
	log.close
	print "\t\t\t\t\t" + caller + "\t" + statement
		
def get_active_labs(logfile):
	print "    get_active_labs"
	sql = "SELECT labID, labName,vcFileShare FROM tblLabs WHERE active=True"
	cursor.execute(sql)
	if cursor.rowcount == 0:
		logstr =  "No active labs found"
		logit(logfile,"get_active_labs",logstr)
	else:
		return cursor
	
def get_games_list(logfile,path):
	gameList=os.listdir(path)
	gameList.sort()
	return gameList
	
def get_gsws_games_list(logfile):
#	sqlx = "SELECT DISTINCT TaskId,TaskName FROM GswsResults WHERE RecommendedRootPath NOT LIKE '%<URL>%'"
#	sqlx = "SELECT DISTINCT TaskId,TaskName FROM GswsResults"
	sqlx = "SELECT DISTINCT TaskName FROM GswsResults"
	cursorx.execute(sqlx)
	rows = cursorx.fetchall()
#	for row in rows:
#		print row.TaskId, row.TaskName
	# if cursorx.rowcount == 0:
		# print 'No games found in GswsResults view'
	# else:
		# for row in cursorx:
			# print row[0],row[1]
	# return cursorx
	return rows
def get_titleID(logfile,game,path):
	gameIDList=os.listdir(path)
	if len(gameIDList) == 0:
		logstr =  'No gameID found for: ' + game
		logit(logfile,"get_titleID",logstr)			
	elif len(gameIDList) > 1:
		logstr =  'More than one gameID found for ' + game
		logit(logfile,"get_titleID",logstr)
	else:
		gameID = gameIDList[0]
	sql = "SELECT gameID, name FROM tblTitles WHERE gameID=%s"
	args = (gameID)
	cursor.execute(sql, [args])
	if cursor.rowcount == 0:
		sql = "INSERT into tblTitles(name,gameID) VALUES(%s,%s)"
		args = (game,gameID)
		cursor.execute(sql, args)
		con.commit()
	elif cursor.rowcount > 1:
		logstr = "more than one gameID found in db:  " + str(gameID)
		logit(logfile,"get_titleID",logstr)
	sql = "SELECT gameID,titleID FROM tblTitles Where gameID=%s"
	args = (gameID)
	cursor.execute(sql, [args])
	for (titleID) in cursor:
		titleID = int(titleID[1])
	return (gameID,titleID)
	
def get_titleID_iggeqadb(logfile,TaskId,TaskName):
	sql = "SELECT titleID, name FROM tblTitles WHERE name=%s AND gameID=%s"
	args = ([TaskName],TaskId)
	try:
		cursor.execute(sql, args)
		con.commit()
	except mdb.Error, e:
		print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
	if cursor.rowcount == 0:
		print 'TaskName not found in iggeqadb.tblTitles:', TaskName
		sql = "INSERT into tblTitles(name,gameID) VALUES(%s,%s)"
		args = (TaskName,TaskId)
		try:
			cursor.execute(sql, args)
			con.commit()
		except mdb.Error, e:
			print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
	elif cursor.rowcount > 1:
		logstr = "multiple records found in iggegadb.tblTitles for TaskName: " + TaskName
		logit(logfile, "get_titleID_iggeqadb",logstr)
	sql = "SELECT titleID FROM tblTitles Where name=%s AND gameID=%s"
	args = (TaskName,[TaskId])
	try:
		cursor.execute(sql, args)
		con.commit()
	except mdb.Error, e:
		print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
	if cursor.rowcount == 0:
		logstr = "No records found in tblTitles for gameID: " + TaskId
		logit(logfile, "get_titleID_iggeqadb", logstr)
		titleId = 0
	elif cursor.rowcount > 1:
		logstr = "Multiple records found in iggeqadb.tblTitles for TaskId:",TaskId,"TaskName:",TaskName
		logit(logfile, "get_titleID_iggeqadb", logstr)
		titleID = 0
	else:
		for (titleID) in cursor:
			titleId = int(titleID[0])
	return (titleId)
		
def get_platform_list(logfile,TaskId):
	sqlx = 'SELECT DISTINCT RecommendedRootPath, BucketId, BucketName FROM GswsResults WHERE TaskId=?' #Note:  removed DeviceId from this query since it resulted in much duplication.
	argsx = (TaskId)
	cursorx.execute(sqlx,argsx)
	rows = cursorx.fetchall()
	return rows
	# if cursorx.rowcount == 0:
		# logstr = 'No results found in GswsResults view for taskId: ' + str(taskId)
		# logit(logfile, "get_platform_list",logstr)
	# return cursorx
		
def get_platformID(logfile,platform):
	sql = "SELECT platformID,description FROM tblPlatforms WHERE description=%s"
	args = (platform)
	cursor.execute(sql,[args])
	if cursor.rowcount == 0:
		sql = "INSERT into tblPlatforms(description) VALUES(%s)"
		args = (platform)
		cursor.execute(sql,[args])
		con.commit()
	elif cursor.rowcount > 1:
		logstr = "multiple platform records found in datase:  " + platform
		logit(logfile,"get_platformID",logstr)
	sql = "SELECT platformID, bucketID, bucketName FROM tblPlatforms WHERE description=%s"
	args = (platform)
	cursor.execute(sql, [args])
	for (data) in cursor:
		platformID = int(data[0])
		bucketID = data[1]
		bucketName = data[2]
		if (not bucketID) or (not bucketName):
			platform_bucketed = "No"
		else:
			platform_bucketed = "Yes"
	return (platformID,platform_bucketed)

def	get_platformID_iggeqadb(logfile,platform,bucketId,bucketName):
	sql = "SELECT platformID FROM tblPlatforms WHERE description=%s"
	args = ([platform])
	try:
		cursor.execute(sql, args)
		con.commit()
	except mdb.Error, e:
		print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
	if cursor.rowcount == 0:
		print 'Platform not found in iggeqadb.tblPlatforms:', platform
		sql = "INSERT into tblPlatforms(description) VALUES(%s)"
		args = ([platform])
		try:
			cursor.execute(sql, args)
			con.commit()
		except mdb.Error, e:
			print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
	elif cursor.rowcount > 1:
		logstr = "multiple records found in iggegadb.tblPlatforms for Platform: " + platform
		logit(logfile, "get_platformID_iggeqadb",logstr)
	sql = "SELECT platformID,bucketID,bucketName FROM tblPlatforms Where description=%s"
	args = ([platform])
	try:
		cursor.execute(sql, args)
		con.commit()
	except mdb.Error, e:
		print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
	if cursor.rowcount == 0:
		logstr = "No records found in tblPlatforms for platform: " + platform
		logit(logfile, "get_platformID_iggeqadb", logstr)
		platformId = 0
		bucketed = "No"
	elif cursor.rowcount > 1:
		logstr = "Multiple records found in iggeqadb.tblPlatforms for platform:",platform
		logit(logfile, "get_platformID_iggeqadb", logstr)
		platformId = 0
		bucketed = "No"
	else:
		for (data) in cursor:
			platformId = int(data[0])
			if (str(bucketId)==data[1]) and (bucketName==data[2]):
				bucketed = "Yes"
			else:
				bucketed = "No"
				logstr ="Platform is not bucketed: " + platform
				logit(logfile, "get_platformID_iggeqadb", logstr)
	return (platformId,bucketed)
	
def get_labId_iggeqadb(logfile,labname):
	sql = "SELECT labId FROM tbllabs WHERE labName=%s"
	args = ([labname])
	cursor.execute(sql,args)
	if cursor.rowcount == 0:
		logstr = "No records found in iggeqadb.tbllabs for labname: " + labname
		logit(logfile, "get_labID_iggeqadb", logstr)
		labId = 0
	elif cursor.rowcount > 1:
		logstr = "Multiple records found in iggeqadb.tbllabs forlabname: " + labname
		logit(logfile, "get_labID_iggeqadb", logstr)
		labId = 0
	else:
		for (data) in cursor:
			labId = int(data[0])
	return(labId)
	
def get_benchmarkID(logfile,labID,titleID,gameID,platformID):
	sql = "SELECT benchmarkID FROM tblBenchmarks WHERE labID=%s AND titleID=%s AND platformID=%s"
	args = (labID,titleID,platformID)
	cursor.execute(sql, args)
	if cursor.rowcount == 0:
		sql = "INSERT into tblBenchmarks(labID,titleID,gameID,platformID) VALUES(%s,%s,%s,%s)"
		args = (labID,titleID,gameID,platformID)
		cursor.execute(sql, args)
		con.commit()
	elif cursor.rowcount > 1:
		logstr = "multiple benchmards found"
		logit(logfile,"get_benchmarkID",logstr)
	sql = "SELECT benchmarkID FROM tblBenchmarks WHERE labID=%s AND titleID=%s AND platformID=%s" 
	args = (labID,titleID,platformID)
	cursor.execute(sql, args)
	for (benchmarkID) in cursor:
		benchmarkID = int(benchmarkID[0])
	return benchmarkID
	
#def get_benchmarkID_iggeqadb(logfile,titleID,gameID,platformID):
#	sql = "SELECT benchmarkID FROM tblBenchmarks WHERE labID=%s AND titleID=%s AND platformID=%s"

def get_dashboard_data(logfile,gameID, benchmarkID, platformID, platform_bucketed):
	sqlx = 'SELECT DISTINCT TaskGuid,TaskName, SalesForceID, FinishedDate, ReleaseDate  FROM GswsResults WHERE TaskID=?'
	parmsx = (gameID)
	cursorx.execute(sqlx,parmsx)
	have_DashBoardEntry = ''
	if cursorx.rowcount == 0:
		have_DashBoardEntry = "No"
		TaskGuid = 'None'
		TaskName = 'None'
		SalesForceID = 'None'
		FinishedDate = 'None'
		ReleaseDate = 'None'
	elif cursorx.rowcount > 1:
		have_DashBoardEntry = "Multiple"
		TaskGuid = 'Multiple'
		TaskName = 'Multiple'
		SalesForceID = 'Multiple'
		FinishedDate = 'Multiple'
		ReleaseDate = 'Multiple'
	else:
		have_DashBoardEntry = "Yes"
		for data in cursorx:
			TaskGuid = data[0]
			TaskName = data[1]
			SalesForceID = data[2]
#			GraphicsBrand = unicodedata.normalize('NFKD',data[6]).encode('ascii','ignore')
			FinishedDate = data[3]
			ReleaseDate = data[4]
	sql = "UPDATE tblTitles SET taskguid=%s, \
				salesforceid=%s, \
				finisheddate=%s, \
				releasedate=%s \
				WHERE gameID=%s"
	args = (TaskGuid,SalesForceID,FinishedDate,ReleaseDate,gameID)
	try:
		cursor.execute(sql, args)
		con.commit()
	except mdb.Error, e:
		print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
	if have_DashBoardEntry == 'No':
		logstr = 'No DashBoard Entry for:  ' + str(gameID)
		logit(logfile,"get_dashboard_data",logstr)
	elif have_DashBoardEntry == 'Multiple':
		logstr = 'Multiple DashBoard Entries for:  ' + str(gameID)
		logit(logfile,"get_dashboard_data",logstr)
	sqlx = 'SELECT Thumbnail FROM GswsResults WHERE TaskID=?'
	parmsx = (gameID)
	cursorx.execute(sqlx,parmsx)
	if cursorx.rowcount == 0:
		logstr = 'No Thumbnail found for:  ' + str(gameID)
		logit(logfile,"get_benchmarkID",logstr)
		have_thumbnail = 0
	elif cursorx.rowcount > 1:
		logstr = 'Multiple Thumbnails found for:  ' + str(gameID)
		logit(logfile,"get_dashboard_data",logstr)
		have_thumbnail = ''
	else:
		have_thumbnail = 1
	sql = "UPDATE tblTitles SET have_thumbnail=%s WHERE gameID=%s"
	args = (have_thumbnail,gameID)
	try:
		cursor.execute(sql, args)
		con.commit()
	except mdb.Error, e:
		print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
	if platform_bucketed == "Yes":
		sql = "SELECT bucketid,bucketname FROM tblplatforms WHERE platformID=%s"
		args = ([platformID])
		try:
			cursor.execute(sql, args)
			con.commit()
		except mdb.Error, e:
			print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
		if cursor.rowcount == 0:
			logstr = 'Error: No platform found, though bucketed is yes.  platformID: ' + str(platformID)
			logit(logfile,"get_benchmarkID",logstr)
		elif cursor.rowcount > 1:
			logstr = 'Error: Multiple platforms found for platformID: ' + str(platformID)
		else:
			for data in cursor:
				bucketid = data[0]
				bucketname = data[1]
			sqlx = 'SELECT DISTINCT TaskName, BucketId, BucketName, RecommendedRootPath FROM GswsResults WHERE TaskID=? AND BucketId=? AND BucketName=?'
			parmsx = (gameID,bucketid,bucketname)
			cursorx.execute(sqlx,parmsx)
			if cursorx.rowcount == 0:
				logstr = 'No DashBoard Bucket Information for:  ' + str(gameID) + ' platformId: ' + str(platformID)
				logit(logfile,"get_dashboard_data",logstr)				
			elif cursorx.rowcount > 1:
				logstr = 'Multiple DashBoard Bucket Matches found for:  ' + str(gameID) + ' platformId: ' + str(platformID)
				logit(logfile,"get_dashboard_data",logstr)				
			else:
				for data in cursorx:
					rrp = data[3]
				sql = "UPDATE tblBenchmarks SET bucketid=%s, \
						bucketname=%s, \
						recommendedrootpath=%s \
						WHERE benchmarkID=%s"
				args = (bucketid, bucketname, rrp,[benchmarkID])
				try:
					cursor.execute(sql, args)
					con.commit()
				except mdb.Error, e:
					print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])				
	else:
		logstr = 'Platform not assigned bucketing information:  ' + str(platformID)
		logit(logfile,"get_dashboard_data",logstr)
		sql = "UPDATE tblBenchmarks SET recommendedrootpath='Unknown' WHERE benchmarkID=%s"
		args = ([benchmarkID])
		try:
			cursor.execute(sql, args)
			con.commit()
		except mdb.Error, e:
			print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])	
			
def test_gname(logfile,gname,titleId):
	if gname.find(':') or gname.find('/'):
		for ch in [':','/']:
			if ch in gname:
				gname = gname.replace(ch,"")
				print 'gname with ch replaced:', gname
				logstr = 'directory name for ' + gname + ' modified from original to remove special character'
				print 'logstr:',logstr
	sql = "UPDATE tbltitles SET alias=%s WHERE titleID=%s"
	args = (gname,titleId)
	try:
		cursor.execute(sql, args)
		con.commit()
	except mdb.Error, e:
		print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])	
	return gname	
#					logit(logfile,"traverse_gswsResults root",logstr)
	
def get_paths_iggeqadb(logfile,labId):
		sql = "SELECT vcFileShare,localFileShare FROM tbllabs WHERE labID=%s"
		args = ([labId])
		try:
			cursor.execute(sql, args)
			con.commit()
		except mdb.Error, e:
			print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
		if cursor.rowcount == 0:
			logstr = 'Error: No lab found for labId: ' + str(labId)
			logit(logfile,"get_paths_iggeqadb",logstr)
			r_path = ''
			l_path = ''
		elif cursor.rowcount > 1:
			logstr = 'Error: Multiple labs found for labId: ' + str(labId)
			logit(logfile,"get_paths_iggeqadb",logstr)
			r_path = ''
			l_path = ''
		else:
			for data in cursor:
				r_path = data[0]
				l_path = data[1]
		return(r_path,l_path)
		
def get_screenshots(logfile,r_path,l_path,benchmarkID):
	if not os.path.exists(r_path):
		logstr = "Remote path does not exist:  " + r_path + "  benchmarkID:  " + str(benchmarkID)
		logit(logfile,"get_screenshots",logstr)
	else:
		if not os.path.exists(l_path):
			os.makedirs(l_path)	
		fileList=os.listdir(r_path)
		fileList.sort()
		n = 0
		if len(fileList) > 0:
			for file in fileList:
				if os.path.isfile(r_path + file) and file != 'Thumbs.db':
					have_screenshots = "Yes"
					if os.path.exists(l_path + file):
						rhexdigest = md5Checksum(r_path + file)
						lhexdigest = md5Checksum(l_path + file)
						sql = "SELECT ssID, benchmarkID, ssFilename, chksum FROM tblScreenShots WHERE ssFilename=%s AND benchmarkID=%s"
						args = (file, benchmarkID)
						cursor.execute(sql, args)
						if cursor.rowcount == 0:
							logstr = "chksum not previously recorded but file has been copied:  " + file + "  benchmarkID:  " + str(benchmarkID)
							logit(logfile,"get_screenshots",logstr)
							sql = "INSERT into tblScreenShots(benchmarkID,ssFilename,chksum) VALUES(%s,%s,%s)"
							args = (benchmarkID, file, rhexdigest)
							cursor.execute(sql, args)
							con.commit()
						else:
							for (chksum) in cursor:
								chksum = chksum[3]
							if rhexdigest != chksum:
								logstr = 'file has changed:  ' + file + "  benchmarkID:  " + str(benchmarkID)
								logit(logfile,"get_screenshots",logstr)
					else:
						shutil.copy (r_path + file, l_path + file)
						lhexdigest = md5Checksum(l_path + file)
						rhexdigest = md5Checksum(r_path + file)
						if lhexdigest != rhexdigest:
							logstr = "Copy failed:  " + file + "  benchmarkID:  " + str(benchmarkID)
							logit(logfile,"get_screenshots",logstr)
						else:
							sql = "SELECT ssID, benchmarkID, ssFilename, chksum FROM tblScreenShots WHERE ssFilename=%s AND benchmarkID=%s"
							args = (file, benchmarkID)
							cursor.execute(sql, args)
							if cursor.rowcount == 0:
								sql = "INSERT into tblScreenShots(benchmarkID,ssFilename,chksum) VALUES(%s,%s,%s)"
								args = (benchmarkID, file, rhexdigest)
								cursor.execute(sql, args)
								con.commit()
							elif cursor.rowcount > 1:
								logstr = "Multiple entries for screenshot found  " + file + "  benchmarkID:  " + str(benchmarkID)
								logit(logfile,"get_screenshots",logstr)
							else:
								logstr = "file was previously recorded but local copy deleted:  " + file + "  benchmarkID:  " + str(benchmarkID)
								logit(logfile,"get_screenshots",logstr)
					n = n + 1
				sql = "UPDATE tblBenchmarks SET num_screenshots=%s WHERE benchmarkID=%s"
				args = (n, benchmarkID)
				try:
					cursor.execute(sql, args)
					con.commit()
				except mdb.Error, e:
					print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
		else:
			sql = "UPDATE tblBenchmarks SET num_screenshots='0' WHERE benchmarkID=%s"
			try:
				cursor.execute(sql, [benchmarkID])
				con.commit()
			except mdb.Error, e:
				print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
				
def get_config_files(logfile,r_path,l_path,benchmarkID):
	if not os.path.exists(r_path):
		logstr = "Remote path does not exist:  " + r_path + "  benchmarkID:  " + str(benchmarkID)
		logit(logfile,"get_config_files",logstr)
	else:
		if not os.path.exists(l_path):
			os.makedirs(l_path)
		fileList=os.listdir( r_path)
		n = 0
		if len(fileList) > 0:
			fileList.sort()
			for file in fileList:
				if os.path.exists(l_path + file):
					rhexdigest = md5Checksum(r_path + file)
					lhexdigest = md5Checksum(l_path + file)
					sql = "SELECT configID, benchmarkID, configFilename, chksum FROM tblConfigs WHERE configFilename=%s AND benchmarkID=%s"
					args = (file, benchmarkID)
					cursor.execute(sql, args)
					if cursor.rowcount == 0:
						logstr = "chksum not previously recorded but file has been copied:  " + file + "  benchmarkID:  " + str(benchmarkID)
						logit(logfile,"get_config_files",logstr)
						sql = "INSERT into tblConfigs(benchmarkID,configFilename,chksum) VALUES(%s,%s,%s)"
						args = (benchmarkID, file, rhexdigest)
						cursor.execute(sql, args)
						con.commit()
					else:
						for (chksum) in cursor:
							chksum = chksum[3]
						if rhexdigest != chksum:
							logstr = 'file has changed:  ' + file + "  benchmarkID:  " + str(benchmarkID)
							logit(logfile,"get_config_files",logstr)
							#  Need to determine what to do in this case
				else:
						shutil.copy (r_path + file, l_path + file)
						lhexdigest = md5Checksum(l_path + file)
						rhexdigest = md5Checksum(r_path + file)
						if lhexdigest != rhexdigest:
							logstr = "Copy failed:  " + file + "  benchmarkID:  " + str(benchmarkID)
							logit(logfile,"get_config_files",logstr)
							#  Need to determine course of action in this case
						else:
							sql = "SELECT configID, benchmarkID, configFilename, chksum FROM tblConfigs WHERE configFilename=%s AND benchmarkID=%s"
							args = (file, benchmarkID)
							cursor.execute(sql, args)
							if cursor.rowcount == 0:
								sql = "INSERT into tblConfigs(benchmarkID,configFilename,chksum) VALUES(%s,%s,%s)"
								args = (benchmarkID, file, rhexdigest)
								cursor.execute(sql, args)
								con.commit()
							elif cursor.rowcount > 0:
								logstr = "multiple config files with same name found in database:  " + file + "  benchmarkID:  " + str(benchmarkID)
								logit(logfile,"get_config_files",logstr)
							else:
								logstr = "config file was previously recorded but local copy deleted:  " + file + "  benchmarkID:  " + str(benchmarkID)
								logit(logfile,"get_config_files",logstr)
				n = n + 1
			sql = "UPDATE tblBenchmarks SET num_configs=%s WHERE benchmarkID=%s"
			args = (n, benchmarkID)
			try:
				cursor.execute(sql, args)
				con.commit()
			except mdb.Error, e:
				print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
		else:
			sql = "UPDATE tblBenchmarks SET num_configs='0' WHERE benchmarkID=%s"
			try:
				cursor.execute(sql, [benchmarkID])
				con.commit()
			except mdb.Error, e:
				print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
