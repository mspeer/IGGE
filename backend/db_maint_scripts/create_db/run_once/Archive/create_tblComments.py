import MySQLdb as mdb
con = mdb.connect('localhost', 'root', '_PW_', 'iggeqadb');
with con:
	cur = con.cursor()
	cur.execute('DROP TABLE IF EXISTS tblComments')
	cur.execute('CREATE TABLE tblComments (commentID INT PRIMARY KEY AUTO_INCREMENT, \
			dt TIMESTAMP, \
			source_tbl VARCHAR(25), \
			source_id	INT, \
			comment VARCHAR(512))')
