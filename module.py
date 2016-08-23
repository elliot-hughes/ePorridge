#!/usr/bin/python

# IMPORTS:
import cgitb
cgitb.enable()
import cgi

import base, settings
import test
from connect import connect
import module_functions
# :IMPORTS

# FUNCTIONS:
def fetch_revokes(db, sn):
	con = connect(False, db)
	cur = con.cursor()
	cur.execute("SELECT TestRevoke.test_id, TestRevoke.comment FROM TestRevoke, Test, Card WHERE Card.sn = {sn} AND Card.card_id = Test.card_id AND Test.test_id = TestRevoke.test_id".format(sn=sn))
	rows = cur.fetchall()		# list of (test_id, comment) items
#	return {test[0]: test[1] for test in rows}		# For >= Python 2.7
	return dict((test[0], test[1]) for test in rows)


def fetch_cardids(db):
	# Get a list of cardids:
	con = connect(False, db)
	cur = con.cursor()
	cur.execute("SELECT card_id FROM Card ORDER by sn ASC")
	return [item[0] for item in cur.fetchall()]


def fetch_sn_from_cardid(db, cardid):
	con = connect(False, db)
	cur = con.cursor()
	cur.execute("SELECT sn FROM Card WHERE card_id={0}".format(cardid))
	try:
		sn = cur.fetchone()[0]		# If value in DB is "NULL", this returns None.
	except Exception as ex:
		return 0
	else:
		if sn:
			return sn
		return 0


def fetch_cardid_from_sn(db, sn):
	con = connect(False, db)
	cur = con.cursor()
	cur.execute("SELECT card_id FROM Card WHERE sn={0}".format(sn))
	try:
		dbid = cur.fetchone()[0]		# If value in DB is "NULL", this returns None.
	except Exception as ex:
#		print ex
		return 0
	else:
		if dbid:
			return dbid
		return 0

def fetch_uniqueID_from_card_id(db, card_id): #Phase out the sn
	con = connect(False, db)
	cur = con.cursor()
	cur.execute("SELECT unique_id FROM Card WHERE card_id={0}".format(card_id))
	try:
		uid = cur.fetchone()[0] 	#If value in DB is "NULL", thsi returns None.
	except Exception as ex:
		return 0
	else:
		if uid:
			return uid
		return 0

def fetch_uniqueID(db, sn):
	con = connect(False, db)
	cur = con.cursor()
	cur.execute("SELECT unique_id FROM Card WHERE sn={0}".format(sn))
	try:
		uid = cur.fetchone()[0]		# If value in DB is "NULL", this returns None.
	except Exception as ex:
		return 0
	else:
		if uid:
			return uid
		return 0

def print_uid_form(db, cardid):
	print '<form method="post" action="add_uid.py?db={db}">'.format(db=db)
	print 'Unique ID: <input type="text" name="unique_id">&nbsp;<input type="submit" value="Add">'
	print '<input type="hidden" name="card_id" value="{0}">'.format(cardid)
	print '</form>'

def print_test_form(db, cardid):
	sn = fetch_sn_from_cardid(db, cardid)
	uid = fetch_uniqueID(db, sn)
	print '<div class="row">'
	print '<div class="col-md-8">'
	print '<h2>SN {0}<br>({1})</h2>'.format(sn, uid)
	print '</div>'
	print '<div class="col-md-4">'
	print '<br><br>'
	print '<a href="characteristic_form.py?db={db}&card_id={dbid}">'.format(db=db, dbid=cardid, uid=uid)
	print '<button>Add a new characteristic</button>'
	print '</a><br>'
	print '<a href="test_form.py?db={db}&card_id={dbid}">'.format(db=db, dbid=cardid, uid=uid)
	print '<button>Add a new test</button>'
	print '</a><br>'
	print '<a href="note_form.py?db={db}&card_id={dbid}">'.format(db=db, dbid=cardid, uid=uid)
	print '<button>Add a new note</button>'
	print '</a><br><br>'
	if not uid:
		print_uid_form(db, cardid)
	print '</a>'
	print '</div>'
	print '</div>'


def print_test(db, n, test_dict):
	# Variables:
	background_colors = {
		-1: "#F6F6F6",
		0: "#FFE5E5",
		1: "#EBFFE4",
	}
	
	# Determine success of test:
	good = -1
	if not test_dict["revoked"]:
		good = (0, 1)[test_dict["passed"]]
	
	## So, good == -1 means that the test is revoked (whether or not it passed), good == 0 means it failed, and good == 1 means it passed.
	
	# Print information:
	print '<h4>Attempt: {0}</h4>'.format(n)
	print '<table class="table table-bordered table-striped Portage_table" style="width: 60%; background-color: {0};">'.format(background_colors[good])
	print '<tbody><tr>'
	print '<th>Name</th>'
	print '<th>Date</th>'
	print '<th colspan=2>Successful?</th>'
	print '</tr><tr>'
	print '<td>{0}</td>'.format(test_dict["tester"])
	print '<td>{0}</td>'.format(test_dict["time"])
	if good == -1:
		print u'<td><b>Revoked</b>: {0}</td>'.format(test.fetch_revoke(db, test_dict["test_id"])).encode('utf-8')
	else:
		print '<td align=left>{0}</td>'.format(("no", "yes")[good])
