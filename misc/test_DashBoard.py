import pyodbc, os, base64
from io import BytesIO
from PIL import Image
import unicodedata
cnxn = pyodbc.connect('DSN=DashBoard')
cursor = cnxn.cursor()

#path = "D:\Projects\IGGE\python_scripts\media"
#filename = "output.jpg"


#cursor.execute("select DeviceId from GswsResults")
#rows = cursor.fetchall()
#for row in rows:
#	print row
#cursor.execute("select TaskGuid,TaskName, SalesForceID, BucketId, BucketName, DeviceId, GraphicsBrand, RecommendedRootPath, FinishedDate, ReleaseDate from GswsResults")
#row = cursor.fetchone()
#if row:
#	print row
#cursor.execute("select Thumbnail from GswsResults")
#data = cursor.fetchone()
#if row:
#	print row[0]
#	png_recovered = base64.decodestring(data[1])
#	fh = open(filename, "w")
#	fh.write(png_recovered)
#	fh.close()
#if data:
#	im = Image.open(BytesIO(base64.b64decode(data)))
#	im.save('output.jpg','jpeg')
#cursor.execute("select distinct(RecommendedRootPath) AS recommendedpath FROM GswsResults ORDER BY recommendedpath DESC;")
cursor.execute("select TOP 1000 TaskId,TaskGuid,TaskName,SalesForceID,BucketId,BucketName,DeviceId,GraphicsBrand,RecommendedRootPath,FinishedDate,ReleaseDate from GswsResults")
rows = cursor.fetchall()
print "taskid","taskname","bucketid","bucketname","deviceid","graphicsbrand","recommendedrootpath"
for row in rows:
	taskid = row[0]
	taskGUID = row[1]
	taskname = row[2]
	salesforceid = row[3]
	bucketid = row[4]
	bucketname = row[5]
	deviceid = row[6]
	graphicsbrand = unicodedata.normalize('NFKD',row[7]).encode('ascii','ignore')
	recommendedrootpath = row[8]
	finisheddate = row[9]
	releasedate = row[10]
	print taskid,taskname,bucketid,bucketname,deviceid,graphicsbrand,recommendedrootpath
