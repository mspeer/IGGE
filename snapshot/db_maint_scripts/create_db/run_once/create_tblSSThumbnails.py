import MySQLdb as mdb
from db_funcs import getssdbcon


con = getssdbcon('tblSSThumbnails')
with con:
	cur = con.cursor()
	cur.execute('DROP TABLE IF EXISTS tblssthumbnails')
	cur.execute('CREATE TABLE tblssthumbnails (SSTHMBId INT PRIMARY KEY AUTO_INCREMENT, \
			sstitleid INT, \
			ssthmbname varchar(25), \
			ssarchident varchar(25), \
			chksum varchar(32), \
			compares BOOLEAN, \
			vis_verified BOOLEAN)')
cur.close()
con.close()
print 'Hit return to exit'
raw_input()
