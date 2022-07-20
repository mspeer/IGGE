import MySQLdb as mdb
from db_funcs import getssdbcon


con = getssdbcon('tblSSScreenShots')
with con:
	cur = con.cursor()
	cur.execute('DROP TABLE IF EXISTS tblssscreenshots')
	cur.execute('CREATE TABLE tblssscreenshots (SSSSId INT PRIMARY KEY AUTO_INCREMENT, \
			ssbmid INT, \
			ssfilename VARCHAR(128), \
			ssarchident VARCHAR(25), \
			chksum VARCHAR(32), \
			compares BOOLEAN default 0, \
			vis_verified BOOLEAN default 0)')
cur.close()
con.close()
print 'Hit return to exit'
raw_input()
