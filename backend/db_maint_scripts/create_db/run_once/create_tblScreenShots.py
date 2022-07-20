import MySQLdb as mdb

from db_funcs import getssdbcon


con = getssdbcon()

with con:
	try:
		cur = con.cursor()
		cur.execute('DROP TABLE IF EXISTS tblScreenShots')
		cur.execute('CREATE TABLE tblScreenShots (id INT PRIMARY KEY AUTO_INCREMENT, \
				benchmarkID INT, \
				filename VARCHAR(128), \
				chksum VARCHAR(32), \
				vis_verified BOOLEAN default null, \
				Hdim INT, \
				Vdim INT, \
				language VARCHAR(25), \
				comment VARCHAR(512))')
		print 'Execution complete'
	except:
		print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
cur.close()
con.close()
print 'Hit return to exit'
raw_input()
