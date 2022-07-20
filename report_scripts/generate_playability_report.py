import os, glob, re, shutil, hashlib, csv
import MySQLdb as mdb
from numpy import genfromtxt
import datetime

con = mdb.connect('localhost','root','_PW_','iggeqadb')
cursor = con.cursor()

dtstart =  str(datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S"))
report = 'D:\\Projects\\IGGE\\summaries\\playability_summary_' + dtstart + '.txt'
outfile = open( report, 'a' )

sql = "select description from tblplatforms order by displayorder asc"
platforms=[]
dict = {}
try:
	cursor.execute(sql)
	con.commit()
except mdb.Error, e:
	print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
for data in cursor:
	platforms.append(data[0])
	dict[data[0]] = 0

outstring = []
outstring.append('name')
outstring.append('rank')
outstring.append('releasedate')
outstring.append('taskId')
outstring.append('thmb')
for platform in platforms:
	outstring.append(platform)
outstring.append('\n')
outfile.write( '|'.join(outstring) )
	
sql = "SELECT distinct tbltitles.name, tbltitles.rank, tbltitles.releasedate, tbltitles.gameID, tbltitles.have_thumbnail \
	FROM tblbenchmarks  \
		JOIN tblTitles ON tblbenchmarks.gameID = tblTitles.gameID \
        JOIN tblPlatforms ON tblbenchmarks.platformID = tblPlatforms.platformID \
        JOIN tblScreenshots ON tblbenchmarks.benchmarkID = tblScreenshots.benchmarkID \
        /*WHERE rank IS NOT NULL*/  ORDER BY rank ASC"
		
try:
	cursor.execute(sql)
	con.commit()
except mdb.Error, e:
	print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
t = 0
for data in cursor:
	t = t + 1
	outstring = []	
	title_name = data[0]
	title_rank = data[1]
	title_releasedate = data[2]
	title_gameid = data[3]
	title_have_thumbnail = data[4]
	outstring.append(title_name)
	outstring.append(str(title_rank))
	outstring.append(title_releasedate)
	outstring.append(str(title_gameid))
	outstring.append(str(title_have_thumbnail))
	for platform in platforms:
		sql = "SELECT distinct tblplatforms.description, tblbenchmarks.benchmarkID, tblbenchmarks.num_screenshots, tblbenchmarks.num_configs, tblbenchmarks.recommendedrootpath \
			FROM tblbenchmarks \
			JOIN tblTitles ON tblbenchmarks.gameID = tblTitles.gameID \
			JOIN tblPlatforms ON tblbenchmarks.platformID = tblPlatforms.platformID \
			WHERE tblplatforms.description = %s AND tbltitles.gameID = %s"
		args = (platform, title_gameid)
		try:
			cursor.execute(sql,args)
			con.commit()
		except mdb.Error, e:
			print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
		for data in cursor:
			platform_description = data[0]
			benchmark_benchmarkID = data[1]
			benchmark_num_screenshots = data[2]
			benchmark_num_configs = data[3]
			benchmark_rrp = data[4]
			dict[platform_description] = benchmark_num_screenshots	
	for platform in platforms:
		outstring.append(str(dict[platform]))
	outstring.append('\n')
	outfile.write( '|'.join(outstring) )
	for key in dict:
		dict[key] = 0

print 'Total Number of Titles:', str(t)
outfile.close


