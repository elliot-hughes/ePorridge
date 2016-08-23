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
def add_note(db, card_id, note):
	# Connect to DB:
	con = connect(True, db)
	cur = con.cursor(buffered=True)
	
	# Insert:
	try:
		# The following method escapes characters correctly:
		cmd = "INSERT INTO Card_Notes (card_id, note, date_time) VALUES (%s, %s, %s)"
		values = (card_id, note, time.strftime("%d/%m/%Y %I:%M:%S"))
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
	card_id = cgi.escape(form.getvalue('serial_num'))		# This is coming from a form.
	cardid = cgi.escape(form.getvalue('card_id'))
	db = settings.get_db()
	
	try:
		note = form.getvalue('note')
	
		if note:
			# Begin:
			base.begin()
			base.header_redirect("module.py?db={0}&card_id={1}#notes".format(db, cardid))
			base.top(db)
	
			# Add note:
			result = add_note(db, sn, note)
			if result:
				print "added note:<br>"
				print note
#				base.header_redirect_module_notes(card_id, serial_num)
	
			base.bottom()

		else:
			base.begin()
			base.header_redirect("module.py?db={0}&card_id={1}".format(db, cardid),1)
			base.top(db)

			print '<center><h3 style="color:red"><i> ERR: Note is empty. Cannot add an empty note. </i></h3></center>'
			base.bottom()

	except Exception as err:  #Needed to deal with special characters in the note.
	
		note = cgi.escape(str(form.getvalue('note')))
		# Begin:
		base.begin()
		base.header_redirect("module.py?db={0}&card_id={1}#notes".format(db, cardid))
		base.top(db)
	
		# Add note:
		result = add_note(db, sn, note)
		if result:
			print "added note:<br>"
			print note
			base.header_redirect_module_notes(card_id, serial_num)
	
		base.bottom()
# :FUNCTIONS

# MAIN:
if __name__ == "__main__":
	main()
# :MAIN
