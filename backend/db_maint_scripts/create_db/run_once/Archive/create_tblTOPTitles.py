import MySQLdb as mdb
con = mdb.connect('localhost', 'root', '_PW_', 'iggeqadb');
with con:
	cur = con.cursor()
	cur.execute('DROP TABLE IF EXISTS tblTitles')
	cur.execute('CREATE TABLE tblTOPTitles (topID INT PRIMARY KEY AUTO_INCREMENT, \
			titleID INT, \
			rank VARCHAR(25), \
			alias VARCHAR(64), \
			comment VARCHAR(512))')
