import MySQLdb as mdb
from db_funcs import getssdbcon


con = getssdbcon('tblSSBenchmarks')

with con:
	cur = con.cursor()
	cur.execute('DROP TABLE IF EXISTS tblssbenchmarks')
	cur.execute('CREATE TABLE tblssbenchmarks (SSBMId INT PRIMARY KEY AUTO_INCREMENT, \
			ssid INT, \
			sstitleid INT, \
			bucketid INT, \
			num_screenshots INT default 0, \
			num_configs INT default 0, \
			compares BOOLEAN default 0)')
cur.close()
con.close()
print 'Hit return to exit'
raw_input()
