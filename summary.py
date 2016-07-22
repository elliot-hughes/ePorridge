#!/usr/bin/python

# IMPORTS:
import cgitb
cgitb.enable()
import cgi

import base, settings, module, test
from connect import connect
import mysql.connector
import module, testtypes
# :IMPORTS

# FUNCTIONS:
def print_modules_table(db):
	# Variables:
	background_colors = {
		-1: "#F6F6F6",      # Unfinished
		0: "#FFE5E5",       # Failed
		1: "#EBFFE4",       # Passed
	}
	## Get the information about each card:
	statuses_list = [(cardid, test.fetch_type_statuses(db, cardid)) for cardid in module.fetch_cardids(db)]
	
	# The table:
	print '<div class="row">'
	print    '<div class="col-md-12">'
	print        '<table class="table" style="width: 100%; font-size: 12px">'
	print            '<tbody>'
	print                '<tr>'
	print                    "<th style='background-color: #F0F0F0; font-size: 16px;'> S/N </th>"
	print                    "<th colspan=2 style='background-color: #F0F0F0; text-align: center; font-size: 16px;'> Tests Remaining </th>"
	print                    '<th colspan=2 style="background-color: #D7FFCA; text-align: center; font-size: 16px;"> Tests Passed </th>'
	print                    '<th colspan=2 style="background-color: #FFD4D4; text-align: center; font-size: 16px;"> Tests Failed </th>'
	print                '</tr>'

	for cardid, statuses in statuses_list:
		# Module variables:
		sn = module.fetch_sn_from_cardid(db, cardid)
		
		# Determine total quality of module:
		good = -1
		if [status for status in statuses if status["passed"] == 0 and status["required"]]:
			# (if there's at least one failed required test)
			good = 0
		elif [status for status in statuses if status["passed"] == 1 and status["required"]] == [status for status in statuses if status["required"]]:
			# (if the set of passed required tests equals the set of required tests)
			good = 1
		
		# Print row:
		print "<tr style='background-color: {0}'>".format(background_colors[good])
		print "<td> <a href='module.py?db={db}&card_id={cardid}&serial_num={sn}'>{sn}</a></td>".format(db=db, sn=sn, cardid=cardid)
		
		## Unfinished testtypes:
		unfinished = [status for status in statuses if status["passed"] == -1]
#		print statuses
		for col in range(2):
			print '<td><ul>'
			for status in unfinished[col::2]:
				print u'<li> <a href="test_form.py?db={db}&card_id={cardid}&serial_num={sn}&suggested={sug}">{name}</a>'.format(db=db, cardid=cardid, sn=sn, sug=status["testtype_id"], name=status["testtype_name"]).encode('utf-8')
			print '</ul></td>'
		
		## Passed testtypes:
		passed = [status for status in statuses if status["passed"] == 1]
		for col in range(2):
			print '<td><ul>'
			for status in passed[col::2]:
				print u'<li> <a href="module.py?db={db}&card_id={cardid}&serial_num={sn}#test-{testtype_id}">{name}</a>'.format(db=db, cardid=cardid, sn=sn, testtype_id=status["testtype_id"], name=status["testtype_name"]).encode('utf-8')
			print '</ul></td>'
		
		## Failed testtypes:
		failed = [status for status in statuses if status["passed"] == 0]
		for col in range(2):
			print '<td><ul>'
			for status in failed[col::2]:
				print u'<li> <a href="module.py?db={db}&card_id={cardid}&serial_num={sn}#test-{testtype_id}">{name}</a>'.format(db=db, cardid=cardid, sn=sn, testtype_id=status["testtype_id"], name=status["testtype_name"]).encode('utf-8')
			print '</ul></td>'
		
		print '</tr>'
	print '</tbody></table></div></div><br><br>'


def main():
	# Arguments:
	db = settings.get_db()
	
	# Basic:
	base.begin()
	base.header(title='{0}: summary'.format(db))
	base.top(db)
	
	# Modules table:
	print_modules_table(db)
	
	# End:
	base.bottom()
#: FUNCTIONS

# MAIN:
if __name__ == "__main__":
	main()
# :MAIN
