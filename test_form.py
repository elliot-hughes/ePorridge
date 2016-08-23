#!/usr/bin/python

# IMPORTS:
import cgitb
cgitb.enable()
import cgi

import base, settings
from connect import connect
import module
# :IMPORTS

# FUNCTIONS:
def print_long_desc(db, suggested_test):
	con = connect(False, db)
	cur = con.cursor()
	cur.execute("SELECT test_type, name, desc_long FROM Test_Type")
	rows = cur.fetchall()
	if not suggested_test:
		suggested_test = 0
	
	for test_type in rows:
		if test_type[0] == suggested_test:
			#print test_type[1].encode('utf-8')+': '
			#print test_type[2].encode('utf-8')
			print '<h3 style="text-align:justify"><b>'+test_type[1].encode('utf-8')+'</b>: '+test_type[2].encode('utf-8')+'</h3>'
 
def print_test_form(db, dbid, sn, suggested_test):
	# Arguments:
	if not suggested_test:
		suggested_test = 0
	uid = module.fetch_uniqueID(db, sn)
	
	# Connect to the DB:
	con = connect(False, db)
	cur = con.cursor()
	
	# Print form:
	print		'<form action="add_test.py?db={0}" method="post" enctype="multipart/form-data">'.format(db)
	print 			'<INPUT TYPE="hidden" name="card_id" value="{0}">'.format(dbid)
	print			'<div class="row">'
	print				'<div class="col-md-12">'
	print					'<h1>Add test for Card {0}<br>({1})</h1>'.format(sn, uid)
	print				'</div>'
	print			'</div>'
	print			'<br><br>'
	cur.execute("SELECT person_id, person_name FROM People;")
	rows = cur.fetchall()
	print			'<div class="row">'
	print				'<div class="col-md-6">'
	print					'<label>Tester'
	print					'<select name="person_id">'
	print						"<option value='0'>Select tester</option>"
	for person_id, name in rows:
		print						"<option value='{0}'>{1}</option>".format(person_id, name)
	print					'</select>'
	print					'</label>'
	print				'</div>'
	cur.execute("SELECT test_type, name FROM Test_Type ORDER BY relative_order ASC;")
	rows = cur.fetchall()
	print				'<div class="col-md-6">'
	print					'<label>Test Type'
	print					'<select name="test_type">'
	for test_type, test_name in rows:
		if test_type == suggested_test:
			print						u'<option value="{0}" selected>{1}</option>'.format(test_type, test_name).encode('utf-8')
		else:
			print						u'<option value="{0}">{1}</option>'.format(test_type, test_name).encode('utf-8')
	print					'</select>'
	print					'</label>'
	print				'</div>'
	print			'</div>'
	print_long_desc(db, suggested_test)
	print			'<br><br>'
	print			'<div class="row">'
	print				'<div class="col-md-3">'
	print					'<label>Successful?'
	print					"<input type='checkbox' name='success' value='1'>"
	print					'</label>'
	print				'</div>'
	print				'<div class="col-md-9">'
	print					'<label>Comments (mandatory)</label><p>'
	print					'<textarea rows="5" cols="50" name="comments"></textarea>'
	print				'</div>'
	print			'</div>'
	print			'<br><br>'
	print			'<div class="row">'
	print				'<div class="col-md-6">'
	print					'<input type="submit" value="Add Test">'
	print				'</div>'
	print			'</div>'
	
	## Attachments:
	for iattach in range(1, 4):
		print			'<br><hr><br>'    
		print			'<div class="row">'
		print				'<div class="col-md-2">'
		print					"<b>Attachment %d:</b>" % (iattach)
		print				'</div><div class="col-md-5">'
		print					"<INPUT type='file' name='attach%d'>"% (iattach)	
		print				'</div><div class="col-md-5">'
		print 					"<label>Description:</label> <INPUT type='text' class='form-control' name='attachdesc%d'>"% (iattach)	
		print                           '</div>'
		print                   '</div>'
		print			'<div class="row">'
		print				'<div class="col-md-10 col-md-offset-2">'
		print					'<label>Comments:</label>'
		print					'<textarea rows = "2" cols="50" class="form-control" name="attachcomment%d"></textarea>' % (iattach)	
		print                               '</div>'
		print                       '</div>'
	print			'<br><br><br><br>'
	
	## Submit:
	print			'<div class="row">'
	print				'<div class="col-md-6">'
	print					'<input type="submit" value="Add Test">'
	print				'</div>'
	print			'</div>'
	
	print			'<br><br><br><br>'
	print		'</form>'


def main():
	# Arguments
	form = cgi.FieldStorage()
	cardid = base.cleanCGInumber(form.getvalue('card_id'))
	suggested_test = base.cleanCGInumber(form.getvalue('suggested'))
	db = settings.get_db()
	sn = module.fetch_sn_from_cardid(db, cardid)
	
	# Basic:
	base.begin()
	base.header(title='{0}: test'.format(db))
	base.top(db)
	
	# Test form:
	print_test_form(db, cardid, sn, suggested_test)
	
	base.bottom()
# :FUNCTIONS

# MAIN:
if __name__ == "__main__":
	main()
# :MAIN
