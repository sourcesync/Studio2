import urllib2
import urlparse
import os

CACHE_DIR = "cache"

USE_CACHE = False
#USE_CACHE = True

def emit_line(str):
	return "%s\n" % str

def get_id(base,ids):
	tryname = base
	counter = 0
	while (True):
		if not (tryname in ids):
			return tryname
		counter += 1
		tryname = "%s_%d" % (base,counter)
		

def gen_page( filename, style, content ):
	f = open(filename,'w')
	f.write("<html><body>\n%s\n%s</body></html>" % (style, content))
	f.flush()
	f.close()
	print "INFO: Wrote file->", filename

def parse_spreadsheet1 ( url ):
	print "Getting->", url
	parts = urlparse.urlparse(url)
	cache_name = parts.query.replace("=","_")
	cache_name = cache_name.replace("&","_")
	cache_file = os.path.join( CACHE_DIR, cache_name )
	if os.path.exists( cache_file ) and USE_CACHE:
		f = open( cache_file, 'r')
		data = f.read()
		f.close()
	else: 
		response = urllib2.urlopen( url )
        	data = response.read()
		f = open( cache_file, 'w')
		f.write( data )
		f.flush()
		f.close()

        lines = data.split("\n")

	# assume first line is header info...
	colnames = lines[0].split(",")
	colnames = [ col.strip() for col in colnames ]

	idx = range(len(colnames))
	colsdct = dict( zip( idx, colnames) )

	# get rest of lines...	
        items = [ line.split(",") for line in lines[1:] ]

	parsed = []
	for item in items:
		if item[0].strip()=="" or item[0][0]=="#":
			continue
		dct = dict( zip( colnames, item ) )
		parsed.append( dct )

	# lets assume the first item is the header...
	return parsed

def dct_join(items,join_key,key2=None):

	ndct = {}	
	for item in items:

		key = item[join_key]
		if (key==""):
			continue
		val = item
	
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
