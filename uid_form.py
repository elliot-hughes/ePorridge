#!/usr/bin/python

# IMPORTS:
import cgitb
cgitb.enable()
import cgi

import base, swttings
import home_page_list
import module_functions

# Deal with URL arguments:
form = cgi.FieldStorage()
card_id = base.cleanCGInumber(form.getvalue('card_id'))
serial_num = base.cleanCGInumber(form.getvalue('serial_num'))

# Print basic HTML stuff:
base.begin()
base.header(title='ATD: Add ID for Board {0}'.format(serial_num))		# Print the header
base.top()
#print 'card_id = ', card_id
#print  'serial_num = ', serial_num

print '''\t\t<form method="post" class="sub-id-form" action="add_id2.py">
			<div class="row">
				<div class="col-md-12">
					<h4>Add a unique ID for the board with SN = {0}</h4>
				</div>
			</div>
			<br>
			<br>
			<div class="row">
				<div class = "col-md-6">
					<label class="sub-id">
						Unique ID: <input name="unique_id">
					</label>
					<input type="hidden" name="card_id" value="{1}">
					<input type="hidden" name="serial_num" value="{0}">
					<input type="submit" value="Submit">
				</div>
			</div>
		</form>'''.format(serial_num, card_id)

base.bottom()
