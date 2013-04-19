import urllib2
import urlparse
import os
import sys
import time

SITE = "http://www.studionyc.com/v2" 
#SITE = "http://thestudio.codetodesign.com/rc2"

CACHE_DIR = "cache"

USE_CACHE = False
#USE_CACHE = True

MOVIES1_PREFIX = "../phil_assets"
PHIL_PREFIX = "../phil_assets"
MOVIES2_PREFIX = "../videos"
VIDEOS_PREFIX = "../videos"
POSTERS_PREFIX = "../posters"
CAPTIONS_PREFIX = "../captions"
CAPTIONS2_PREFIX = "../Illustrator Captions V2"
CONTENT_620_PREFIX = "../content_6_20_2012"
CONTENT_625_PREFIX = "../content_6_25_2012"
CONTENT_76_PREFIX = "../content_7_6_2012"
GEORGE_PREFIX = "../george_assets"

def site_replace(path):
	str = path.replace("SITE",SITE)
	return str

def path_replace(fpath):
        fpath = fpath.replace("PHIL",PHIL_PREFIX)
        fpath = fpath.replace("MOVIES1",MOVIES1_PREFIX)
        fpath = fpath.replace("MOVIES2",MOVIES2_PREFIX)
        fpath = fpath.replace("VIDEOS",VIDEOS_PREFIX)
        fpath = fpath.replace("VPOSTERS",POSTERS_PREFIX)
        fpath = fpath.replace("CAPTIONS",CAPTIONS_PREFIX)
        fpath = fpath.replace("CAPS2",CAPTIONS2_PREFIX)
	fpath = fpath.replace("CONTENT620", CONTENT_620_PREFIX )
	fpath = fpath.replace("CONTENT625", CONTENT_625_PREFIX )
	fpath = fpath.replace("CONTENT76", CONTENT_76_PREFIX )
	fpath = fpath.replace("GEORGE", GEORGE_PREFIX )
	fpath = fpath.replace(" ","%20")
	return fpath

def create_path( path ):
	str = path.replace(" ","%20")
	return str

def emit_line(str):
	return "%s\n" % str

def get_id(base,ids):
	tryname = base
	counter = 0
	while (True):
		if not (tryname in ids):
			return tryname
		else:
			print "ERROR: Cannot repeat id!", tryname, ids
			sys.exit(1)
		counter += 1
		tryname = "%s_%d" % (base,counter)


def get_title( filename ):

	bname = os.path.basename( filename ).split(".")[0]
	print "get title->", bname
		
	titlepath = "SEO/title/" + bname
	if ( os.path.exists( titlepath ) ):
		f = open( titlepath, 'r')
		contents = f.read()
		f.close()
		return contents.strip()
	else:
		return "TheStudio"

def get_description( filename ):

        bname = os.path.basename( filename ).split(".")[0]
        print "get description->", bname

        dpath = "SEO/description/" + bname
        if ( os.path.exists( dpath ) ):
                f = open( dpath, 'r')
                contents = f.read()
                f.close()
                return contents.strip()
        else:
                return "TheStudio"

def get_keywords( filename ):
        bname = os.path.basename( filename ).split(".")[0]
        print "get keywords->", bname
        dpath = "SEO/keywords/" + bname
        if ( os.path.exists( dpath ) ):
                f = open( dpath, 'r')
                contents = f.read()
                f.close()
                return contents.strip()
        else:
                return "design"

def get_analytics( ):
	cfile = "google/code.txt"
	if ( os.path.exists( cfile ) ):
		print "file exists!",cfile
		f = open(cfile,'r')
		contents = f.read()
		f.close()
		return contents.strip()
	else:
		return ""

def gen_page( filename, style, content, head_script, load_script ):

	title = get_title( filename )

	description = get_description( filename )
	
	keywords = get_keywords( filename )

	analytics = get_analytics()
	#print analytics

	load_script = "" + load_script

	f = open(filename,'w')
	loader = "function docload () { %s; } \n\n window.onload=docload;" % load_script
	f.write('<!DOCTYPE html >\n')  #"-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">')
	fmt = '<html xmlns="http://www.w3.org/1999/xhtml" >\n<head><title>%s</title>' + \
		"<meta name=\"description=\" content=\"%s\">" + \
		"<meta name=\"keywords=\" content=\"%s\">" + \
		'<meta http-equiv=\"content-type\" content=\"text/html;charset=utf-8\" />' + \
		"<style type=\"text/css\" >%s</style>\n%s</head>\n" + \
		'<body><div>\n' + \
		'<script type=\"text/javascript\" >\n%s\n%s\n</script>\n%s\n' + \
		'</div></body></html>'
	f.write(fmt % (title, description, keywords, style, analytics, head_script, loader, content) )
	f.flush()
	f.close()
	print "INFO: Wrote file->", filename

def parse_spreadsheet1 ( url, descr=None ):
	if descr:
		print "Common: Getting %s ->" % descr, url
	else:
		print "Common: Getting->", url
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

		print item
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
