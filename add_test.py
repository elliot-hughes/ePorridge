#!/usr/bin/python

# IMPORTS:
import cgitb
cgitb.enable()
import cgi
import os

import base, settings, module
from connect import connect
import module
# :IMPORTS

# FUNCTIONS:
def add_test_basic(db, person_id, test_type, card_id, success, comments):
	# Arguments:
#	card_id = module.fetch_cardid_from_sn(db, sn)
	
	# Connect to the DB:
	con = connect(True, db)
	cur = con.cursor()
	
	# Insert:
	cmd_sql = "INSERT INTO Test (person_id, test_type_id, card_id, successful, comments, day) VALUES (%s, %s, %s, %s, %s, NOW())"
	## This is safer because Python takes care of escaping any illegal/invalid text
	items = (person_id, test_type, card_id, int(success), comments)
	#if comments:
	cur.execute(cmd_sql, items)
	test_id = cur.lastrowid
	con.commit()
#	else:	test_id = 0
	
	return test_id


def add_test_attachment(db, test_id, afile, desc, comments):
	if afile.filename:
		# Connect to DB:
		con = connect(True, db)
		cur = con.cursor()
		
		# Insert:
		originalname = os.path.basename(afile.filename)
		cur.execute("INSERT INTO Attachments (test_id, attachmime, attachdesc, comments, originalname) VALUES (%s,%s,%s,%s,%s)", (test_id, afile.type, desc, comments, originalname))
		att_id = cur.lastrowid
		con.commit()
		
		# Deal with path:
		ofn = settings.get_attachment_path(db, int(test_id), int(att_id))
		sub_path = os.path.dirname(ofn)
		if not os.path.exists(sub_path):
			os.makedirs(sub_path)
		open(ofn, 'wb').write(afile.file.read())
#		print '<div> The file %s was uploaded successfully. </div>' % (originalname)

def main():
	# Arguments:
	form = cgi.FieldStorage()
	person_id = base.cleanCGInumber(form.getvalue("person_id"))
	test_type = base.cleanCGInumber(form.getvalue("test_type"))
	card_id = base.cleanCGInumber(form.getvalue("card_id"))
	success = (False, True)[bool(form.getvalue("success"))]
	
	## Comments:
	comments = form.getvalue("comments")
	if comments:
		comments = cgi.escape(comments)
	
	db = settings.get_db()
	sn = module.fetch_sn_from_cardid(db, card_id)

	# Basic:
	base.begin()
	#base.header(title='{0}: add test'.format(db))
	base.header_redirect("module.py?db={0}&card_id={1}".format(db, card_id))
	#base.header_redirect_module_test(card_id, serial_num, test_type)
	base.top(db)
	
	# Add the test:
	test_id = add_test_basic(db, person_id, test_type, card_id, success, comments)
	## Attachments:
	for i in range(1, 4):
		afile = form['attach{0}'.format(i)]
		if (afile.filename):
			adesc= form.getvalue("attachdesc{0}".format(i))
			if adesc:
				adesc = cgi.escape(adesc)
			acomment= form.getvalue("attachcomment{0}".format(i))
			if acomment:
				acomment = cgi.escape(acomment)
			add_test_attachment(db, test_id, afile, adesc, acomment)
	
	base.bottom()
# :FUNCTIONS

# MAIN:
if __name__ == "__main__":
	main()
# :MAIN
