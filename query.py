#!/usr/bin/python

# IMPORTS:
import cgitb
cgitb.enable()
import cgi

import base, settings, module
# :IMPORTS

# CLASSES:
# :CLASSES

# VARIABLES:
# :VARIABLES

# FUNCTIONS:
def main():
	# Arguments:
	form = cgi.FieldStorage()
	sn = form.getvalue("serial_number")
	db = settings.get_db()
	## KLUDGE for special ease-of-access for "hf_qie" DBs:
	if "hf_qie" in db:
		if len(sn) == 3:
			sn = "3040000000000500" + sn
	
	if sn:
		card_id = module.fetch_cardid_from_sn(db, sn)
		if card_id:
			base.error(db, "Finding the module ...", redirect="module.py?db={0}&card_id={1}".format(db, card_id), redirect_time=0)
		else:
			base.error(db, "There is no module in this database with a serial number matching \"{0}\".".format(sn))
	else:
		base.error(db, "What did you expect to happen?")
	return True
# :FUNCTIONS

# MAIN:
if __name__ == "__main__":
	main()
# :MAIN

