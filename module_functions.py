from connect import connect
import settings
import cgitb; cgitb.enable()

def Portage_fetch(test_type_id, card_sn):
    db = connect(0)
    cur = db.cursor()
    cur.execute("SELECT People.person_name, Test.day, Test.successful, Test.comments, Test_Type.name, Test.test_id FROM Test, Test_Type, People, Card  WHERE Test_Type.test_type = %(test_id)s AND Card.sn = %(sn)s AND People.person_id = Test.person_id AND Test_Type.test_type=Test.test_type_id AND Test.card_id = Card.card_id ORDER BY Test.day ASC" %{'test_id':test_type_id, 'sn':card_sn})
    return cur.fetchall()


def Portage_fetch_attach(test_id):
    db = connect(0)
    cur = db.cursor()
    cur.execute('SELECT attach_id, attachmime, attachdesc, originalname, test_id FROM Attachments WHERE test_id=%(tid)s ORDER BY attach_id' % {'tid':test_id})
    attachments = cur.fetchall()
    return attachments

def export_to_xml(sn, card_id):

    print 			'<div class="row">'
    #print  				'<div class="col-md-8">'
    #print  					'<h2><u>e-Portage for %d</u></h2>' %sn
    #print  				'</div>'
    print 				'<div class="col-md-8">'
    print 					'<br><br><br><br>'
    print                   '<a href="exportCard.py?card_id=%(id)d&serial_num=%(serial)d">' %{'serial':sn, 'id':card_id}
    print                          '<button> Export </button>'
    print                   '</a>'
    print 				'</div>'
    print 			'</div>'


def ePortageTest(test_type_id, card_sn, test_name, revokes ,attempts):

	print  			'<div class="row">'
	print           			'<div class="col-md-12">'
	print					'<h3 id="test-{0}">{1}</h3>'.format(test_type_id, test_name)
	print					'<br>'

	background_colors = {
		-1: "#F6F6F6",
		0: "#FFE5E5",
		1: "#EBFFE4",
	}

	n = 0
#	print attempts
	for attempt in attempts:
		# Determine success of test:
		if attempt[5] in revokes:		# Card ID
			good = -1		# Unknown
		else:
			if attempt[2] == 1:		# Success bit
				good = 1		# Passed
			else:
				good = 0		# Failed
		n += 1
		
		# Print stuff:
		print	   			'<h4>Attempt: %d</h4>'%n
		print				'<table class="table table-bordered table-striped Portage_table" style="width: 60%; background-color: {0};">'.format(background_colors[good])
		print						'<tbody>'
		print						'<tr>'
		print							'<th>Name</th>'
		print							'<th>Date</th>'
		print							'<th colspan=2>Successful?</th>'
#		print							'<th>Comments</th>'
		print						'</tr>'
		print						'<tr>'
		print					                '<td> %(pname)s </td>' %{ "pname":attempt[0]}
		print					                '<td> %(when)s </td>' %{ "when":attempt[1]}
		if good == -1:
			print					'<td><b>Revoked</b>: %(comment)s </td>' %{ "comment":revokes[attempt[5]] }
		elif good == 1:
			print					'<td align=left> Yes </td>'
			print "<td align=right style='{ background-color: yellow; }' ><a href='revoke_success.py?test_id=%(id)s'>Revoke</a></td>" %{ "id":attempt[5]}
		elif good == 0:
			print					'<td colspan=2>No</td>'
			print "<td align=right style='{ background-color: yellow; }' ><a href='revoke_failure.py?test_id=%(id)s'>Revoke</a></td>" %{ "id":attempt[5]}
		print						'</tr>'
		print						'<tr>'
		print						            '<td><b>Comments:</b></td>' 
		print					                '<td colspan=3> %(comm)s </td>' %{ "comm":attempt[3]}
		print						'</tr>'
		
		## Attachements:
		attachments = Portage_fetch_attach(attempt[5])
		for afile in attachments:
			print '<tr><td>Attachment: <a href="get_attach.py?attach_id=%s">%s</a><td colspan=2><i>%s</i></tr>' % (afile[0],afile[3],afile[2])
		
		print						'</tbody>'
		print                               '</table>'
		
		## Display image if there is one:
		images = [(afile[0], afile[-1]) for afile in attachments if (".png" in afile[3] or ".jpg" in afile[3])]
#		print images
		if images:
			location = settings.getAttachmentPathFor(images[0][1], images[0][0]).replace("/var/www/html", "")
			print "<a href='{0}'><img src='{0}' style='width:66%'></a>".format(location)
#			print location

	print				'</div>'
	print				'</div>'
	print                       '<hr><br>'


