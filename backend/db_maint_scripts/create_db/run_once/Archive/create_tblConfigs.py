import MySQLdb as mdb
con = mdb.connect('localhost', 'root', '_PW_', 'iggeqadb');
with con:
	cur = con.cursor()
	cur.execute('DROP TABLE IF EXISTS tblConfigs')
	cur.execute('CREATE TABLE tblConfigs (configID INT PRIMARY KEY AUTO_INCREMENT, \
			benchmarkID INT, \
			configFileName VARCHAR(128), \
			chksum VARCHAR(32), \
			vis_verified BOOLEAN not null default 0, \
			language VARCHAR(25), \
			comment VARCHAR(512))')
