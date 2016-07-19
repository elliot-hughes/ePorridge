# IMPORTS:
import cgi
import mysql.connector
# :IMPORTS

# VARIABLES:
db_default = "hf_qie_2016"
# :VARIABLES

# FUNCTIONS
def connect(write, db=db_default):
	# Connect to the DB:
	if (write):
		connection = mysql.connector.connect(user='Inserter', password='hcalInserter', database=db)
	else:
		connection = mysql.connector.connect(user='ReadUser', password='hcalReader', database=db)
	
	# Return stuff:
	connection.name = db
	return connection
# :FUNCTIONS
