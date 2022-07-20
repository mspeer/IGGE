<BU>import os, glob, re, shutil, hashlib
import MySQLdb as mdb

con = mdb.connect('localhost','root','_PW_','iggeqadb')
cursor = con.cursor()

local<BU>path = 'D:\\Projects\\IGGE\\<BU>localrepo'
logfile = 'D:\\Projects\\IGGE\\logfiles\\logfile.txt'
log = open( logfile, 'a')

def scandirs(path):
	for currentFile in glob.glob( os.path.join(path, '*') ):
		if os.path.isdir(currentFile):
			scandirs(currentFile)
def md5Checksum(filePath):
	with open(filePath, 'rb') as fh:
		m = hashlib.md5()
		while True:
			data = fh.read(8192)
			if not data:
				break
		m.update(data)
	return m.hexdigest()
#	Lab identification	
sql = "SELECT labID, labName,vcFileShare FROM tblLabs WHERE active=True"
cursor.execute(sql)
if cursor.rowcount == 0:
	logstr =  "No active labs found"
	log.write(logstr + '\n')
#	Exit()
else:
	for (labID, labName, vcFileShare) in cursor:
		path = vcFileShare
		print 'Entering into:  ' + path
# Have labID
#	Game title identification
		gameList=os.listdir(path)
		gameList.sort()
		for game in gameList:
			f = open('excludefile.txt')
			lines = f.readlines()
			excludes = [str(e.strip()) for e in lines]
			if game in excludes:
				print 'game exluded: ' + game
			else:
				gameIDList=os.listdir(path+'\\'+game+'\\RTM')
				if len(gameIDList) == 0:
					logstr =  'No gameID found for ' + game
					log.write(logstr + '\n')
					
				elif len(gameIDList) > 1:
					logstr =  'More than one gameID found for ' + game
					log.write(logstr + '\n')
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
					logstr = "more than one gameID found in db"
					log.write(logstr + '\n')
				sql = "SELECT gameID,titleID FROM tblTitles Where gameID=%s"
				args = (gameID)
				cursor.execute(sql, [args])
				for (titleID) in cursor:
	#				print titleID
					titleID = int(titleID[1])
		# Have titleID
	#	Platform identification
				platformList=os.listdir( path + '\\' + game + '\\RTM\\' + gameID + '\\benchmarks\\' )
				platformList.sort()
				for platform in platformList:
					if os.path.isdir(path + '\\' + game + '\\RTM\\' + gameID + '\\benchmarks\\' + platform) and re.search(r'^BDW|^HSW',platform):
						sql = "SELECT platformID,description FROM tblPlatforms WHERE description=%s"
						args = (platform)
						cursor.execute(sql,[args])
						if cursor.rowcount == 0:
							sql = "INSERT into tblPlatforms(description) VALUES(%s)"
							args = (platform)
							cursor.execute(sql,[args])
							con.commit()
						elif cursor.rowcount > 1:
							logstr = "multiple platform records found in datase"
							log.write(logstr + '\n')
						sql = "SELECT platformID FROM tblPlatforms WHERE description=%s"
						args = (platform)
						cursor.execute(sql, [args])
						for (platformID) in cursor:
							platformID = int(platformID[0])
		# Have platformID
	#	Benchmark identification
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
							log.write(logstr + '\n')
						sql = "SELECT benchmarkID FROM tblBenchmarks WHERE labID=%s AND titleID=%s AND platformID=%s" 
						args = (labID,titleID,platformID)
						cursor.execute(sql, args)
						for (benchmarkID) in cursor:
							benchmarkID = int(benchmarkID[0])
		#  Have BenchmarkID
