import MySQLdb as mdb
con = mdb.connect('localhost', 'root', '_PW_', 'iggeqadb');
with con:
	cur = con.cursor()
	cur.execute('DROP TABLE IF EXISTS tblDeviceIds')
	cur.execute('CREATE TABLE tblDeviceIds (deviceIdid INT PRIMARY KEY AUTO_INCREMENT, \
			deviceId VARCHAR(25), \
			graphicsbrand VARCHAR(64), \
			comment VARCHAR(512))')
