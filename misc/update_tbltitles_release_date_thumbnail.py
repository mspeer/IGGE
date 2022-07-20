import pyodbc, os, base64
from io import BytesIO
from PIL import Image
cnxn = pyodbc.connect('DSN=DashBoard')
cursor = cnxn.cursor()

path = "D:\Projects\IGGE\python_scripts\media"
filename = "output.jpg"


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
cursor.execute("select TOP 10 TaskGuid, TaskName, BucketId, BucketName, DeviceId, GraphicsBrand, FinishedDate, ReleaseDate from GswsResults;")
data = cursor.fetchall()
for row in data:
	print row
