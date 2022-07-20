import MySQLdb as mdb

from db_funcs import getssdbcon


con = getssdbcon()

with con:
	try:
		cur = con.cursor()
		cur.execute('DROP TABLE IF EXISTS tblBenchmarks')
		cur.execute('CREATE TABLE tblBenchmarks (benchmarkID INT PRIMARY KEY AUTO_INCREMENT, \
				titleID INT, \
				gameID VARCHAR(25), \
				platformID INT, \
				labID INT, \
				bucketid VARCHAR(25), \
				bucketname VARCHAR(25), \
				num_configs INT, \
				num_screenshots INT, \
				status VARCHAR(25), \
				recommendedresolution VARCHAR(25), \
				recommendedrootpath VARCHAR(255), \
				comment VARCHAR(512))')
		print 'Execution complete'
	except:
		print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
cur.close()
con.close()
print 'Hit return to exit'
raw_input()
