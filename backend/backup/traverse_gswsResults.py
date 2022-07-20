<BU>import os, sys, glob, re, shutil, hashlib
import MySQLdb as mdb
import pyodbc, base64
from io import BytesIO
from PIL import Image
import unicodedata
import datetime


from functions import get_active_labs
from functions import md5Checksum
from functions import logit
from functions import get_titleID
from functions import get_platformID
from functions import get_benchmarkID
from functions import get_dashboard_data
from functions import get_screenshots
from functions import get_config_files
from functions import get_gsws_games_list
from functions import get_titleID_iggeqadb
from functions import get_platform_list
from functions import get_platformID_iggeqadb
from functions import get_labId_iggeqadb
from functions import get_paths_iggeqadb
from functions import test_gname

global logfile

print "Begin run:", str(datetime.datetime.now())
dtstart =  str(datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S"))
local<BU>path = 'D:\\Projects\\IGGE\\<BU>localrepo'
logfile = 'D:\\Projects\\IGGE\\logfiles\\get_gsws_data_logfile_' + dtstart + '.txt'
logit(logfile,"traverse_gswsResults root","Begin run")

# fspath = lab[2]

gswsgameList = get_gsws_games_list(logfile)						#	Games List
for gswsgame in gswsgameList:
	f = open('excludefile.txt')
	c = open('completedfile.txt')
	lines = f.readlines()
	comp = c.readlines()
	excludes = [str(e.strip()) for e in lines]
	completed = [str(d.strip()) for d in comp]
	f.close
	c.close
	if gswsgame.TaskName in excludes:
		print '    game excluded:',gswsgame.TaskName
	elif gswsgame.TaskName in completed:
		print '    game already completed:',gswsgame.TaskName
	else:
		#  Need to search gsws for gsws.TaskName and choose only the latest TaskId.  Then replace all gsws.TaskId's with this new taskId.
		#  gswsgame is now set to only pull Distinct TaskName 
		titleId = get_titleID_iggeqadb(logfile,gswsgame.TaskId,gswsgame.TaskName)		#titleID
		platformList = get_platform_list(logfile,gswsgame.TaskId)
		for platformdata in platformList:
			platform = platformdata.RecommendedRootPath.split('\\')[len(platformdata.RecommendedRootPath.split('\\'))-3]
			labName = platformdata.RecommendedRootPath.split('\\')[2].split('.')[0]
			labId = get_labId_iggeqadb(logfile,labName)
			pdata = get_platformID_iggeqadb(logfile,platform,platformdata.BucketId,platformdata.BucketName)		#platformID
			platformId = pdata[0]
			bucketed = pdata[1]
			benchmarkId = get_benchmarkID(logfile,labId,titleId,gswsgame.TaskId,platformId)		#benchmarkID
			print 'TitleId:',gswsgame.TaskId,'TitleName:',gswsgame.TaskName,'platform:',platform
			paths = get_paths_iggeqadb(logfile,labId)
			r_path_base = paths[0]
			l_path_base = paths[1]
			get_dashboard_data(logfile,gswsgame.TaskId,benchmarkId,platformId,bucketed)				#Get dashboard data for gameID(taskID)
			gname = test_gname(logfile,gswsgame.TaskName,titleId)
			r_path = platformdata.RecommendedRootPath
			l_path = l_path_base + '\\' + gname + '\\RTM\\' + str(gswsgame.TaskId) + '\\benchmarks\\' + platform + '\\Recommended\\'
			get_screenshots(logfile,platformdata.RecommendedRootPath,l_path,benchmarkId,)
			r_path = r_path + 'GameSettingFiles\\'
			l_path= l_path + 'GameSettingFiles\\'
			get_config_files(logfile,r_path,l_path,benchmarkId)
		c = open( 'completedfile.txt', 'a' )
		c.write(gswsgame.TaskName + '\n')
		c.close
logit(logfile,"traverse_gswsResults root","End run")
print "End run:", str(datetime.datetime.now())
