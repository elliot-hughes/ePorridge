import re

def begin():
	# Print preamble:
	print "Content-type: text/html"
	print ""
	print "<!DOCTYPE HTML>"
	print "<html>"

def header(title='ePortage'):
	print '''<head>
	<link rel="stylesheet" href="/ePorridge/css/bootstrap.min.css">
	<link rel="stylesheet" href="/ePorridge/css/style.css">
	<title>{0}</title>
</head>'''.format(title)


def header_redirect(url, seconds=0):
	print '<head><link rel="stylesheet" href="/ePorridge/css/bootstrap.min.css">'
	print '<link rel="stylesheet" href="/ePorridge/css/style.css">'
	print '<meta http-equiv="refresh" content="{1}; url={0}"></head>'.format(url, seconds)

def header_redirect_module_test(card_id, serial_num, test_type):
	print '''<head>
	<meta http-equiv="refresh" content="0; url=module.py?card_id={0}&serial_num={1}#test-{2}">
</head>'''.format(card_id, serial_num, test_type)

def header_redirect_module_notes(card_id, serial_num):
	print '''<head>
	<meta http-equiv="refresh" content="0; url=module.py?card_id={0}&serial_num={1}#notes">
</head>'''.format(card_id, serial_num)

def top(db, title="HCAL Phase I Upgrade", subtitle="HF Frontend Quality Assurance Testing"):
	subtitle = "database = {0}".format(db)
	print '''<body class="custom-body">
	<div class="center-panel">
		<div style="height:300px;">
			<!--<div class="container">-->
				<div class="row">
					<!--<div align=left><img src="/us-cms.png" class="img-responsive"></div>-->
					<div align=center>
						<br>
						<h1 class="title">{0}</h1>
						<h2 class="title" style='color: red'>{1}</h2>
						<br>
					</div>
				</div>
			<!--</div>-->
			<div class="row" align=center>
				<div class="col-md-12">
					<a href="home.py?db={2}"><button class="home">Home</button></a>
					<a href="summary.py?db={2}"><button>Summary</button></a>
					<a href="testers.py?db={2}"><button>Testers</button></a>
					<a href="erudition.py?db={2}"><button>Setup</button></a>
					<a href="index.html"><button>Pick a different database</button></a>
				</div>
				<br><br><br>
			</div>
		</div>'''.format(title, subtitle, db)
#<a href="fwVersion.py"><button>F/W versions</button></a>

def bottom():
	print "\t</div>"
	print '\t<br><br><div id="footer-container"><center><span class="footer">Powered by <a href="https://github.com/elliot-hughes/ePorridge">ePorridge</a>.</span><br><a href="https://github.com/elliot-hughes/ePorridge"><img src="resources/logo.png" width="100px"></a></center></div><br>'
	print "</body>"
	print "</html>"


def cleanCGInumber(cgitext):
	if not cgitext:
		return 0
	return int(re.sub('[^0-9]', '', cgitext))



def error(db, msg, redirect="", redirect_time=1):
	begin()
	top(db)
	if redirect:
		header_redirect(redirect, redirect_time)
	else:
		header()
	print '<center><h3 style="color:red"><i>{0}</i></h3><br><h4 style="font-weight:bold"><a href="javascript:history.back()" style="text-decoration:none; color:red;">&larr; Go back</a></h4></center>'.format(msg)
	bottom()
