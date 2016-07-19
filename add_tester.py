#!/usr/bin/python

# IMPORTS:
import cgi
import cgitb
cgitb.enable()

import base, settings
from connect import connect
# :IMPORTS

# FUNCTIONS:
def main():
	# Arguments:
	form = cgi.FieldStorage()
	tester_name = form.getvalue("testerName")
	db = settings.get_db()
	
	# Begin:
	base.begin()
	base.header(title='{0}: add tester'.format(db))
        base.header_redirect("testers.py?db={0}".format(db))
        base.top(db)
	
	# Connect to DB:
	con = connect(True, db)
	cur = con.cursor(buffered=True)
	
	#print "INSERT INTO people (person_name, person_id) VALUES ('{0}',{1})".format(testerName,testerID)
	if tester_name:
		cur.execute("INSERT INTO People (person_name) VALUES ('{0}')".format(tester_name))
		con.commit()
		con.close()
	else:
		print "ERROR: null tester name submitted. Database not updated."
	
	base.bottom()
# :FUNCTIONS

# MAIN:
if __name__ == "__main__":
	main()
# :MAIN

