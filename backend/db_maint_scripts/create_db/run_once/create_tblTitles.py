import MySQLdb as mdb

from db_funcs import getssdbcon


con = getssdbcon()

with con:
	try:
		cur = con.cursor()
		cur.execute('DROP TABLE IF EXISTS tblTitles')
		cur.execute('CREATE TABLE tblTitles (titleID INT PRIMARY KEY AUTO_INCREMENT, \
				name VARCHAR(64), \
				alias VARCHAR(64), \
				taskguid VARCHAR(36), \
				salesforceid VARCHAR(25), \
				finisheddate VARCHAR(30), \
				releasedate VARCHAR(30), \
				gameID INT, \
				rank INT, \
				gsws_goal BOOLEAN not null default 0, \
				raptr_goal BOOLEAN not null default 0, \
				have_thumbnail BOOLEAN not null default 0, \
				thmb_chksum VARCHAR(32), \
				thmb_vis_verified BOOLEAN default null, \
				comment VARCHAR(512))')
		print 'Execution complete'
	except:
		print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
cur.close()
con.close()
print 'Hit return to exit'
raw_input()
