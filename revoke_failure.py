#!/usr/bin/python

import cgi
import base
import home_page_list
#import add_test_functions

#cgi header
print "Content-type: text/html\n"

form = cgi.FieldStorage()
test_id = base.cleanCGInumber(form.getvalue('test_id'))
#suggested_test = base.cleanCGInumber(form.getvalue('suggested'))

base.header(title='Revoke Failure')
base.top()

print '<br><br>'
print 'Revoking test %i from list of valid tests'%test_id
print 'Please add any comments about why the test is being revoked:'
print '<form action="revokeFormHandler.py" method="post" enctype="multipart/form-data">'
print '  <input type="hidden" name="test_id" value=%i>'%test_id
print '  <br><br>'
print '  <textarea rows="5" cols="100" name="comments"></textarea>'
print '  <br><br>'
print '  <input type="submit" value="Revoke">'
print '</form>'

base.bottom()
