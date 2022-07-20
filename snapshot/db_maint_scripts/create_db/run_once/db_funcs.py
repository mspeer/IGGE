import sys
import MySQLdb as mdb

def getssdbcon(table):
	if len(sys.argv) == 1:
		print 'Create ' + table
		print 'Choose environment:\n'
		print '1) Development\n'
		print '2) Test\n'
		print '3) Production\n'
		u_in = raw_input("Enter 1, 2 or 3 (or q to quit): ")
		while u_in not in ['1','2','3','q']:
			print "Invalid Entry"
			u_in = raw_input("Enter 1, 2 or 3 (or q to quit): ")
	elif len(sys.argv) == 2:
		if str(sys.argv[1]) not in ['1','2','3','q']:
			print "Invalid commandline argument passed.  Valid entries are 1,2,3 or q.  Please check calling function:",str(sys.argv[0])
			print 'Hit return to exit'
			raw_input()
		else:
			u_in = str(sys.argv[1])	
	else:
		print "Invalid use of commandline arguments.  Valid entries are 1,2,3 or q.  Please check calling function:",str(sys.argv[0])
		print 'Hit return to exit'
		raw_input()
		sys.exit()
	if u_in == '1':
		con = mdb.connect('localhost', 'root', '_PW_', 'iggessdbdev');	
	elif u_in == '2':
		con = mdb.connect('localhost', 'root', '_PW_', 'iggessdbtst');
	elif u_in == '3':
		confirm = raw_input("This will result in loss of all data in Production database.  Proceed? (Y/N): ")
		while confirm not in ['Y','N']:
			confirm = raw_input("Y or N")
		if confirm == 'Y':
			con = mdb.connect('localhost', 'root', '_PW_', 'iggessdbprd');
		else:
			print 'Operation canceled.  Exiting program'
			print 'Hit return to exit'
			raw_input()
			sys.exit()
	elif u_in == 'q':
		print 'Operation canceled'
		print 'Hit return to exit'
		raw_input()
		sys.exit()
	else:
		print 'Invalid entry'
		print 'Hit return to exit'
		raw_input()
		sys.exit()		
	return con
