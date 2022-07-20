import MySQLdb as mdb
con = mdb.connect('localhost', 'root', '_PW_', 'iggeqadb');
with con:
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
			recommendedrootpath VARCHAR(255), \
			comment VARCHAR(512))')