#						print benchmarkID
		#  Check if have local directory to store screenshots and config files, if not create it in local<BU>path
						localpath=local<BU>path + '\\' + game + '\\RTM\\' + gameID + '\\benchmarks\\' + platform + '\\Recommended'
						if not os.path.exists(localpath):
							os.makedirs(localpath)
		#  Get list of screenshot files:
						fileList=os.listdir( path + '\\' + game + '\\RTM\\' + gameID + '\\benchmarks\\' + platform + '\\Recommended')
						fileList.sort()
						if len(fileList) > 0:
							print len(fileList), "screen shot file(s) found"
							sql = "UPDATE tblBenchmarks SET have_screenshots=TRUE WHERE benchmarkID=%s"
							try:
								cursor.execute(sql, [benchmarkID])
								con.commit()
							except:
								print 'There was a MySQL warning.'
							for file in fileList:
								if os.path.isfile(path + '\\' + game + '\\RTM\\' + gameID + '\\benchmarks\\' + platform + '\\Recommended\\' + file) and file != 'Thumbs.db':	
									if os.path.exists(local<BU>path + '\\' + game + '\\RTM\\' + gameID + '\\benchmarks\\' + platform + '\\Recommended\\' + file):
										rhexdigest = md5Checksum(path + '\\' + game + '\\RTM\\' + gameID + '\\benchmarks\\' + platform + '\\Recommended\\' + file)
										lhexdigest = md5Checksum(local<BU>path + '\\' + game + '\\RTM\\' + gameID + '\\benchmarks\\' + platform + '\\Recommended\\' + file)
										sql = "SELECT ssID, benchmarkID, ssFilename, chksum FROM tblScreenShots WHERE ssFilename=%s AND benchmarkID=%s"
										args = (file, benchmarkID)
										cursor.execute(sql, args)
										if cursor.rowcount == 0:
											logstr = "chksum not previously recorded but file has been copied"
											log.write(logstr + '\n')
											sql = "INSERT into tblScreenShots(benchmarkID,ssFilename,chksum) VALUES(%s,%s,%s)"
											args = (benchmarkID, file, rhexdigest)
											cursor.execute(sql, args)
											con.commit()
										else:
											for (chksum) in cursor:
												chksum = chksum[3]
											if rhexdigest != chksum:
												logstr = 'file has changed'
												log.write(logstr + '\n')
									else:
										shutil.copy (path + '\\' + game + '\\RTM\\' + gameID + '\\benchmarks\\' + platform + '\\Recommended\\' + file, local<BU>path + '\\' + game + '\\RTM\\' + gameID + '\\benchmarks\\' + platform + '\\Recommended\\' + file)
										lhexdigest = md5Checksum(local<BU>path + '\\' + game + '\\RTM\\' + gameID + '\\benchmarks\\' + platform + '\\Recommended\\' + file)
										rhexdigest = md5Checksum(path + '\\' + game + '\\RTM\\' + gameID + '\\benchmarks\\' + platform + '\\Recommended\\' + file)
										if lhexdigest != rhexdigest:
											logstr = "Copy failed"
											log.write(logstr + '\n')
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
												logstr = "Multiple entries for screenshot found"
												log.write(logstr + '\n')
											else:
												logstr = "file was previously recorded but local copy deleted"
												log.write(logstr + '\n')
						else:
							print "No screen shot files found"
							sql = "UPDATE tblBenchmarks SET have_screenshots=FALSE WHERE benchmarkID=%s"
							try:
								cursor.execute(sql, [benchmarkID])
								con.commit()
							except:
								print 'There was a MySQL warning.'
		#  Get config files							
						localpath=local<BU>path + '\\' + game + '\\RTM\\' + gameID + '\\benchmarks\\' + platform + '\\Recommended\\GameSettingFiles'
						if not os.path.exists(localpath):
							os.makedirs(localpath)
						fileList=os.listdir( path + '\\' + game + '\\RTM\\' + gameID + '\\benchmarks\\' + platform + '\\Recommended\\GameSettingFiles')
						if len(fileList) > 0:
							print len(fileList), "configuration file(s) found"
							sql = "UPDATE tblBenchmarks SET have_config=TRUE WHERE benchmarkID=%s"
							try:
								cursor.execute(sql, [benchmarkID])
								con.commit()
							except:
								print 'There was a MySQL warning.'
							fileList.sort()
							for file in fileList:
								if os.path.exists(local<BU>path + '\\' + game + '\\RTM\\' + gameID + '\\benchmarks\\' + platform + '\\Recommended\\GameSettingFiles\\' + file):
									rhexdigest = md5Checksum(path + '\\' + game + '\\RTM\\' + gameID + '\\benchmarks\\' + platform + '\\Recommended\\GameSettingFiles\\' + file)
									lhexdigest = md5Checksum(local<BU>path + '\\' + game + '\\RTM\\' + gameID + '\\benchmarks\\' + platform + '\\Recommended\\GameSettingFiles\\' + file)
									sql = "SELECT configID, benchmarkID, configFilename, chksum FROM tblConfigs WHERE configFilename=%s AND benchmarkID=%s"
									args = (file, benchmarkID)
									cursor.execute(sql, args)
									if cursor.rowcount == 0:
										logstr = "chksum not previously recorded but file has been copied"
										log.write(logstr + '\n')
										sql = "INSERT into tblConfigs(benchmarkID,configFilename,chksum) VALUES(%s,%s,%s)"
										args = (benchmarkID, file, rhexdigest)
										cursor.execute(sql, args)
										con.commit()
									else:
										for (chksum) in cursor:
											chksum = chksum[3]
										if rhexdigest != chksum:
											logstr = 'file has changed'
											log.write(logstr + '\n')
											#  Need to determine what to do in this case
								else:
										shutil.copy (path + '\\' + game + '\\RTM\\' + gameID + '\\benchmarks\\' + platform + '\\Recommended\\GameSettingFiles\\' + file, local<BU>path + '\\' + game + '\\RTM\\' + gameID + '\\benchmarks\\' + platform + '\\Recommended\\GameSettingFiles\\' + file)
										lhexdigest = md5Checksum(local<BU>path + '\\' + game + '\\RTM\\' + gameID + '\\benchmarks\\' + platform + '\\Recommended\\GameSettingFiles\\' + file)
										rhexdigest = md5Checksum(path + '\\' + game + '\\RTM\\' + gameID + '\\benchmarks\\' + platform + '\\Recommended\\GameSettingFiles\\' + file)
										if lhexdigest != rhexdigest:
											logstr = "Copy failed"
											log.write(logstr + '\n')
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
												logstr = "multiple config files with same name found in database"
												log.write(logstr + '\n')
											else:
												logstr = "config file was previously recorded but local copy deleted"
												log.write(logstr + '\n')
						else:
							print "No config files found"
							sql = "UPDATE tblBenchmarks SET have_config=FALSE WHERE benchmarkID=%s"
							try:
								cursor.execute(sql, [benchmarkID])
								con.commit()
							except:
								print 'There was a MySQL warning.'
log.close()
