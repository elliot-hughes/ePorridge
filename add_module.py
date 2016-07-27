#!/usr/bin/python

# IMPORTS:
import cgi
import cgitb
cgitb.enable()

import base, settings, module
from connect import connect
# :IMPORTS

# FUNCTIONS:
def main():
	# Arguments:
	form = cgi.FieldStorage()
	sn = form.getvalue("serial_number")
	db = settings.get_db()
	
	## Attempt insert:
	try:
		con = connect(True, db)
		cur = con.cursor()
		cur.execute("INSERT INTO Card SET sn = '{0}'; ".format(sn)) 
		con.commit()	
		con.close()
	
	except Exception as ex:
		base.begin()
		base.header(title='{0}: add module'.format(db))
		base.top(db)
		print ex
		print '<h3>Serial number "{0}" already exists! It was not added.</h3>'.format(sn)

	else:
		cardid = module.fetch_cardid_from_sn(db,sn)
		base.begin()
		base.header_redirect("module.py?db={0}&card_id={1}".format(db,cardid))
		base.top(db)
	
	base.bottom()
# :FUNCTIONS

# MAIN:
if __name__ == "__main__":
	main()
# :MAIN
