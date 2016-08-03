#!/usr/bin/python

# IMPORTS:
import cgi, sys
import cgitb
cgitb.enable()

import base, settings
from connect import connect
# :IMPORTS

# FUNCTIONS:
def main():
	# Arguments:
	form = cgi.FieldStorage()
	testtype_name = form.getvalue("testName")
	testtype_short = form.getvalue("descShort")
	testtype_long = form.getvalue("descLong")
	testtype_req = (False, True)[bool(form.getvalue("required"))]
	db = settings.get_db()
	
	# Begin:
	base.begin()
	base.header_redirect("erudition.py?db={0}".format(db),1)
	base.top(db)
	
	# Insert:
	con = connect(True, db)
	cur = con.cursor()
	if testtype_name and testtype_long:
		cur.execute("INSERT INTO Test_Type (name, required, desc_short, desc_long, relative_order) VALUES ('{0}', {1}, '{2}', '{3}', 1);".format(testtype_name, int(testtype_req), testtype_short, testtype_long))
		con.commit()
		con.close()

	else:
		print '<center><h3 style="color:red"><i> ERROR: Null test type or test type description provided. Please input again.</i></h3></center>'

	base.bottom()
# :FUNCTIONS

# MAIN:
if __name__ == "__main__":
	main()
# :MAIN


