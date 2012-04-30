
import urllib2

def parse_spreadsheet1 ( url ):
	response = urllib2.urlopen( url )
        data = response.read()
        lines = data.split("\n")

	# assume first line is header info...
	colnames = lines[0].split(",")
	colnames = [ col.strip() for col in colnames ]
	print "colnames->", colnames

	idx = range(len(colnames))
	colsdct = dict( zip( idx, colnames) )

	# get rest of lines...	
        items = [ line.split(",") for line in lines[1:] ]

	parsed = []
	for item in items:
		dct = dict( zip( colnames, item ) )
		parsed.append( dct )

	return parsed
