import MySQLdb as mdb
from db_funcs import getssdbcon


con = getssdbcon()
with con:
	try:
		cur = con.cursor()
		cur.execute('DROP TABLE IF EXISTS tblDeviceIds')
		cur.execute('CREATE TABLE tblDeviceIds (deviceIdid INT PRIMARY KEY AUTO_INCREMENT, \
				deviceId VARCHAR(25), \
				graphicsbrand VARCHAR(64), \
				comment VARCHAR(512))')
		print 'Execution complete'
	except:
		print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
cur.close()
con.close()
print 'Hit return to exit'
raw_input()
