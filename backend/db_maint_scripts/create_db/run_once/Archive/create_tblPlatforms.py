import MySQLdb as mdb
con = mdb.connect('localhost', 'root', '_PW_', 'iggeqadb');
with con:
	cur = con.cursor()
	cur.execute('DROP TABLE IF EXISTS tblPlatforms')
	cur.execute('CREATE TABLE tblPlatforms (platformID INT PRIMARY KEY AUTO_INCREMENT, \
			description VARCHAR(25), \
			bucketID VARCHAR(25), \
			bucketName VARCHAR(25), \
			comment VARCHAR(512))')
