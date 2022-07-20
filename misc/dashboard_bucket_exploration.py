import pyodbc, os, base64
from io import BytesIO
from PIL import Image
import unicodedata
cnxn = pyodbc.connect('DSN=DashBoard')
cursor = cnxn.cursor()

cursor.execute("select DISTINCT BucketId,BucketName,DeviceId,GraphicsBrand from GswsResults")
rows = cursor.fetchall()
print "bucketid","bucketname","deviceid","graphicsbrand"
for row in rows:
	bucketid = row[0]
	bucketname = row[1]
	deviceid = row[2]
	graphicsbrand = unicodedata.normalize('NFKD',row[3]).encode('ascii','ignore')
	print bucketid,bucketname,deviceid,graphicsbrand
