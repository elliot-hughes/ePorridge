#!/usr/bin/python

# IMPORTS:
import cgitb
cgitb.enable()
import cgi
import os

import time
import base, settings
from connect import connect
import module
# :IMPORTS

# FUNCTIONS:
def add_characteristic_basic(db, card_id, char_id, char_value):
	# Arguments:
#	card_id = module.fetch_cardid_from_sn(db, sn)
	
	# Connect to the DB:
	con = connect(True, db)
	cur = con.cursor()
	
	# Insert:
	cmd_sql = "INSERT INTO Card_Info (card_id, info_type, info) VALUES (%s, %s, %s)"
	## This is safer because Python takes care of escaping any illegal/invalid text
	items = (card_id, char_id, char_value)
	cur.execute(cmd_sql, items)
	test_id = cur.lastrowid
	con.commit()
	
	return 1

def check_duplicate_characteristic(db, card_id, char_id):
	
	# Connect to the DB:
	con = connect(True, db)
	cur = con.cursor()
	
	# Get the characteristics:
	cur.execute('SELECT info_type, card_id FROM Card_Info')
	existing_characteristics = cur.fetchall()

	# Compare the existing characteristics with the one above:
	already_exists = False	
	for info_type, temp_card_id in existing_characteristics:
		if temp_card_id == card_id and char_id == info_type:
			already_exists = True
		else:
			continue

	return already_exists
	

def main():
	# Arguments:
	form = cgi.FieldStorage()
	card_id = base.cleanCGInumber(form.getvalue("card_id"))
	
	#Characteristic and char_id value addition:
	char_id = base.cleanCGInumber(form.getvalue('CharacteristicID'))
	char_value = cgi.escape(form.getvalue('char_value'))
	
	db = settings.get_db()

	# Basic:
	if char_value:
		base.begin()
		base.header_redirect("module.py?db={0}&card_id={1}".format(db,card_id),seconds=1)
		base.top(db)
	
		# Add the characteristic:
		duplicate_exists = check_duplicate_characteristic(db, card_id, char_id)
		if not duplicate_exists:
			char_id = add_characteristic_basic(db, card_id, char_id, char_value)
		else: 
			print '<center><h3 style="color:red"><i>Characteristic already exists!</i></h3></center>'
	
		base.bottom()

	else:
		base.begin()
		base.header_redirect("module.py?db={0}&card_id={1}".format(db,card_id),1)
		base.top(db)
		
		print '<center><h3 style="color:red"><i> ERR: No characteristic info added! Please fill in the box.</i></h3></center>'

		base.bottom()

# :FUNCTIONS

# MAIN:
if __name__ == "__main__":
	main()
# :MAIN
