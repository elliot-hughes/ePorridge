####################################################################
# Type: MODULE                                                     #
#                                                                  #
# Description: [description]                                       #
####################################################################

# IMPORTS:
import cgitb
cgitb.enable()
import cgi
from collections import OrderedDict

import base, settings
from connect import connect
import module_functions
# :IMPORTS

# FUNCTIONS:
def fetch_cardid_from_testid(db, test_id):
	con = connect(False, db)
	cur = con.cursor()
	cur.execute("SELECT card_id FROM Test WHERE test_id={0}".format(test_id))
	try:
		card_id = cur.fetchone()[0]		# If value in DB is "NULL", this returns None.
	except Exception as ex:
		print ex
		return 0
	else:
		if card_id:
			return card_id
		return 0

def fetch_testtypeid_from_testid(db, test_id):
	con = connect(False, db)
	cur = con.cursor()
	cur.execute("SELECT test_type_id FROM Test WHERE test_id={0}".format(test_id))
	try:
		testtype_id = cur.fetchone()[0]		# If value in DB is "NULL", this returns None.
	except Exception as ex:
		print ex
		return 0
	else:
		if testtype_id:
			return testtype_id
		return 0


def fetch_revoke(db, test_id):
	# Get a list of tests for this card:
	con = connect(False, db)
	cur = con.cursor()
	cur.execute("SELECT TestRevoke.comment FROM TestRevoke WHERE TestRevoke.test_id={0}".format(test_id))
	try:
		result = cur.fetchone()[0]
		if not result:		# If "comment" entry exists but is empty.
			return True
		return result
	except:
		return False


def fetch_tests(db, cardid, attachments=True, inclusive=True):
	# Get a list of tests for this card:
	con = connect(False, db)
	cur = con.cursor()
	
	# Fetch:
	revoked_ids = fetch_revoked(db, cardid)
	tests = OrderedDict()
	for testtype_dict in fetch_types(db, inclusive=inclusive):
		cur.execute("SELECT People.person_name, Test.day, Test.successful, Test.comments, Test_Type.name, Test.test_id FROM Test, Test_Type, People, Card WHERE Test_Type.test_type={0} AND Card.card_id={1} AND People.person_id=Test.person_id AND Test_Type.test_type=Test.test_type_id AND Test.card_id = Card.card_id ORDER BY Test.day ASC".format(testtype_dict["testtype_id"], cardid))
		test_dicts = [{
			"tester": item[0],
			"time": item[1],
			"passed": item[2],
			"comments": item[3],
			"type": item[4],
			"test_id": item[5],
			"revoked": (False, True)[bool(item[5] in revoked_ids)],
		} for item in cur.fetchall()]
		
		result_list = []
		for test_dict in test_dicts:
			cur.execute("SELECT Attachments.attach_id, Attachments.attachmime, Attachments.attachdesc, Attachments.originalname FROM Attachments WHERE Attachments.test_id={0}".format(test_dict["test_id"]))
			test_dict["attachments"] = [{
				"id": item[0],
				"type": item[1],
				"description": item[2],
				"name": item[3],
			} for item in cur.fetchall()]
			result_list.append(test_dict)
		
		tests[(testtype_dict["testtype_id"], testtype_dict["testtype_name"])] = result_list
	return tests


def fetch_test_statuses(db, cardid, inclusive=False):
	# Get a list of test status dictionaries for this card:
	con = connect(False, db)
	cur = con.cursor()
	cur.execute("SELECT Test.test_id, Test.test_type_id, Test_Type.required, Test.successful FROM Test_Type, Test WHERE Test.card_id={cardid} AND Test_Type.test_type=Test.test_type_id".format(cardid=cardid))
	statuses = [{"test_id": item[0], "testtype_id": item[1], "required": item[2], "passed": item[3]} for item in cur.fetchall()]
	
	# If necessary, subtract out the revoked tests:
	if not inclusive:
		testids_revoked = fetch_revoked(db, cardid)
		return [status for status in statuses if status["test_id"] not in testids_revoked]
	return statuses


def fetch_passed(db, cardid, revoked=False):
	# Get a list of all tests passed by this card:
	con = connect(False, db)
	cur = con.cursor()
	cur.execute("SELECT Test.test_id FROM Test_Type, Test WHERE Test.card_id={cardid} AND Test_Type.test_type=Test.test_type_id AND Test_Type.required=1 AND Test.successful=1".format(cardid=cardid))
	testids = [item[0] for item in cur.fetchall()]
	
	# If necessary, subtract out the revoked tests:
	if not revoked:
		testids_revoked = fetch_revoked(db, cardid)
		return [testid for testid in testids if testid not in testids_revoked]
	return testids