#		print "<td align=right style='{{background-color: yellow;}}'><a href='revoke.py?db={0}&test_id={1}'>Revoke</a></td>".format(db, test_dict["test_id"])
		print "<td align=right style='{{background-color: yellow;}}'>"
		print '<form method="post" class="sub-card-form" action="revoke.py?db={0}&test_id={1}">'.format(db, test_dict["test_id"])
		print 'Revoke:<br>'
		print '<input type="text" name="comment"><br><input type="submit" value="Submit">'
		print '</form>'
		print "</td>"
	print '</tr><tr>'
	print '<td><b>Comments:</b></td>' 
	print u'<td colspan=3>{0}</td>'.format(test_dict["comments"]).encode('utf-8')
	print '</tr>'
	
	## Print attachements:
	for attachment in test_dict["attachments"]:
		if not test_dict["revoked"]:
			print u'<tr><td>Attachment: <a href="get_attach.py?db={0}&attach_id={1}">{2}</a><td colspan=2><i>{3}</i></tr>'.format(db, attachment["id"], attachment["name"], attachment["description"]).encode('utf-8')
	print '</tbody></table>'
	### Display image if there is one:
	for attachment in test_dict["attachments"]:
		if not test_dict["revoked"]:
			ext = attachment["name"].split(".")[-1].lower()
			if ext in ["png", "jpg", "jpeg", "gif"]:
				location = settings.get_attachment_path(db, test_dict["test_id"], attachment["id"]).replace("/var/www/html", "")
				print "<a href='{0}'><img src='{0}' style='width:66%'></a>".format(location)


def print_tests(db, cardid):
	print "<h2 id='tests'>Test information</h2>"
	tests = test.fetch_tests(db, cardid, inclusive=True)
	for testtype_tuple, test_list in tests.items():
		print '<div><br><div class="row">'
		print '<div class="col-md-12">'
		print u'<h3 id="test-{testtype_id}"><a href="test_form.py?db={db}&card_id={cardid}&suggested={testtype_id}">{name}</a></h3><br>'.format(db=db, testtype_id=testtype_tuple[0], name=testtype_tuple[1], cardid=cardid).encode('utf-8')
		for i, test_dict in enumerate(test_list):
			print_test(db, i + 1, test_dict)
		print '<hr></div></div>'
	

def print_characteristics(db, cardid):

	sn = fetch_sn_from_cardid(db, cardid)
	con = connect(False, db)
	cur = con.cursor()

	print '<div class="row">'
	print '<div class="col-md-12">'
	print "<h2>Module information</h2>"
	cur.execute("SELECT Card_Info.card_id, Card_Info.info_type, Card_Info.info, Card_Info_Types.info_type_id, Card_Info_Types.Info_Name FROM Card_Info, Card, Card_Info_Types WHERE Card_Info.card_id={0} AND Card_Info_Types.info_type_id = Card_Info.info_type AND Card.sn={1}".format(cardid,sn));
	characteristic_list = []
	characteristic_list = cur.fetchall()
	if len(characteristic_list) != 0:
		print '<table class="table" style="width:100%; font-size: 12px">'
  		print '<tr><th><h3>Characteristic</h3></th><th><h3>Value</h3></th></tr>'
	
		for item in characteristic_list:
			print '<tr><th>{char_name}</th>'.format(char_name=item[4])
			print '<th>{char_value}</th>'.format(char_value=item[2])
	
		print '</table>'
	else:
		print '<center><h4><i> There is no module information </i></h4></center>'

def print_notes(db, cardid):
	sn = fetch_sn_from_cardid(db, cardid)
	# Fetch list of notes:
	con = connect(False, db)
	cur = con.cursor()
	cur.execute("SELECT date_time, note FROM Card_Notes WHERE sn={0}".format(sn));
	notes = cur.fetchall()
	
	# Print notes:
	print '<div class="row">'
	print '<div class="col-md-12">'
	print "<h2 id='notes'>User notes</h2><br>"
	if notes:
		for note in notes :
			print "{0}</b><br>".format(note[0])
			print u"<i>{0}</i><br><br><br><br>".format(note[1]).encode('utf-8')
	else:
		print "<i>(There are no notes for this module.)</i>"
	print '</div><br><div><hr><br>'


def main():
	# Arguments:
	form = cgi.FieldStorage()
	cardid = base.cleanCGInumber(form.getvalue('card_id'))
#	sn = base.cleanCGInumber(form.getvalue('serial_num'))
	db = settings.get_db()
	sn = fetch_sn_from_cardid(db, cardid)
	
	# Basic:
	base.begin()
	base.header(title='{0}: module'.format(db))
	base.top(db)
	
	# Add test form:
	print_test_form(db, cardid)
	print_characteristics(db, cardid)
	print_tests(db, cardid)
	print_notes(db, cardid)
	
#	module_functions.export_to_xml(serial_num, card_id)
	
	base.bottom()
# :FUNCTIONS

# MAIN:
if __name__ == "__main__":
	main()
# :MAIN
