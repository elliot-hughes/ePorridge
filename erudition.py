#!/usr/bin/python

# IMPORTS:
import cgi
import cgitb
cgitb.enable()

import base, settings
from connect import connect
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

def fetch_card_info(db):
	# Connect to DB:
	con = connect(False, db)
	cur = con.cursor()
	
	# Fetch from DB:
	cur.execute("SELECT info_type_id, Info_Name, Info_Desc_Short, Info_Desc_Long FROM Card_Info_Types")
	rows = cur.fetchall()
	
	# Return:
	return sorted([{'id':info[0], 'name':info[1], 'short':info[2], "long":info[3]} for info in rows], key=lambda k: k["id"])

def print_test_info_table(db):
	print '<div class="row">'
	print '<div class="col-md-12">'
	print '<center><h3>Test information</h3></center>'
	print '<table class="table" id="testInfoTable" style="width:100%">'
	print '<tbody>'
	print '<tr>'
	print '<th>Test name</th>'
	print '<th>Description</th>'
	print '<th>Required?</th>'
	print '</tr>'
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

	print '</tbody>'
	print '</table>'
	print '</div>'
	print '</div>'

def print_card_info_table(db):
	card_infos = fetch_card_info(db)
	print '<div class="row">'
	print '<div class="col-md-12">'
	print '<center><h3>Module information</h3></center>'
	if (card_infos):
		print '<table class="table" id="cardInfoTable" style="width:100%">'
		print '<tbody>'
		print '<tr>'
		print '<th>Characteristic</th>'
		print '<th>Description</th>'
		print '</tr>'
		for card_info in card_infos:
	
			print '<tr align=left>'
			print u'<td>{0}</td>'.format(card_info['name']).encode('utf-8')
			print u'<td>{0}</td>'.format(card_info['long']).encode('utf-8')
			print '</tr>'

		print '</tbody>'
		print '</table>'
		print '</div>'
		print '</div>'
	else:
		print '<center><p><i>No module information.</i></p></center>'

def print_testtype_form(db):
	print '<div class="row"><form action="add_testtype.py?db={0}" method="post" enctype="multipart/form-data">'.format(db)
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
	print '</form></div>'

def print_cardinfotype_form(db):
	print '<div class="row"><form action="add_cardInfoType.py?db={0}" method="post" enctype="multipart/form-data">'.format(db)
	print '\t<div class="col-md-6">'
	print '\t\t<b>Add characteristic type:</b><br>'
	print '\t\tName:<br>'
	print '\t\t<input type="text" name="characteristic"><br><br>'
	print '\t\tDescribe the characteristic in brief:<br>'
	print '\t\t<textarea name="descShort" rows="5" cols="50"></textarea><br><br>'
	print '\t\tDescribe the characteristic at length:<br>'
	print '\t\t<textarea name="descLong" rows="5" cols="100"></textarea><br><br>'
	print '\t\t<input type="submit" value="Submit"><br><br>'
	print '\t</div>'
	print '</form></div>'

def main():
	db = settings.get_db()
	
	base.begin()
	base.header(title='{0}: tests'.format(db))
	base.top(db)

	print_test_info_table(db)
	print '<br><br>'	
	print_testtype_form(db)

	print_card_info_table(db)
	print '<br><br>'	
	print_cardinfotype_form(db)

	base.bottom()
# :FUNCTIONS

# MAIN:
if __name__ == "__main__":
	main()
# :MAIN
