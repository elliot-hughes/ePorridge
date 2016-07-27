#!/usr/bin/python

import cgi
import cgitb
cgitb.enable()

import base, settings
from connect import connect

def main():
	form = cgi.FieldStorage()
	infoName = cgi.escape(form.getvalue("characteristic","no name found"))
	descShort = cgi.escape(form.getvalue("descShort","no description found"))
	descLong = cgi.escape(form.getvalue("descLong","no description found"))
	db = settings.get_db()
	
	
	con = connect(True,db)
	cur = con.cursor(buffered=True)

	cur.execute("INSERT INTO Card_Info_Types (Info_Name,Info_Desc_Short,Info_Desc_Long) VALUES ('{0}','{1}','{2}');".format(infoName,descShort,descLong))

	con.commit()
	con.close()

	base.begin()
	base.header_redirect('erudition.py?db={0}#cardInfoTable'.format(db))
	base.bottom()

# MAIN:
if __name__ == "__main__":
        main()
# :MAIN
