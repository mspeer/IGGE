import os, sys, glob, re, shutil, hashlib, urllib, zipfile
from time import sleep
import MySQLdb as mdb
import pyodbc, base64
from io import BytesIO
from PIL import Image
import unicodedata
import datetime
import urllib2
import urllib

conss = mdb.connect('localhost','root','_PW_','iggessdb')
cursorss = conss.cursor()

def logit(logfile,caller,statement):
	log = open( logfile, 'a' )
	dtstamp = str(datetime.datetime.now())
	log.write(dtstamp + "|" + caller + "|" + statement + '\n')
	log.close
	print "\t\t\t\t\t" + caller + "\t" + statement

def getSSID(ssdate,sstype):
	sql = "SELECT * FROM tblsnapshots WHERE ssdate=%s AND sstype=%s"
	args = (ssdate,sstype)
	cursorss.execute(sql,args)
	if cursorss.rowcount == 0:
		ssidentifier = 1
	else:
		ssidentifier = cursorss.rowcount + 1
	sql = "INSERT into tblsnapshots(ssdate,sstype,ssidentifier) VALUES(%s,%s,%s)"
	args = (ssdate,sstype,ssidentifier)
	cursorss.execute(sql,args)
	conss.commit()
	sql = "SELECT ssid FROM tblsnapshots Where ssdate=%s AND sstype=%s"
	args = (ssdate,sstype)
	cursorss.execute(sql,args)
	for (ssid) in cursorss:
		ssid = int(ssid[0])
	return (ssid,ssidentifier)	

	
def md5Checksum(filePath):
#	print 'filePath:',filePath
	BLOCKSIZE = 65536
	hasher = hashlib.md5()
	with open(filePath, 'rb') as afile:
		buf = afile.read(BLOCKSIZE)
		while len(buf)>0:
				hasher.update(buf)
				buf = afile.read(BLOCKSIZE)
#	print 'hash:',hasher.hexdigest()
	return hasher.hexdigest()

def getHWConfigurations(baseurl):
	url = baseurl + 'hwconfigurations'
	response = urllib2.urlopen(url)
	tmpstr = response.read().split('},{')
	configs = []
	for str in tmpstr:
		str = str.replace('[{','')
		str = str.replace('}]','')
		tmpstr2 = str.split(',')
		for str2 in tmpstr2:
			str2 = str2.replace('"','')
			data = str2.split(':')
			if 'DeviceId' in data[0]:
				deviceid = data[1]
			elif 'FinishedDate' in data[0]:
				finisheddate = data[1]
			elif 'GraphicsBrand' in data[0]:
				graphicsbrand = data[1]
			elif 'GroupId' in data[0]:
				bucketid = data[1]
			elif 'LastUpdatedOn' in data[0]:
				lastupdatedon = data[1]
		tuple = (deviceid,bucketid,graphicsbrand,finisheddate,lastupdatedon)
		configs.append(tuple)
	return configs

def getGamesByDeviceId(deviceid,baseurl):
	url = baseurl + 'games/' + deviceid
	response = urllib2.urlopen(url)
	tmpstr = response.read().split('},{')
	games = []
	for str in tmpstr:
		str = str.replace('[\'','')
		str = str.replace('\']','')
		tmpstr2 = str.split(',')
		for str2 in tmpstr2:
			str2 = str2.replace('"','')
			data = str2.split(':')
			if 'TaskId' in data[0]:
				taskid = data[1]
			elif 'SalesForceId' in data[0]:
				salesforceid = data[1]
			elif 'Name' in data[0]:
				name = data[1]
			elif 'LastUpdatedOn' in data[0]:
				lastupdatedon = data[1]
			elif 'Thumbnail' in data[0]:
				thumbnail = data[1]
			elif 'FinishedDate' in data[0]:
				finisheddate = data[1]
			elif 'ReleaseDate' in data[0]:
				releasedate = data[1]
		tuple = (taskid,salesforceid,name,lastupdatedon,finisheddate,releasedate,thumbnail)
		games.append(tuple)
	return games

