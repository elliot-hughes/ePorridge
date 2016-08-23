#!/usr/bin/python

# IMPORTS:
import cgi
import cgitb
cgitb.enable()

import base, settings, module, testers
# :IMPORTS

# FUNCTIONS:
def print_form(db, cardid):
	sn = module.fetch_sn_from_cardid(db, cardid)
	print '<form method="post" class="sub-id-form" action="add_note.py?db={0}">'.format(db)
	print '<div class="row">'
	print '<div class="col-md-12">'
	print '<h4>Add a note for the board a serial number of \"{0}\"</h4>'.format(sn)
	print '</div>'
	print '</div>'
	print '<br><br>'
	
	print '<div class="row">'
	print '<div class="col-md-6">'
	print '<label>Tester:&nbsp;&nbsp;<select name="person_id"><option value="0">Select tester</option>'
	people = testers.fetch_user_info(db)
	for person in people:
		print u'<option value="{0}">{1}</option>'.format(person["id"], person["name"]).encode("utf-8")
	print '</select></label></div></div>'
	
	print '<div class="row">'
	print '<div class = "col-md-6">'
	print '<label class="sub-id">'
	print 'Note: <br>'
	print '<textarea rows="10" cols="100" , name="note"></textarea> <br>'
	print '</label>'
	print '<input type="hidden" name="serial_num" value="{0}">'.format(sn)
	print '<input type="hidden" name="card_id" value="{0}">'.format(cardid)
	print '<input type="submit" value="Submit">'
	print '</div>'
	print '</div>'
	print '</form>'


def main():
	# Arguments:
	form = cgi.FieldStorage()
	cardid = base.cleanCGInumber(form.getvalue('card_id'))
	db = settings.get_db()
	
	# Basic:
	base.begin()
	base.header(title='{0}: module'.format(db))
	base.top(db)
	
	# Form:
	print_form(db, cardid)
	
	base.bottom()
# :FUNCTIONS

# MAIN:
if __name__ == "__main__":
	main()
# :MAIN
