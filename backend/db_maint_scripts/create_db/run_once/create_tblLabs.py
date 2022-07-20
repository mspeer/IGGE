import MySQLdb as mdb

from db_funcs import getssdbcon


con = getssdbcon()

with con:
	try:
		cur = con.cursor()
		cur.execute('DROP TABLE IF EXISTS tblLabs')
		cur.execute('CREATE TABLE tblLabs (labID INT PRIMARY KEY AUTO_INCREMENT, \
				labName VARCHAR(25), \
				vcFileShare VARCHAR(256), \
				localFileShare VARCHAR(256), \
				active	BOOLEAN not null default 0, \
				comment VARCHAR(512))')
		print 'Execution complete'
	except:
		print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
cur.close()
con.close()
print 'Hit return to exit'
raw_input()
