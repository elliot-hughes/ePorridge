#!/usr/bin/python

# IMPORTS:
import cgitb
cgitb.enable()
import cgi

import base, settings, module, test
from connect import connect
# :IMPORTS

# FUNCTIONS:

def print_stat_table(db):
	sn = []
	statuses_list = [(cardid, test.fetch_type_statuses(db, cardid)) for cardid in module.fetch_cardids(db)]
	
	rattata = 0 # boards failed
        mewtwo = 0 # boards passed
        chansey = 0 # boards incomplete
        pikachu = 0 # total boards
	mrmime = 0 # duplicates

        # Variables:
        background_colors = {
                -1: "#F6F6F6",      # Unfinished
                0: "#FFE5E5",       # Failed
                1: "#EBFFE4",       # Passed
		2: "#FF69B4",       # Why not
        }

        # print header
        print '<div class="row">'
        print    '<div class="col-md-12">'
        print        '<table class="table" style="width: 100%; font-size: 12px">'
        print            '<tbody>'
        print                '<tr>'
        print                    "<th style='background-color: #FFFFFF; font-size: 16px;'> Total Boards </th>"
        print                    "<th style='background-color: #F6F6F6; text-align: center; font-size: 16px;'> Boards Incomplete </th>"
        print                    '<th style="background-color: #EBFFE4; text-align: center; font-size: 16px;"> Boards Passed </th>'
        print                    '<th style="background-color: #FFE5E5; text-align: center; font-size: 16px;"> Boards Failed </th>'
        print                '</tr>'



	# fetch serial numbers, count boards, check statuses
        for cardid, statuses in statuses_list:
	        sn.append(module.fetch_sn_from_cardid(db, cardid))
		good = -1
		# count failed board
		if [status for status in statuses if status["passed"] == 0 and status["required"]]:
			# (if there's at least one failed required test)
			good = 0
			rattata += 1
		
		# count passed board
		elif [status for status in statuses if status["passed"] == 1 and status["required"]] == [status for status in statuses if status["required"]]:
			# (if the set of passed required tests equals the set of required tests)
			good = 1
			mewtwo += 1
	
		# incomplete boards
		elif [good == -1]:
			chansey += 1

		# count all boards
		pikachu += 1

	#hairror check
	try:
		pikachu == rattata + mewtwo + chansey
	except:
		print "<tr>NOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO nice hair</tr>"

	print "<tr style='background-color: {0}'>".format(background_colors[2])
	print "<td style='text-align: right'>"+str(pikachu)+"</td>"
	print "<td style='text-align: right'>"+str(chansey)+" ("+str(round(chansey/float(pikachu)*100))+"%)</td>"
	print "<td style='text-align: right'>"+str(mewtwo)+" ("+str(round(mewtwo/float(pikachu)*100))+"%)</td>"
	print "<td style='text-align: right'>"+str(rattata)+" ("+str(round(rattata/float(pikachu)*100))+"%)</td>"
	print "</tr>"
        print '</tbody></table></div></div><br><br>'

def print_tests_table(db):

	print '<div class="row">'
        print '<div class="col-md-12">'
        print '<table class="table" style="width: 100%; font-size: 12px">'
        print '<tbody>'
        print '<tr>'
	print '<th style="background-color: #FFFFFF; font-size: 16px;">Test</th>'
	print '<th style="background-color: #F6F6F6; text-align: center; font-size: 16px;">Boards Untested</th>'
	print '<th style="background-color: #EBFFE4; text-align: center; font-size: 16px;">Boards Passed</th>'
	print '<th style="background-color: #FFE5E5; text-align: center; font-size: 16px;">Boards Failed</th>'
	print '</tr>'
	
	statuses_list = [(cardid, test.fetch_type_statuses(db, cardid)) for cardid in module.fetch_cardids(db)]

	names = []
	totals = []
	passed = []
	failed = []
	remain = []

	for entry in statuses_list:
		for test2 in entry[1]:
			check = 1
			for k in names:
				if test2["testtype_name"] == k:
					check = 0
					ind = names.index(k)
					totals[ind] += 1
					if test2["passed"] == 1: passed[ind] += 1
					elif test2["passed"] == 0: failed[ind] += 1
					elif test2["passed"] == -1: remain[ind] += 1				
			if check == 1:
				names.append(test2["testtype_name"])
				totals.append(1)
				if test2["passed"] == 1: passed.append(1), failed.append(0), remain.append(0)
				elif test2["passed"] == 0: passed.append(0), failed.append(1), remain.append(0)
				elif test2["passed"] == -1: passed.append(0), failed.append(0), remain.append(1)

	passedper = []
	failedper = []
	remainper = []
	for i in range(len(totals)):
		passedper.append(round(passed[i]/float(totals[i])*100))
		failedper.append(round(failed[i]/float(totals[i])*100))
		remainper.append(round(remain[i]/float(totals[i])*100))

	for k in range(len(names)):
		print "<tr><td>"+str(names[k].encode('utf-8'))+"</td><td style='text-align:right'>"+str(remain[k])+" ("+str(remainper[k])+"%)"+"</td><td style='text-align:right'>"+str(passed[k])+" ("+str(passedper[k])+"%)"+"</td><td style='text-align:right'>"+str(failed[k])+" ("+str(failedper[k])+"%)"+"</td></tr>"

        print '</tbody></table></div></div><br><br>'

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
		print "<td> <a href='module.py?db={db}&card_id={cardid}'>{sn}</a></td>".format(db=db, cardid=cardid, sn=sn)
		
		## Unfinished testtypes:
		unfinished = [status for status in statuses if status["passed"] == -1]
#		print statuses
		for col in range(2):
			print '<td><ul>'
			for status in unfinished[col::2]:
				print u'<li> <a href="test_form.py?db={db}&card_id={cardid}&suggested={sug}">{name}</a>'.format(db=db, cardid=cardid, sug=status["testtype_id"], name=status["testtype_name"]).encode('utf-8')
			print '</ul></td>'
		
		## Passed testtypes:
		passed = [status for status in statuses if status["passed"] == 1]
		for col in range(2):
			print '<td><ul>'
			for status in passed[col::2]:
				print u'<li> <a href="module.py?db={db}&card_id={cardid}#test-{testtype_id}">{name}</a>'.format(db=db, cardid=cardid, testtype_id=status["testtype_id"], name=status["testtype_name"]).encode('utf-8')
			print '</ul></td>'
		
		## Failed testtypes:
		failed = [status for status in statuses if status["passed"] == 0]
		for col in range(2):
			print '<td><ul>'
			for status in failed[col::2]:
				print u'<li> <a href="module.py?db={db}&card_id={cardid}#test-{testtype_id}">{name}</a>'.format(db=db, cardid=cardid, testtype_id=status["testtype_id"], name=status["testtype_name"]).encode('utf-8')
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
	print_stat_table(db)
	print_tests_table(db)
	print_modules_table(db)
	
	# End:
	base.bottom()
#: FUNCTIONS

# MAIN:
if __name__ == "__main__":
	main()
# :MAIN
