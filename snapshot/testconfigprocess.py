
#  append to baseurl:  hwconfigurations  --return the HW configuration for all supported graphics brands
#					games/<deviceid>  --return list of playable games for supplied deviceid
#					games/blank/<graphics brand string>  --return list of playable games for supplied graphics brand
#					games/getgame/<taskid>	-- returns game info for supplied taskid
#					games/DownloadImageZip/<taskid>/<deviceid>	--download zip of all screenshots for specified game + deviceid
#					games/DownloadImageZipByGraphicsBrand/<taskid>/<graphics brand string>	--download zip file of all screenshots for specified game + graphics brand
#					games/GetGamesWithConfig	--get a list of games for which at least on config is present
#					games/DownloadconfigZip/<taskid>	--download configuration file for specified taskid
#						Zips up all config files for the game.  maintains the original files names and extensions.  Adds double underscore "__",gameid, another underscore "_" and hardware groupid.
#	Command line arguments are available to bypass user prompt and to allow for automation front end.  Valid entries are 1,2,3 or q
#		corresponding to dev,tst,prd and quit respectively.



import datetime
import os
import sys
import MySQLdb as mdb

from ss_functions import logit
from ss_functions import getargs
from ss_functions import getzipscreenshots
from ss_functions import getHWConfigurations
from ss_functions import loadDeviceIds
from ss_functions import getGamesByDeviceId
from ss_functions import getSSID
from ss_functions import getTitleId
from ss_functions import writethumbnail
from ss_functions import getBenchmarkId
from ss_functions import processscreenshots
from ss_functions import getGamesListWithConfig
from ss_functions import getConfig
from ss_functions import processconfigs
from ss_functions import comparedbs

tempzipdir = 'D:\\Projects\\IGGE\\zipfiles\\'
tmppath = 'D:\\Projects\\IGGE\\tmpfiles\\'

init_data = getargs()
sstype = init_data[0]
baseurl = init_data[1]
ssrepopath = init_data[2]
conss = init_data[3]
cursorss = conss.cursor()	
ssdate = str(datetime.datetime.now().strftime("%Y%m%d"))
ssdata = getSSID(conss,cursorss,ssdate,sstype)
ssid = ssdata[0]
ssidentifier = ssdata[1]
ssarchident = str(ssdate) + "_" + str(ssidentifier)
dtstart =  datetime.datetime.now()
print '\n'
print 'Start run:',str(dtstart)
print 'ssid:',ssid
logfile = 'D:\\Projects\\IGGE\\logfiles\\snapshots\\snapshot_logfile_' + str(ssid) + '_' + str(ssidentifier) + '.txt'
logit(logfile,"gswservice_api_call root","Begin snapshot of:  " + sstype)
if not os.path.exists(tmppath):
	os.makedirs(tmppath)
if not os.path.exists(tempzipdir):
	os.makedirs(tempzipdir)
hwconfigs = getHWConfigurations(baseurl)  #returns list of tuple = (deviceid,bucketid,graphicsbrand,finisheddate,lastupdatedon)
loadDeviceIds(conss,cursorss,ssid,hwconfigs)
configs_sorted = sorted(hwconfigs, key=lambda tup: tup[1])  # Create an ordered list by bucketid to restrict game searched to one set per bucket
bucketid_unique = set()	#Not using this?
hwconfigs_unique = []
bucket_itr = 0
for item in configs_sorted:  #generate a new sorted list with only unique bucketids, first occurance from configs_sorted.
	if item[1] not in bucketid_unique:
		hwconfigs_unique.append(item)
		bucketid_unique.add(item[1])
for hwconfig in hwconfigs_unique: 
	bucket_itr = bucket_itr + 1
	deviceid = hwconfig[0]
	bucketid = hwconfig[1]
	print 'deviceid:',deviceid,'*******************************'+str(bucket_itr)+'************************************************'
	print '\n'
	games = getGamesByDeviceId(deviceid,baseurl)   # returns tuple = (taskid,salesforceid,name,lastupdatedon,finisheddate,releasedate)
	for game in games: 
		taskid = game[0]
		salesforceid = game[1]
		name = game[2]
		lastupdatedon = game[3]
		finisheddate = game[4]
		releasedate = game[5]
		thumbnail = game[6]
		print 'taskid:',taskid,'bucketid:',bucketid
		sstitleid = getTitleId(conss,cursorss,ssid,taskid,name,finisheddate,releasedate,salesforceid,lastupdatedon)
		writethumbnail(conss,cursorss,ssid,tmppath,ssrepopath,thumbnail,taskid,sstitleid,ssarchident)
		getzipscreenshots(tempzipdir,taskid,deviceid,baseurl)
		ssbmid = getBenchmarkId(conss,cursorss,sstitleid,bucketid,ssid)
		num_screenshots = processscreenshots(conss,cursorss,ssbmid,sstitleid,tempzipdir,taskid,bucketid,sstype,ssdate,ssidentifier,ssrepopath,ssarchident,ssid)
		print 'num_screenshots:',num_screenshots
		print '\n'
	print '\n\n'

print '\n'
print 'Processing configurations files'
configs = getGamesListWithConfig(baseurl)
for config in configs:
	print '\n'
	taskid = config
	print '----------------------------------------------------------------------------'
	print 'taskid:',taskid
	getConfig(taskid,ssarchident,tempzipdir,baseurl)
	processconfigs(conss,cursorss,ssid,tempzipdir,ssrepopath,ssarchident)
comparedbs(conss,cursorss,ssid)
dtend = datetime.datetime.now()
dtime = dtend - dtstart
print 'End run:',str(dtend)
print 'Execution time:',str(dtime)	
print '\n'
print 'Hit return to exit'
raw_input()	#This is to hold the window open after the script completes	
