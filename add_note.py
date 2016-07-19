#!/usr/bin/python

# IMPORTS:
import cgi
import cgitb
cgitb.enable()
import time

import base, settings
from connect import connect
# :IMPORTS

# FUNCTIONS:
def add_note(db, sn, note):
	# Connect to DB:
	con = connect(True, db)
	cur = con.cursor(buffered=True)
	
	# Insert:
	try:
		# The following method escapes characters correctly:
		cmd = "INSERT INTO Card_Notes (sn, note, date_time) VALUES (%s, %s, %s)"
		values = (sn, note, time.strftime("%d/%m/%Y %I:%M:%S"))
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
	note = cgi.escape(form.getvalue('note'))
	sn = cgi.escape(form.getvalue('serial_num'))
	cardid = cgi.escape(form.getvalue('card_id'))
	db = settings.get_db()
	
	# Begin:
	base.begin()
	base.header_redirect("module.py?db={0}&card_id={1}&serial_num={2}#notes".format(db, cardid, sn))
	base.top(db)
	
	# Add note:
	result = add_note(db, sn, note)
	if result:
		print "added note:<br>"
		print note
#		base.header_redirect_module_notes(card_id, serial_num)
	
	base.bottom()
# :FUNCTIONS

# MAIN:
if __name__ == "__main__":
	main()
# :MAIN
