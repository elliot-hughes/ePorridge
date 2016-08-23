from connect import connect
import mysql.connector
import module_functions, settings
import time


def add_id(sn, qid):
	try:
		db = connect(1)
		cur = db.cursor()
		cur.execute("UPDATE Card SET unique_id ='{1}' WHERE sn ={0};".format(sn, qid))
		print "<span style='color: green'>SUCCESS:</span><br>"
		print "<span>UPDATE Card SET unique_id ='{1}' WHERE sn ={0};</span><br><br>".format(sn, qid)
		print "<span><a href='home_page.py'>Go back home</a></span>"
		db.commit()
		db.close()
	except mysql.connector.Error as err:
		print "<span style='color: red'>ERROR</span><br>"
		print err
#		print("<h3>Serial number already exists!</h3>")

def add_note(sn, note):
#	note = MySQLdb.escape_string(note)

	try:
		db = connect(1)
		cur = db.cursor()
		
		# The following method escapes characters correctly:
		cmd = "INSERT INTO Card_Notes (sn, note, date_time) VALUES (%s, %s, %s)"
		values = (sn, note, time.strftime("%d/%m/%Y %I:%M:%S"))
		cur.execute(cmd, values)
#		cur.execute("INSERT Card_Notes SET sn={0}, note='{1}', date_time='{2}';".format(sn, note, time.strftime("%d/%m/%Y %I:%M:%S")))
#		print "<span style='color: green'>SUCCESS:</span><br>"
#		print "<span><a href='home_page.py'>Go back home</a></span>"
		db.commit()
		db.close()
		return True
	except mysql.connector.Error as err:
		print "<span style='color: red'>ERROR</span><br>"
		print err
		print "<br><br>"
		print note
		return False
#		print("<h3>Serial number already exists!</h3>")

