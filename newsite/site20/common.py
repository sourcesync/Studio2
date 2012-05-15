import urllib2

def emit_line(str):
	return "%s\n" % str

def parse_spreadsheet1 ( url ):
	response = urllib2.urlopen( url )
        data = response.read()
        lines = data.split("\n")

	# assume first line is header info...
	colnames = lines[0].split(",")
	colnames = [ col.strip() for col in colnames ]
	print "COMMON: colnames->", colnames

	idx = range(len(colnames))
	colsdct = dict( zip( idx, colnames) )

	# get rest of lines...	
        items = [ line.split(",") for line in lines[1:] ]

	parsed = []
	for item in items:
		if item[0].strip()=="" or item[0][0]=="#":
			print "COMMON: empty or comment line->", item
			continue
		dct = dict( zip( colnames, item ) )
		parsed.append( dct )

	# lets assume the first item is the header...
	return parsed

def dct_join(items,join_key,key2=None):

	ndct = {}	
	for item in items:
		#print "item->", item, join_key

		key = item[join_key]
		val = item
		print "KV->", key, val
	
		results = []
		if ndct.has_key(key):
			results = ndct[key]
		results.append( val )
		ndct[key] = results

	if key2:
		nndct = {}
		for key in ndct.keys():
			items = ndct[key]
			nresults = dct_join( items, key2 )
			nndct[key] = nresults
		return nndct
	else:
		return ndct
