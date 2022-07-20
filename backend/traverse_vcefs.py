import os, sys, glob, re, shutil, hashlib
import MySQLdb as mdb
import pyodbc, base64
from io import BytesIO
from PIL import Image
import unicodedata
import datetime

#includepath = "../includes/functions.py"
#sys.path.append(os.path.abspath(includepath))
from functions import get_active_labs
from functions import md5Checksum
from functions import logit
from functions import get_games_list
from functions import get_titleID
from functions import get_platformID
from functions import get_benchmarkID
from functions import get_dashboard_data
from functions import get_screenshots
from functions import get_config_files

dtstart =  str(datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S"))
local<bu>path = 'D:\\Projects\\IGGE\\<bu>localrepo'

global logfile
logfile = 'D:\\Projects\\IGGE\\logfiles\\scandirs_logfile_' + dtstart + '.txt'

def scandirs(fspath):
	for currentFile in glob.glob( os.path.join(fspath, '*') ):
		if os.path.isdir(currentFile):
			scandirs(currentFile)

print "Begin run:", dtstart
logit(logfile,"scandirs root","Begin run")

labs = get_active_labs(logfile)									#	Lab identification	

for lab in labs:
	labID = lab[0]
	labName = lab[1]
	fspath = lab[2]
	print 'Entering into:  ' + fspath
	gameList = get_games_list(logfile,fspath)						#	Games List
	for game in gameList:
		print '    game:',game
		f = open('excludefile.txt')
		lines = f.readlines()
		excludes = [str(e.strip()) for e in lines]
		if game in excludes:
			print '    game exluded:',game
		else:
			gameData = get_titleID(logfile,game,fspath+'\\'+game+'\\RTM')		#titleID
			gameID = gameData[0]
			titleID = gameData[1]
			platformList=os.listdir( fspath + '\\' + game + '\\RTM\\' + gameID + '\\benchmarks\\' )
			platformList.sort()
			for platform in platformList:
				if os.path.isdir(fspath + '\\' + game + '\\RTM\\' + gameID + '\\benchmarks\\' + platform) and re.search(r'^BDW|^HSW',platform):
					print "        benchmark: ",platform
					data = get_platformID(logfile,platform)		#platformID
					platformID = data[0]
					platform_bucketed = data[1]
					benchmarkID = get_benchmarkID(logfile,labID,titleID,gameID,platformID)		#benchmarkID
					get_dashboard_data(logfile,gameID,benchmarkID,platformID,platform_bucketed)				#Get dashboard data for gameID(taskID)					
					r_path = fspath + '\\' + game + '\\RTM\\' + gameID + '\\benchmarks\\' + platform + '\\Recommended\\'
					l_path = local<BU>path + '\\' + game + '\\RTM\\' + gameID + '\\benchmarks\\' + platform + '\\Recommended\\'
					get_screenshots(logfile,r_path,l_path,benchmarkID,)
					r_path = fspath + '\\' + game + '\\RTM\\' + gameID + '\\benchmarks\\' + platform + '\\Recommended\\GameSettingFiles\\'
					l_path=local<BU>path + '\\' + game + '\\RTM\\' + gameID + '\\benchmarks\\' + platform + '\\Recommended\\GameSettingFiles\\'
					get_config_files(logfile,r_path,l_path,benchmarkID)

logit(logfile,"scandirs root","End run")
print "End run:", str(datetime.datetime.now())
