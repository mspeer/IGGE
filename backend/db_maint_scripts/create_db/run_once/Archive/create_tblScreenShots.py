import MySQLdb as mdb
con = mdb.connect('localhost', 'root', '_PW_', 'iggeqadb');
with con:
	cur = con.cursor()
	cur.execute('DROP TABLE IF EXISTS tblScreenShots')
	cur.execute('CREATE TABLE tblScreenShots (ssID INT PRIMARY KEY AUTO_INCREMENT, \
			benchmarkID INT, \
			ssFilename VARCHAR(128), \
			chksum VARCHAR(32), \
			vis_verified BOOLEAN not null default 0, \
			dimensions VARCHAR(25), \
			language VARCHAR(25), \
			comment VARCHAR(512))')
