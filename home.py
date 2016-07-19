#!/usr/bin/python

# IMPORTS:
import cgitb
cgitb.enable()
import cgi

import base, settings
import module
from connect import connect
# /IMPORTS

# FUNCTIONS:
def fetch_list_module(db):
	# Get cursor:
	con = connect(False, db)
	cur = con.cursor()
	
	# Fectch from DB:
	cur.execute("SELECT sn, Card_id FROM Card ORDER by Card.sn ASC")
	rows = cur.fetchall()
	return rows


def print_list_module(db, n_columns=3):
	# Get module list:
	row = fetch_list_module(db)
	
	# Format columns:
	cols = ['']*n_columns
	for i, card in enumerate(row):
		card_sn = card[0]
		card_dbid = card[1]
		card_uid = module.fetch_uniqueID(db, card_sn)
		
		cols[i%n_columns] += '<li style="font-size:18px"><a href="module.py?db={db}&card_id={dbid}&serial_num={sn}"> {sn} ({uid})</h4></li>'.format(db=db, sn=card_sn, dbid=card_dbid, uid=card_uid)
	
	# Print columns:
	print '<div class="row">'
	print '<div class="col-md-4"><ul>'
	print cols[0]
	print '</ul></div><div class="col-md-4"><ul>'
	print cols[1]
	print '</ul></div><div class="col-md-4"><ul>'
	print cols[2]
	print '</ul></div>'


def print_module_form(db):
	print	'<form method="post" class="sub-card-form" action="add_module.py?db={db}">'.format(db=db)
	print		'<b>Add new module:</b><br>'
	print		'Serial number: <input type="int" name="serial_number">&nbsp;<input type="submit" value="Submit">'
	print	'</form>'


def print_home(db):
	print '\t\t<div class="row">'
	print '\t\t\t<div class="col-md-3">'
	print '\t\t\t\t<h2>All Boards:</h2>'
	print '\t\t\t\t<strong><em>(Sorted by serial number)</em></strong>'
	print '\t\t\t</div>'
	print '\t\t\t<div class="col-md-6">'
#	print '\t\t\t\t<a href="add_module.py?db={db}"><button type="button">Add a new board</button></a>'.format(db=db)
	print_module_form(db)
	print '\t\t\t</div>'
	print '\t\t</div>'
	print '\t\t<br>'
	print_list_module(db)



def main():
	# Identify DB from URL:
	db = settings.get_db()
	
	base.begin()                                    # Print the preamble and opening html tag.
	base.header(title='ePorridge')		# Print the header.
	base.top(db)		# Print the top portion of the body (title, buttons). This remains the same for every page.
	print_home(db)		# Print what should appear on the home page. (Defined above.)
	base.bottom()		# Print footer (if applicable) and closing body and html tags.
# :FUNCTIONS

# MAIN:
if __name__ == "__main__":
	main()
# :MAIN
