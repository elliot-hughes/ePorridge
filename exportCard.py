#!/usr/bin/python
import cgi
import base
import home_page_list
import exportCard_functions


#cgi header
print "Content-type: text/html\n"

form = cgi.FieldStorage()
#card_id = form.getvalue('card_id')
serial_num = base.cleanCGInumber(form.getvalue('serial_num'))

base.header(title='Exporting Card: {0}'.format(serial_num))
base.top()

exportCard_functions.export(serial_num)

base.bottom()
