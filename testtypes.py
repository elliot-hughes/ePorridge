#!/usr/bin/python

# IMPORTS:
import cgi
import cgitb
cgitb.enable()

import base, settings
from connect import connect
import module_functions
# :IMPORTS

# FUNCTIONS:
def fetch_test_info(db):
	# Connect to DB:
	con = connect(False, db)
	cur = con.cursor()
	
	# Fetch from DB:
	cur.execute("SELECT name, desc_long, required, relative_order FROM Test_Type")
	rows = cur.fetchall()
	
	# Return:
	return sorted([{'name':test[0], 'desc':test[1], 'req':test[2], "order":test[3]} for test in rows], key=lambda k: k["order"])


def main():
	db = settings.get_db()
	
	base.begin()
	base.header(title='{0}: tests'.format(db))
	base.top(db)

	print '<div class="row">'
	print    '<div class="col-md-12">'
	print        '<table class="table" style="width:100%">'
	print            '<tbody>'
	print                '<tr>'
	print                    '<th> Name </th>'
	print                    '<th> Description </th>'
	print                    '<th> Required? </th>'
	print                '</tr>'
	testInfo = fetch_test_info(db)
	for test in testInfo:

		print '<tr align=left>'
		print u'<td>{0}</td>'.format(test['name']).encode('utf-8')
		print u'<td>{0}</td>'.format(test['desc']).encode('utf-8')
		if test['req'] == 0 :
			print '<td>no</td>'
		else:
			print '<td>yes</td>'
		print '</tr>'

	print            '</tbody>'
	print         '</table>'
	print    '</div>'
	print '</div>'

	print '<br><br>'
	print '<form action="add_testtype.py?db={0}" method="post" enctype="multipart/form-data">'.format(db)
	print '\t<div class="col-md-6">'
	print '\t\t<b>Add test type:</b><br>'
	print '\t\tName:<br>'
	print '\t\t<input type="text" name="testName"><br><br>'
	print '\t\tDescribe the test in brief:<br>'
	print '\t\t<textarea name="descShort" rows="5" cols="50"></textarea><br><br>'
	print '\t\tDescribe the test at length:<br>'
	print '\t\t<textarea name="descLong" rows="5" cols="100"></textarea><br><br>'
	print '\t\t<input type="checkbox" name="required" checked="checked">Required<br><br>'
	print '\t\t<input type="submit" value="Submit"><br><br>'
	print '\t</div>'
	print '</form>'

	base.bottom()
# :FUNCTIONS

# MAIN:
if __name__ == "__main__":
	main()
# :MAIN
