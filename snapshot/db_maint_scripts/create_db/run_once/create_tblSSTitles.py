import MySQLdb as mdb
from db_funcs import getssdbcon


con = getssdbcon('tblSSTitles')
with con:
	cur = con.cursor()
	cur.execute('DROP TABLE IF EXISTS tblsstitles')
	cur.execute('CREATE TABLE tblsstitles (sstitleid INT PRIMARY KEY AUTO_INCREMENT, \
			ssid INT, \
			name varchar(255), \
			taskid	INT, \
			rank INT, \
			finisheddate VARCHAR(30), \
			releasedate VARCHAR(30), \
			salesforceid VARCHAR(50), \
			have_thumbnail BOOLEAN default 0, \
			have_screenshot BOOLEAN default 0, \
			have_configs BOOLEAN default 0, \
			compares BOOLEAN default 0)')
cur.close()
con.close()
print 'Hit return to exit'
raw_input()
