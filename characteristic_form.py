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
def print_characteristic_form(db, dbid, sn, suggested_char):
	# Arguments:
	if not suggested_char:
		suggested_char = 0
	uid = module.fetch_uniqueID(db, sn)
	
	# Connect to the DB:
	con = connect(False, db)
	cur = con.cursor()
	
	# Print form:
	print		'<form action="add_characteristic.py?db={0}" method="post" enctype="multipart/form-data">'.format(db)
	print 			'<INPUT TYPE="hidden" name="serial_number" value="{0}">'.format(sn)
	print 			'<INPUT TYPE="hidden" name="card_id" value="{0}">'.format(dbid)
	print			'<div class="row">'
	print				'<div class="col-md-12">'
	print					'<h1>Add characteristic for Card {0}<br>({1})</h1>'.format(sn, uid)
	print				'</div>'
	print			'</div>'
	print			'<br><br>'
	print			'<div class="row">'
	cur.execute("SELECT Info_Name,info_type_id FROM Card_Info_Types;")
	rows = cur.fetchall()
	print				'<div class="col-md-6">'
	print					'<label> Characteristic'
	print					'<select name="CharacteristicID">'
	for characteristic, info_type_id in rows:
		if info_type_id == suggested_char:
			print						'<option value="{0}" selected>{1}</option>'.format(info_type_id, characteristic)
		else: 
			print						'<option value="{0}">{1}</option>'.format(info_type_id, characteristic)
	print					'</select>'
	print					'</label>'
	print				'</div>'
	print			'</div>'
	print			'<br><br>'

	print			'<div class="row">'
	print				'<div class="col-md-9">'
	print					'<label> Characteristic Value </label><p>'
	print					'<textarea rows="5": cols="50" name="char_value"></textarea>'
	print				'</div>'
	print			'</div>'
	print			'<br><br>'
	
## Submit:
	print			'<div class="row">'
	print				'<div class="col-md-6">'
	print					'<input type="submit" value="Add Characteristic">'
	print				'</div>'
	print			'</div>'

	print			'<br><br><br><br>'
	print		'</form>'


def main():
	# Arguments
	form = cgi.FieldStorage()
	cardid = base.cleanCGInumber(form.getvalue('card_id'))
	db = settings.get_db()
	suggested_char = base.cleanCGInumber(form.getvalue('suggested'))
	sn = module.fetch_sn_from_cardid(db, cardid)
	
	# Basic:
	base.begin()
	base.header(title='{0}: characteristic'.format(db))
	base.top(db)
	
	# Characteristic form:
	print_characteristic_form(db, cardid, sn, suggested_char)
	
	base.bottom()
# :FUNCTIONS

# MAIN:
if __name__ == "__main__":
	main()
# :MAIN
