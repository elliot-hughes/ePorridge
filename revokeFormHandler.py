#!/usr/bin/python

import cgi
import base

from connect import connect
import mysql.connector
import cgitb; cgitb.enable()

def inRevokeList( test_id ) : 

    db = connect(0)
    cur = db.cursor()

    cur.execute("SELECT test_id FROM TestRevoke where test_id=%i"%test_id)
    rows = cur.fetchall()
    #print rows

    return not rows==[] 

def addTestToRevokeList(test_id, comments):
	db = connect(1)
	cur = db.cursor()
	
	# The following method escapes characters correctly:
	cmd = "INSERT INTO TestRevoke (test_id, comment) VALUES (%s, %s)"
	values = (test_id, comments)
	cur.execute(cmd, values)
	
	db.commit()

#cgi header
print "Content-type: text/html\n"

form = cgi.FieldStorage()
test_id = base.cleanCGInumber(form.getvalue("test_id"))
comments = cgi.escape(form.getvalue("comments"))

base.header(title='Revoke')
base.top()

print '<br><br>'

if not inRevokeList( test_id ) : 
    addTestToRevokeList(test_id, comments) 
    print 'Done'
else :
    print 'Test already revoked...'

base.bottom()