def getzipscreenshots(tempzipdir,taskid,deviceid,baseurl):
	fileList=os.listdir(tempzipdir)
	if len(fileList) > 0:
		for file in fileList:
			os.remove(tempzipdir + file)
	url = baseurl + 'games/DownloadImageZip/' + taskid + '/' + deviceid
	name = os.path.join(tempzipdir, 'temp.zip')
	try:
		name, hdrs = urllib.urlretrieve(url, name)
	except IOError, e:
		print "Can't retrieve %r to %r: %s" % (url, tempzipdir, e)
		return
	try:
		z = zipfile.ZipFile(name)
	except zipfile.error, e:
		print "Bad zipfile (from %r): %s" % (url, e)
		return
	for n in z.namelist():
		dest = os.path.join(tempzipdir, n)
		destdir = os.path.dirname(dest)
		if not os.path.isdir(destdir):
			os.makedirs(destdir)
		data = z.read(n)
		f = open(dest, 'wb')
		f.write(data)
		f.close()
	z.close()
	sleep(0.1)
	os.unlink(name)

def getGamesListWithConfig(baseurl):
	url = baseurl + '/games/GetGamesWithConfig'
	response = urllib2.urlopen(url)
	tmpstr = response.read().split('},{')
	configs = []
	for str in tmpstr:
		str = str.replace('[{','')
		str = str.replace('}]','')
		tmpstr2 = str.split(',')
		for str2 in tmpstr2:
			str2 = str2.replace('"','')
			data = str2.split(':')
			if 'TaskId' in data[0]:
				taskid = data[1]
		configs.append(taskid)
	return configs

def getConfig(taskid,ssarchident,tempzipdir,baseurl):
	fileList=os.listdir(tempzipdir)
	if len(fileList) > 0:
		for file in fileList:
			os.remove(tempzipdir + file)
	url = baseurl + 'games/DownloadConfigZip/' + taskid
	name = os.path.join(tempzipdir, 'temp.zip')
	try:
		name, hdrs = urllib.urlretrieve(url, name)
	except IOError, e:
		print "Can't retrieve %r to %r: %s" % (url, tempzipdir, e)
		return
	try:
		z = zipfile.ZipFile(name)
	except zipfile.error, e:
		print "Bad zipfile (from %r): %s" % (url, e)
		return
	for n in z.namelist():
		dest = os.path.join(tempzipdir, n)
		destdir = os.path.dirname(dest)
		if not os.path.isdir(destdir):
			os.makedirs(destdir)
		data = z.read(n)
		f = open(dest, 'wb')
		f.write(data)
		f.close()
	z.close()
	sleep(0.1)
	os.unlink(name)	
	
def loadDeviceIds(ssid,configs):
	for item in configs:
		deviceid = item[0]
		bucketid = item[1]
		sql = "SELECT ssdid FROM tblssdeviceids WHERE ssid=%s AND deviceid=%s AND bucketid=%s ORDER BY ssdid DESC"
		args = (ssid,deviceid,bucketid)
		cursorss.execute(sql,args)
		if cursorss.rowcount == 0:
			sql = "INSERT into tblssdeviceids(ssid,deviceid,bucketid) VALUES(%s,%s,%s)"
			args = (ssid,deviceid,bucketid)
			cursorss.execute(sql,args)
			conss.commit()
			sql = "SELECT ssdid FROM tblssdeviceids WHERE ssid=%s AND deviceid=%s AND bucketid=%s  ORDER BY ssdid DESC"
			args = (ssid,deviceid,bucketid)
			cursorss.execute(sql,args)
			if cursorss.rowcount == 0:
				print 'error creating deviceid record for deviceid:',deviceid,'bucketid:',bucketid
			elif cursorss.rowcount > 1:
				print 'Error:  multiple records found for deviceid:',deviceid,'bucketid:',bucketid
			else:
				print 'Added new record to tblssdeviceid for deviceid:',deviceid,'bucketid:',bucketid
		elif cursosrs.rowcount >1:
			print 'ERROR:  Multiple matching records found for deviceid:',deviceid
			
