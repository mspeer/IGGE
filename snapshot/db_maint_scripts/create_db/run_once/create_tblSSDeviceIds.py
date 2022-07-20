import MySQLdb as mdb
from db_funcs import getssdbcon


con = getssdbcon('tblSSDeviceIds')
with con:
	cur = con.cursor()
	cur.execute('DROP TABLE IF EXISTS tblssdeviceids')
	cur.execute('CREATE TABLE tblssdeviceids (SSDId INT PRIMARY KEY AUTO_INCREMENT, \
			ssid INT, \
			bucketid INT, \
			deviceid VARCHAR(50), \
			compares BOOLEAN default 0)')
cur.close()
con.close()
print 'Hit return to exit'
raw_input()
