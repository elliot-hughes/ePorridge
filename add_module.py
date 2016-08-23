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

	if sn:
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
			print '<center><h3 style="color:red"><i>Serial number "{0}" already exists! It was not added.</i></h3></center>'.format(sn)

		else:
			cardid = module.fetch_cardid_from_sn(db,sn)
			base.begin()
			base.header_redirect("module.py?db={0}&card_id={1}".format(db,cardid))
			base.top(db)
	else:
		base.begin()
		base.header_redirect("home.py?db={0}".format(db),1)
		base.top(db) 
		print '<center><h3 style="color:red"><i>Tried to input null serial number. Do not do that.</i></h3></center>'.format(sn)
	
	base.bottom()
# :FUNCTIONS

# MAIN:
if __name__ == "__main__":
	main()
# :MAIN
