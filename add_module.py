#!/usr/bin/python

# IMPORTS:
import cgi
import cgitb
cgitb.enable()

import base, settings
from connect import connect
# :IMPORTS

# FUNCTIONS:
def main():
	# Arguments:
	form = cgi.FieldStorage()
	sn = form.getvalue("serial_number")
	#card_id = cgi.escape(form.getvalue('card_id'))
	db = settings.get_db()
	
	# Begin:
	base.begin()
	base.header(title='{0}: add module'.format(db))
	base.header_redirect("module.py?db={0}".format(db))
	base.top(db)
	
	# Insert:
	## Make sure SN is a number:
	try:
		sn = int(sn)
	except Exception as ex:
		print '<h3>ERROR: Serial number {0} isn\'t an integer.</h3>'.format(sn)
	else:
		## Attempt insert:
		try:
			con = connect(True, db)
			cur = con.cursor()
			cur.execute("INSERT INTO Card SET sn = '{0}'; ".format(sn)) 
			con.commit()
			con.close()
		except Exception as ex:
			print ex
			print '<h3>Serial number "{0}" already exists! It was not added.</h3>'.format(sn)
	
	base.bottom()
# :FUNCTIONS

# MAIN:
if __name__ == "__main__":
	main()
# :MAIN