def getTitleId(ssid,taskid,name,finisheddate,releasedate,salesforceid,lastupdatedon):	#Need to find out what lastupdateon is and add it below if needed
	sql = "SELECT sstitleid FROM tblsstitles WHERE taskid=%s AND ssid=%s ORDER BY sstitleid DESC"
	args = (taskid,ssid)
	cursorss.execute(sql,args)
	if cursorss.rowcount == 0:
		sql = "INSERT into tblsstitles(ssid,name,taskid,finisheddate,releasedate,salesforceid) VALUES(%s,%s,%s,%s,%s,%s)"
		args = (ssid,name,taskid,finisheddate,releasedate,salesforceid)
		cursorss.execute(sql,args)
		conss.commit()
		sql = "SELECT sstitleid FROM tblsstitles WHERE taskid=%s AND ssid=%s ORDER BY sstitleid DESC"
		args = (taskid,ssid)
		cursorss.execute(sql,args)
		if cursorss.rowcount == 0:
			print 'error creating title record for taskid:',taskid
			sstitleid = 0
		elif cursorss.rowcount > 1:
			print 'Error:  multiple records found for taskid:',taskid
			sstitleid = 0
		else:
			data = cursorss.fetchone()
			sstitleid = int(data[0])
	elif cursorss.rowcount > 1:
		print 'Multiple matching records found for title id.  Using the most recent'
		data = cursorss.fetchone()
		sstitleid = int(data[0])
	else:
		data = cursorss.fetchone()
		sstitleid = int(data[0])
	return sstitleid

def writethumbnail(ssid,tmppath,ssrepopath,thumbnail,taskid,sstitleid,ssarchident):
	fileList=os.listdir(tmppath)
	if len(fileList) > 0:
		for file in fileList:
			os.remove(tmppath + file)
	ssthmbdir = ssrepopath + 'thmbs\\'
	thmbname = str(taskid) + '.jpg'  #Temporary for chksum calc then to be renamed with archident when the file is archived.  save arch reference in advance.
	if not os.path.exists(ssthmbdir):
		os.makedirs(ssthmbdir)
	fi = open(tmppath + thmbname, 'wb')
	fi.write(thumbnail.decode('base64'))
	fi.close()
	new_chksum = md5Checksum(tmppath + thmbname)
	sql = "SELECT ssthmbid FROM tblssthumbnails WHERE chksum=%s AND ssthmbname!=%s and sstitleid!=%s ORDER by ssthmbid ASC"
	args = (new_chksum,thmbname,sstitleid)
	cursorss.execute(sql,args)
	if cursorss.rowcount != 0:
		print 'Error:  Existing checksums found in db for ssthmbname:',ssthmbname,'sstitleid:',sstitleid
		data = cursorss.fetchall()
		for row in data:
			print row
	if os.path.isfile(ssthmbdir+thmbname):
		old_chksum = md5Checksum(ssthmbdir+thmbname)
		if new_chksum == old_chksum: #will use the previous file and copy the reference into a new record and delete the new file.
			os.remove(tmppath + thmbname)
			have_thumbnail = 1
			sql = "SELECT ssthmbid,ssarchident,compares,vis_verified FROM tblssthumbnails WHERE ssthmbname=%s AND chksum=%s AND sstitleid=%s ORDER by ssthmbid DESC"
			args = (thmbname,new_chksum, sstitleid)
			cursorss.execute(sql,args)
			if cursorss.rowcount == 0:
				print 'Error:  Missing original record definition for thmbname:',thmbname
				sql = "INSERT into tblssthumbnails (sstitleid,ssthmbname,ssarchident,chksum) VALUES (%s,%s,%s,%s)"
				args = (sstitleid,thmbname,ssarchident,new_chksum)
				cursorss.execute(sql,args)
				conss.commit()
			elif cursorss.rowcount > 1:
				print 'Error:  multiple thumbnail records found for thmbname:',thmbname,'Need to reconcile database'
				ssthmbid = 0
