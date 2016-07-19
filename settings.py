# IMPORTS:
import cgi
# :IMPORTS

# VARIABLES:
db_default = "hf_qie_2016"
archive_path = "/var/www/html/ePorridge_archives"
# :VARIABLES

# FUNCTIONS:
def get_db():
	db = db_default
	form = cgi.FieldStorage()
	db_url = form.getvalue('db')
	if db_url:
		db = db_url
	return db

def get_attachment_path_base(db):
	return archive_path + "/" + db

def get_attachment_path(db, test_id, attach_id):
	return "{0}/{1}/{2}".format(get_attachment_path_base(db), test_id, attach_id)
# :FUNCTIONS
