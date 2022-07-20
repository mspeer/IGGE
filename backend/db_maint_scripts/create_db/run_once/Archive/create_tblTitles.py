import MySQLdb as mdb
con = mdb.connect('localhost', 'root', '_PW_', 'iggeqadb');
with con:
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
			thmb_vis_verified BOOLEAN not null default 0, \
			comment VARCHAR(512))')