#			else: #  Have a current thumbnail record for the active sstitleid.  Don't need to do anything.
		else:  #will archive the previous file using the previous archident and copy in the new file and create a new reference.
			sql = "SELECT ssthmbid, ssarchident FROM tblssthumbnails WHERE ssthmbname=%s AND chksum=%s ORDER BY ssthmbid DESC"
			args = (thmbname,old_chksum)
			cursorss.execute(sql,args)
			if cursorss.rowcount ==0:
				print 'Error:  Unable to find tblssthumbnails entry for existing thumbnail:',thmbname,' Need to reconcile database'
			elif cursorss.rowcount > 1:
				print 'Error:  Multiple references found for thumbnail:', thmbname,'archident:',' Need to reconcile database'
			else:
				data = cursorss.fetchone()
				archident = data[1]
				basename, extension = os.path.splitext(thmbname)
				if not os.path.exists(ssthmbdir + "\\archive\\"):
					os.makedirs(ssthmbdir + "\\archive\\")
				shutil.move(ssthmbdir + thmbname, ssthmbdir + "\\archive\\" + basename + "_" + archident + extension)
				shutil.move(tmppath + thmbname, ssthmbdir + thmbname)
				sql = "INSERT into tblssthumbnails (sstitleid,ssthmbname,ssarchident,chksum) VALUES (%s,%s,%s,%s)"
				args = (sstitleid,thmbname,ssarchident,new_chksum)
				cursorss.execute(sql,args)
				conss.commit()
	else: #A previous version of the thumbnail does not exists.  copy in thumbnail and create a reference to it.
		shutil.move(tmppath + thmbname, ssthmbdir + thmbname)
		sql = "SELECT ssthmbid,ssarchident,compares,vis_verified FROM tblssthumbnails WHERE ssthmbname=%s AND chksum=%s AND sstitleid=%s ORDER by ssthmbid DESC"
		args = (thmbname,new_chksum, sstitleid)
		cursorss.execute(sql,args)
		if cursorss.rowcount == 0:
			sql = "INSERT into tblssthumbnails (sstitleid,ssthmbname,ssarchident,chksum) VALUES (%s,%s,%s,%s)"
			args = (sstitleid,thmbname,ssarchident,new_chksum)
			cursorss.execute(sql,args)
			conss.commit()			
		elif cursorss.rowcount > 1:
			print 'Error:  multiple thumbnail records found for thmbname:',thmbname,'Need to reconcile database'
		else:
			print 'Error:  An existing record was found for thmbname:',thmbname			
	sql = "UPDATE tblsstitles SET have_thumbnail=%s WHERE sstitleid=%s"
	args = (1,sstitleid)
	try:
		cursorss.execute(sql,args)
		conss.commit()
	except mdb.Error, e:
		print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
	print 'have_thumbnail:',1
				
def getBenchmarkId(sstitleid,bucketid,ssid):
	sql = "SELECT ssbmid FROM tblssbenchmarks WHERE sstitleid=%s AND bucketid=%s AND ssid=%s ORDER BY ssbmid DESC"
	args = (sstitleid,bucketid,ssid)
	cursorss.execute(sql,args)
	if cursorss.rowcount == 0:
		sql = "INSERT into tblssbenchmarks(sstitleid,bucketid,ssid) VALUES(%s,%s,%s)"
		args = (sstitleid,bucketid,ssid)
		cursorss.execute(sql,args)
		conss.commit()
		sql = "SELECT ssbmid FROM tblssbenchmarks WHERE sstitleid=%s AND bucketid=%s AND ssid=%s ORDER BY ssbmid DESC"
		args = (sstitleid,bucketid,ssid)
		cursorss.execute(sql,args)
		if cursorss.rowcount == 0:
			print 'Error creating benchmark record for sstitleid:',sstitleid,'bucketid:',bucketid,'ssid:',ssid
			ssbmid = 0
		elif cursorss.rowcount > 1:
			print 'Error: multiple benchmark records found for sstitleid:',sstitleid,'bucketid:',bucketid,'ssid:',ssid,' after first finding none'
			ssbmnid = 0
		else:
			data = cursorss.fetchone()
			ssbmid = int(data[0])
	elif cursorss.rowcount > 1:
		print 'multiple benchmark records found for sstitleid:',sstitleid,'bucketid:',bucketid,'ssid:',ssid,'  Using most recent'
		data = cursorss.fetchone()
		ssbmid = data[0]
	else:
		data = cursorss.fetchone()
		ssbmid = int(data[0])		
	return ssbmid			
	
