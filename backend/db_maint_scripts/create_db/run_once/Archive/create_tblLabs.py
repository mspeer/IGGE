import MySQLdb as mdb
con = mdb.connect('localhost', 'root', '_PW_', 'iggeqadb');
with con:
	cur = con.cursor()
	cur.execute('DROP TABLE IF EXISTS tblLabs')
	cur.execute('CREATE TABLE tblLabs (labID INT PRIMARY KEY AUTO_INCREMENT, \
			labName VARCHAR(25), \
			vcFileShare VARCHAR(256), \
			localFileShare VARCHAR(256), \
			active	BOOLEAN not null default 0, \
			comment VARCHAR(512))')
