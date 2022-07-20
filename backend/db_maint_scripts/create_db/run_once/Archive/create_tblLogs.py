import MySQLdb as mdb
con = mdb.connect('localhost', 'root', '_PW_', 'iggeqadb');
with con:
	cur = con.cursor()
	cur.execute('DROP TABLE IF EXISTS tblLogs')
	cur.execute('CREATE TABLE tblLogs (logID INT PRIMARY KEY AUTO_INCREMENT, \
			dt TIMESTAMP, \
			logentry VARCHAR(512))')