def processscreenshots(ssbmid,sstitleid,tempzipdir,taskid,bucketid,sstype,ssdate,ssidentifier,ssrepopath,ssarchident):
	ssrepodir = ssrepopath + 'ScreenShots\\' + str(taskid) + '\\' + str(bucketid) + '\\'
	if not os.path.exists(ssrepodir):
		os.makedirs(ssrepodir)
	fileList=os.listdir(tempzipdir)
	fileList.sort()
	num_screenshots = 0
	if len(fileList) > 0:
		for file in fileList:
			basename, extension = os.path.splitext(file)
			new_chksum = md5Checksum(tempzipdir + file)
			sql = "SELECT ssssid FROM tblssscreenshots WHERE chksum=%s AND ssfilename!=%s and ssbmid!=%s ORDER by ssssid ASC"
			args = (new_chksum,file,ssbmid)
			cursorss.execute(sql,args)
			if cursorss.rowcount != 0:
				print 'Error:  Existing checksums found in db for screenshot:',file,'ssssid:',ssssid
				data = cursorss.fetchall()
				for row in data:
					print row
			if os.path.isfile(ssrepodir + file):
				old_chksum = md5Checksum(ssrepodir + file)
				if new_chksum == old_chksum:  #will use the previous file and copy the reference into a new record and delete the new file.
					os.remove(tempzipdir + file)
					sql = "SELECT ssssid,ssarchident,compares,vis_verified FROM tblssscreenshots WHERE ssfilename=%s AND chksum=%s AMD ssbmid=%s ORDER by ssssid DESC"
					args = (file,new_chksum,ssbmid)
					cursorss.execute(sql,args)
					if cursorss.rowcount == 0:
						print 'Error:  Missing original record definition for file:', file,'taskid:',taskid,'bucketid:',bucketid
						sql = "INSERT into tblssscreenshots (ssbmid,ssfilename,ssarchident,chksum) VALUES (%s,%s,%s,%s)"
						args = (ssbmid,file,ssarchident,new_chksum)
						cursorss.execute(sql,args)
						conss.commit()
						num_screenshots = num_screenshots + 1
					elif cursorss.rowcount > 1:
						print 'Error:  multiple screenshot records found for file:',file,'taskid:',taskid,'bucketid:',bucketid,'  Need to reconcile database'
						# May want to use latest for consistency.