def fetch_failed(db, cardid, revoked=False):
	# Get a list of all tests failed by this card:
	con = connect(False, db)
	cur = con.cursor()
	cur.execute("SELECT Test.test_id FROM Test_Type, Test WHERE Test.card_id={cardid} AND Test_Type.test_type=Test.test_type_id AND Test_Type.required=1 AND Test.successful=0".format(cardid=cardid))
	testids = [item[0] for item in cur.fetchall()]
	
	# If necessary, subtract out the revoked tests:
	if not revoked:
		testids_revoked = fetch_revoked(db, cardid)
		return [testid for testid in testids if testid not in testids_revoked]
	return testids


def fetch_revoked(db, cardid):
	# Get a list of all tests for this card that were revoked:
	con = connect(False, db)
	cur = con.cursor()
	cur.execute("SELECT TestRevoke.test_id FROM TestRevoke, Test WHERE Test.card_id={cardid} AND Test.test_id=TestRevoke.test_id".format(cardid=cardid))
	testids = [item[0] for item in cur.fetchall()]
	return testids


def fetch_types(db, inclusive=True):
	# Get a list of all testtypes:
	con = connect(False, db)
	cur = con.cursor()
	cur.execute("SELECT test_type, name, required, relative_order FROM Test_Type")
	if not inclusive:
		return sorted([{"testtype_id": item[0], "testtype_name": item[1], "required": item[2], "order": item[3]} for item in cur.fetchall() if item[2]], key=lambda k: k["order"])
	return sorted([{"testtype_id": item[0], "testtype_name": item[1], "required": item[2], "order": item[3]} for item in cur.fetchall()], key=lambda k: k["order"])


def fetch_type_statuses(db, cardid, include_revoked=False):
	# Get a list of {testtype_id, testtype_name, required_value, passed_value} (for each test type):
	statuses = []
	test_statuses = fetch_test_statuses(db, cardid, inclusive=include_revoked)
	for testtype_dict in fetch_types(db, inclusive=True):
		testtype_id = testtype_dict["testtype_id"]
		status = testtype_dict
		passed = [test_status for test_status in test_statuses if test_status["passed"] and test_status["testtype_id"]==testtype_id]
		failed = [test_status for test_status in test_statuses if not test_status["passed"] and test_status["testtype_id"]==testtype_id]
		if passed and failed:
			status["passed"] = 0
		elif passed:
			status["passed"] = 1
		elif failed:
			status["passed"] = 0
		elif not passed and not failed:
			status["passed"] = -1
		statuses.append(status)
	return statuses


def fetch_untested_types(db, cardid, revoked=False):
	# Get a list of all testtypes untested by this card:
	con = connect(False, db)
	cur = con.cursor()
	cur.execute("SELECT Test.test_id FROM Test_Type, Test WHERE Test.card_id={cardid} AND Test_Type.test_type=Test.test_type_id AND Test_Type.required=1 AND Test.successful=0".format(cardid=cardid))
	testids = [item[0] for item in cur.fetchall()]
	
	# If necessary, subtract out the revoked tests:
	if not revoked:
		testids_revoked = fetch_revoked(db, cardid)
		return [testid for testid in testids if testid not in testids_revoked]
	return testids


def fetch_revokes(db, sn):
	con = connect(False, db)
	cur = con.cursor()
	cur.execute("SELECT TestRevoke.test_id, TestRevoke.comment FROM TestRevoke, Test, Card WHERE Card.sn = {sn} AND Card.card_id = Test.card_id AND Test.test_id = TestRevoke.test_id".format(sn=sn))
	rows = cur.fetchall()		# list of (test_id, comment) items
#	return {test[0]: test[1] for test in rows}		# For >= Python 2.7
	return dict((test[0], test[1]) for test in rows)

def fetch_testid_from_name(db, name):
	# Connect to the DB:
	con = connect(False, db)
	cur = con.cursor()
	cur.execute("SELECT test_type FROM Test_Type WHERE name='{0}'".format(name))
	return int(cur.fetchone()[0])

#def fetch_attachment(db, test_id):
#	con = connect(False, db)
#	cur = con.cursor()
#	cur.execute('SELECT attach_id, attachmime, attachdesc, originalname, test_id FROM Attachments WHERE test_id={0}'.format(test_id)
#	attachments = cur.fetchall()
#	return attachments
# :FUNCTIONS
