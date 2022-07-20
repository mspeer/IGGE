import MySQLdb as mdb

from db_funcs import getssdbcon


con = getssdbcon()

with con:
	try:
		cur = con.cursor()
		cur.execute('DROP TABLE IF EXISTS tblTOPTitles')
		cur.execute('CREATE TABLE tblTOPTitles (topID INT PRIMARY KEY AUTO_INCREMENT, \
				titleID INT, \
				rank VARCHAR(25), \
				alias VARCHAR(64), \
				comment VARCHAR(512))')
		print 'Execution complete'
	except:
		print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
cur.close()
con.close()
print 'Hit return to exit'
raw_input()