#					else: #We already have one copy of this file with the correct reference.  Should we even get this such that an error is needed?
#						data = cursorss.fetchone()
#						p_ssarchident = data[1]
#						p_compares = data[2]
#						p_vis_verified = data[3]
#						sql = "INSERT into tblssscreenshots (ssbmid,ssfilename,ssarchident,chksum,compares,vis_verified) VALUES (%s,%s,%s,%s,%s,%s)"
#						args = (ssbmid,file,p_ssarchident,new_chksum,p_compares,p_vis_verified)
#						cursorss.execute(sql,args)
#						conss.commit()
#						num_screenshots = num_screenshots + 1
				else:	#will archive the previous file using the previous archident and copy in the new file and create a new reference.
					sql = "SELECT ssbmid,ssarchident FROM tblssscreenshots WHERE ssfilename=%s and chksum=%s ORDER by ssbmid DESC"
					args = (file,old_chksum)
					cursorss.execute(sql,args)
					if cursorss.rowcount == 0:
						print 'Error:  Unable to find screenshot entry for existing file:',file,'taskid:',taskid,'bucketid:',bucketid,' Need to reconcile database'
					elif cursorss.rowcount > 1:
						print 'Error:  Multiple references found for screenshot file:',file,'ssarchident:',ssarchident,'  Need to reconcile database'
						# May want to use latest for consistency.
					else:
						data = cursorss.fetchone()
						archident = data[1]
						if not os.path.exists(ssrepodir + "\\archive\\"):
							os.makedirs(ssrepodir + "\\archive\\")
						shutil.move(ssrepodir + file, ssrepodir + "\\archive\\" + basename + "_" + archident + extension)
						shutil.move(tempzipdir + file, ssrepodir + file)
						sql = "INSERT into tblssscreenshots (ssbmid,ssfilename,ssarchident,chksum) VALUES (%s,%s,%s,%s)"
						args = (ssbmid,file,ssarchident,new_chksum)
						cursorss.execute(sql,args)
						conss.commit()						
						num_screenshots = num_screenshots + 1
			else:	# A previous version of the screenshot does not exists.  Copy in the screenshot and create a reference to it.
				shutil.move(tempzipdir + file, ssrepodir + file)
				sql = "INSERT into tblssscreenshots (ssbmid,ssfilename,ssarchident,chksum) VALUES (%s,%s,%s,%s)"
				args = (ssbmid,file,ssarchident,new_chksum)
				cursorss.execute(sql,args)
				conss.commit()						
				num_screenshots = num_screenshots + 1			
	else:
		print 'No screenshots found for taskid:',taskid,' bucketid:',bucketid
	if num_screenshots > 1:
		sql = "UPDATE tblssbenchmarks SET num_screenshots=%s WHERE ssbmid=%s"
		args = (num_screenshots,ssbmid)
		try:
			cursorss.execute(sql,args)
			conss.commit()
		except mdb.Error, e:
			print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])	
		sql = "UPDATE tblsstitles SET have_screenshot=%s WHERE sstitleid=%s"
		args = (1,sstitleid)
		try:
			cursorss.execute(sql,args)
			conss.commit()
		except mdb.Error, e:
			print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
	return num_screenshots

