import MySQLdb as mdb
from db_funcs import getssdbcon


con = getssdbcon('tblSnapshots')
with con:
	cur = con.cursor()
	cur.execute('DROP TABLE IF EXISTS tblSnapshots')
	cur.execute('CREATE TABLE tblSnapshots (SSId INT PRIMARY KEY AUTO_INCREMENT, \
			ssdate VARCHAR(8), \
			ssidentifier VARCHAR(25), \
			sstype VARCHAR(25), \
			ssarchident VARCHAR(25))')
cur.close()
con.close()
print 'Hit return to exit'
raw_input()
