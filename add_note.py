#!/usr/bin/python

# IMPORTS:
import cgi
import cgitb
cgitb.enable()
import time

import base, settings, testers
from connect import connect
# :IMPORTS

# FUNCTIONS:
def add_note(db, sn, note, person_id):
	# Connect to DB:
	con = connect(True, db)
	cur = con.cursor(buffered=True)
	
	# Insert:
	try:
		# The following method escapes characters correctly:
		cmd = "INSERT INTO Card_Notes (sn, note, date_time, person_id) VALUES (%s, %s, %s, %s)"
		values = (sn, note, time.strftime("%d/%m/%Y %I:%M:%S"), person_id)
		cur.execute(cmd, values)
		con.commit()
		con.close()
		return True
	except Exception as ex:
		print "<span style='color: red'>ERROR</span><br>"
		print ex
		print "<br><br>"
		print note
		return False


def main():
	# Arguments:
	form = cgi.FieldStorage()
	sn = cgi.escape(form.getvalue('serial_num'))		# This is coming from a form.
	cardid = cgi.escape(form.getvalue('card_id'))
	person_id = base.cleanCGInumber(form.getvalue('person_id'))
	db = settings.get_db()
	note = cgi.escape(form.getvalue('note')) if form.getvalue('note') else False
	
#	base.begin()
#	print person_id
#	print note
#	base.bottom()
	
	if not person_id:
		base.error(db, "You must select a tester to be associated with this note.")
	else:
		if not note:
			base.error(db, "You left the note field empty. You're not allowed to make an empty note.")
		else:
			# Begin:
			base.begin()
			base.header_redirect("module.py?db={0}&card_id={1}#notes".format(db, cardid))
			base.top(db)
			
			# Add note:
			result = add_note(db, sn, note, person_id)
			if result:
				print "added note:<br>"
				print note
#				base.header_redirect_module_notes(card_id, serial_num)
			
			base.bottom()
# :FUNCTIONS

# MAIN:
if __name__ == "__main__":
	main()
# :MAIN