def processconfigs(ssbmid,sstitleid,tempzipdir,ssrepopath,ssarchident,taskid):	
	fileList=os.listdir(tempzipdir)
	fileList.sort()
	if len(fileList) > 0:
		num_configs = 0
		for file in fileList:
			filename, tmpstr = file.split('__')
			gameid, hwgroup, itr = tmpstr.split('_')
			shutil.move(tempzipdir + file, tempzipdir + filename)
			basename, extension = os.path.splitext(filename)
			ssrepodir = ssrepopath + 'Configs\\' + str(taskid) + '\\' + str(hwgroup) + '\\'
			bucketid = hwgroup
			if not os.path.exists(ssrepodir):
				os.makedirs(ssrepodir)
			new_chksum = md5Checksum(tempzipdir + filename)
			sql = "SELECT sscfgid FROM tblssconfigs WHERE chksum=%s AND configfilename!=%s and ssbmid!=%s ORDER by sscfgid ASC"
			args = (new_chksum,filename,ssbmid)
			cursorss.execute(sql,args)
			if cursorss.rowcount != 0:
				print 'Error:  Existing checksums found in db for configfilename:',filename,'sscfgid:',sscfgid
				data = cursorss.fetchall()
				for row in data:
					print row
			if os.path.isfile(ssrepodir + filename):
				old_chksum = md5Checksum(ssrepodir + filename)
				if new_chksum == old_chksum:  #Will us the previous file and copy the reference into a new record and delete the new file
					os.remove(tempzipdir + filename)
					sql = "SELECT sscfgid,ssarchident,compares,vis_verified FROM tblssconfigs WHERE configfilename=%s AND chksum=%s AND ssbmid=%s ORDER by sscfgid DESC"
					args = (filename,new_chksum,ssbmid)
					cursorss.execute(sql,args)
					if cursorss.rowcount == 0:
						print 'Error:  Missing original record definition for configfilename:',filename,'taskid:',taskid,'bucketid:',bucketid
						sql = "INSERT into tblssconfigs (ssbmid,configfilename,ssarchident,chksum) VALUES (%s,%s,%s,%s)"
						args = (ssbmid,filename,ssarchident,new_chksum)
						cursorss.execute(sql,args)
						conss.commit()
						num_configs = num_configs + 1
					elif cursorss.rowcount > 1:
						print 'Error:  multiple config records found for configfilename:',filename,'taskid:',taskid,'bucketid:',bucketid,'Need to reconcile database'
						# May want to use latest for consistency.
	#				else:  #We already have a correct reference.  Don't need to do anything.  Should this raise an error?
	#					data = cursorss.fetchone()
	#					p_ssarchident = data[1]
	#					p_compares = data[2]
	#					p_vis_verified = data[3]
	#					sql = "INSERT into tblssconfigs (ssbmid,configfilename,ssarchident,chksum,compares,vis_verified) VALUES (%s,%s,%s,%s,%s,%s)"
	#					args = (ssbmid,filename,p_ssarchident,new_chksum,p_compares,p_vis_verified)
	#					cursorss.execute(sql,args)
	#					conss.commit()
	#					num_configs = num_configs + 1
				else:  #Will archive the previous file using the previous archident and copy in the new file and create a new references
					sql = "SELECT ssbmid, ssarchident FROM tblssconfigs WHERE configfilename=%s AND chksum=%s ORDER by ssbmid DESC"
					args = (filename,old_chksum)
					cursorss.execute(sql,args)
					if cursorss.rowcount == 0:
						print 'Error:  Unable to find record for existing config filename:',filename,'taskid:',taskid,'bucketid:',bucketid
					elif cursorss.rowcount > 1:
						print 'Error: Multiple references found for config filename:',filename,'taskid:',taskid,'bucketid:',bucketid, 'Need to reconcile database'
						# may want to use latest for consistency
					else:
						data = cursorss.fetchone()
						archident = data[1]
						if not os.path.exists(ssrepodir + "\\archive\\"):
							os.makedirs(ssrepodir + "\\archive\\")
						shutil.move(ssrepodir + filename, ssrepodir + "\\archive\\" + basename + "_" + archident + extension)
						shutil.move(tempzipdir + filename, ssrepodir + filename)
						sql = "INSERT into tblssconfigs (ssbmid,configfilename,ssarchident,chksum) VALUES (%s,%s,%s,%s)"
						args = (ssbmid,filename,ssarchident,new_chksum)
						cursorss.execute(sql,args)
						conss.commit()
						num_configs = num_configs + 1
			else:  # A previous version of the configuration file does not exist.  Copy in the config file and create a reference to it
				shutil.move(tempzipdir + filename, ssrepodir + filename)
				sql = "INSERT into tblssconfigs (ssbmid,configfilename,ssarchident,chksum) VALUES (%s,%s,%s,%s)"
				args = (ssbmid,filename,ssarchident,new_chksum)
				cursorss.execute(sql,args)
				conss.commit()
				num_configs = num_configs + 1				
	else:
		print 'No configuration files found for taskid:',taskid,'bucketid:',bucketid
	if num_configs > 0:
		sql = "UPDATE tblssbenchmarks SET num_configs=%s WHERE ssbmid=%s"
		args = (num_configs,ssbmid)
		try:
			cursorss.execute(sql,args)
			conss.commit()
		except mdb.Error, e:
			print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
		sql = "UPDATE tblsstitles SET have_configs=%s WHERE sstitleid=%s"
		args = (1,sstitleid)
		try:
			cursorss.execute(sql,args)
			conss.commit()
		except mdb.Error, e:
			print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])			
	return num_configs
