
#  append to baseurl:  hwconfigurations  --return the HW configuration for all supported graphics brands
#					games/<deviceid>  --return list of playable games for supplied deviceid
#					games/blank/<graphics brand string>  --return list of playable games for supplied graphics brand
#					games/getgame/<taskid>	-- returns game info for supplied taskid
#					games/DownloadImageZip/<taskid>/<deviceid>	--download zip of all screenshots for specified game + deviceid
#					games/DownloadImageZipByGraphicsBrand/<taskid>/<graphics brand string>	--download zip file of all screenshots for specified game + graphics brand
#					games/GamesWithConfig	--get a list of games for which at least on config is present
#					games/DownloadconfigZip/<taskid>	--download configuration file for specified taskid
#						Zips up all config files for the game.  maintains the original files names and extensions.  Adds double underscore "__",gameid, another underscore "_" and hardware groupid.



import datetime
import os

from snapshot_functions import logit
from snapshot_functions import getzipscreenshots
from snapshot_functions import getHWConfigurations
from snapshot_functions import loadDeviceIds
from snapshot_functions import getGamesByDeviceId
from snapshot_functions import getSSID
from snapshot_functions import getTitleId
from snapshot_functions import writethumbnail
from snapshot_functions import getBenchmarkId
from snapshot_functions import processscreenshots
from snapshot_functions import getGamesListWithConfig
from snapshot_functions import getConfig
from snapshot_functions import processconfigs


tempzipdir = 'D:\\Projects\\IGGE\\zipfiles\\'
tmppath = 'D:\\Projects\\IGGE\\tmpfiles\\'
print 'Choose environment to snapshot:\n'
print '1) Development (Not yet enabled)\n'
print '2) Test\n'
print '3) Production\n'
u_in = input("Enter 2 or 3: ")
while u_in not in [2,3]:
	print "Invalid Entry"
	u_in = input("Enter 2 or 3: ")
if u_in == 1:
	sstype = 'dev'
	baseurl = 'yet_to_be_defined'
	ssrepopath = 'D:\\Projects\\IGGE\\SSRepo\\Dev\\'
elif u_in == 2:
	sstype = 'tst'
	baseurl = 'http://192.168.87.212/GSWService/api/'
	ssrepopath = 'D:\\Projects\\IGGE\\SSRepo\\Test\\'
else:
	sstype = 'prd'
	baseurl = 'http://192.198.165.84/GSWService/api/'
	ssrepopath = 'D:\\Projects\\IGGE\\SSRepo\\Prod\\'	
ssdate = str(datetime.datetime.now().strftime("%Y%m%d"))
ssdata = getSSID(ssdate,sstype)
ssid = ssdata[0]
ssidentifier = ssdata[1]
ssarchident = str(ssdate) + "_" + str(ssidentifier)
dtstart =  datetime.datetime.now()
print 'Start run:',str(dtstart)
print 'ssid:',ssid
logfile = 'D:\\Projects\\IGGE\\logfiles\\snapshots\\snapshot_logfile_' + str(ssid) + '_' + str(ssidentifier) + '.txt'
logit(logfile,"gswservice_api_call root","Begin snapshot of:  " + sstype)
if not os.path.exists(tmppath):
	os.makedirs(tmppath)
if not os.path.exists(tempzipdir):
	os.makedirs(tempzipdir)
hwconfigs = getHWConfigurations(baseurl)  #returns list of tuple = (deviceid,bucketid,graphicsbrand,finisheddate,lastupdatedon)
loadDeviceIds(ssid,hwconfigs)
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
	games = getGamesByDeviceId(deviceid,baseurl)   # returns tuple = (taskid,salesforceid,name,lastupdatedon,finisheddate,releasedate)
	for game in games: 
		taskid = game[0]
		salesforceid = game[1]
		name = game[2]
		lastupdatedon = game[3]
		finisheddate = game[4]
		releasedate = game[5]
		thumbnail = game[6]
		print 'taskid:',taskid
		sstitleid = getTitleId(ssid,taskid,name,finisheddate,releasedate,salesforceid,lastupdatedon)
		writethumbnail(ssid,tmppath,ssrepopath,thumbnail,taskid,sstitleid,ssarchident)
		getzipscreenshots(tempzipdir,taskid,deviceid,baseurl)
		ssbmid = getBenchmarkId(sstitleid,bucketid,ssid)
		num_screenshots = processscreenshots(ssbmid,sstitleid,tempzipdir,taskid,bucketid,sstype,ssdate,ssidentifier,ssrepopath,ssarchident)
		print 'num_screenshots:',num_screenshots
		print '\n'
	print '\n\n'
configs = getGamesListWithConfig(baseurl)
print '\n'
print 'Processing configurations files'
for config in configs:
	print '\n'
	taskid = config
	print 'taskid:',taskid
	getConfig(taskid,ssarchident,tempzipdir,baseurl)
	num_configs = processconfigs(ssbmid,sstitleid,	tempzipdir,ssrepopath,ssarchident,taskid)
	print 'num_configs:',num_configs
dtend = datetime.datetime.now()
dtime = dtend - dtstart
print 'End run:',str(dtend)
print 'Execution time:',str(dtime)		
