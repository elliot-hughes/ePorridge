#!/usr/bin/python

# IMPORTS:
import cgitb
cgitb.enable()
import cgi

import base, settings
from connect import connect
import mysql.connector
import module_functions
# :IMPORTS

# FUNCTIONS:
def fetch_user_info(db):
	# Connect to DB:
	con = connect(False, db)
	cur = con.cursor()
	
	# Fetch from DB:
	cur.execute("SELECT person_name, person_id FROM People")
	rows = cur.fetchall()
	
	# Return
	return [{'name': user[0], 'id': user[1]} for user in rows]


def main():
	db = settings.get_db()
	
	base.begin()
	base.header(title='{0}: testers'.format(db))
	base.top(db)
	
	
	print '<div class="row">'
	print    '<div class="col-md-12">'
	print        '<table class="table" style="width:650px" align="center">'
	print                '<tr>'
	print                    '<th > Name </th>'
	print                    '<th > ID </th>'
	print                '</tr>'
	userInfo = fetch_user_info(db)
	for user in userInfo:

		print '<tr>'
		print '<td align="left">',user['name'],'</td>'
		print '<td align="left">',user['id'],'</td>'
		print '</tr>'

	print         '</table>'
	print    '</div>'
	print '</div>'

	print '<br><br>'
	print '<form action="add_tester.py?db={0}" method="post" enctype="multipart/form-data">'.format(db)
	print '\t<div class="col-md-6">'
	print '\t\t<b>Add tester</b><br>'
	print '\t\ttester name:<br>'
	print '\t\t<textarea name="testerName" cols="35" rows="1"></textarea><br>'
	print '\t\t<input type="submit" value="Submit">'
	print '\t</div>'
	print '</form>'

	base.bottom()
# :FUNCTIONS

# MAIN:
if __name__ == "__main__":
	main()
# :MAIN
