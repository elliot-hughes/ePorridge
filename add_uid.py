#!/usr/bin/python

# IMPORTS:
import cgi, cgitb
cgitb.enable()

import base, settings, module
from connect import connect
# :IMPORTS

# FUNCTIONS:
def main():
	# Arguments:
	form = cgi.FieldStorage()
	if form.getvalue('unique_id'):
		uid = cgi.escape(form.getvalue('unique_id'))
		card_id = cgi.escape(form.getvalue('card_id'))
	db = settings.get_db()
	
	# Print basic HTML stuff:
	base.begin()
	base.header(title='Adding a unique ID...')
	base.header_redirect("module.py?db={0}&card_id={1}".format(db, card_id))
	base.top(db)
	
	# Add:
	try:
		con = connect(True, db)
		cur = con.cursor()
		cur.execute('UPDATE Card SET unique_id="{0}" WHERE card_id={1}'.format(uid, card_id))
		con.commit()
		con.close()
	except Exception as err:
		print "<span style='color: red'>ERROR</span><br>"
		print err
#		print("<h3>Serial number already exists!</h3>")

	base.bottom()
# :FUNCTIONS

# MAIN:
if __name__ == "__main__":
	main()
# :MAIN
