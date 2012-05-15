
ARTISTS_SUBPAGES_URL = "https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdEQ0djkyTGF0V01Rb2pJQW84MFlNSFE&output=csv"

ASSET_PREFIX = "../../phil_assets"

import urllib2
import common
import copy
import os

def get_items():
	# get a list of items ( each a dct )...
	parsed = common.parse_spreadsheet1( ARTISTS_SUBPAGES_URL )

	# explode items as necessary...
	exploded = []
	for item in parsed:
		if item['name'] == 'AUTO':
			expr = item['file'].split("+")
			print expr
			reg = expr[0]
			st = int(expr[1])
			end = int(expr[2])
			prev = False
			prevDct = None
			for i in range(st,end+1):
				print i
				dct = copy.deepcopy( item )
				dct['file'] = reg % i
				dct['name'] = dct['file'].split('.')[0]
				if prevDct: prevDct['alink'] = dct['name']
				dct['blink'] = prev
				dct['alink'] = False
				prevDct = dct
				prev = dct['name']
				exploded.append( dct )
		else:
			exploded.append(item)

	return exploded	

def gen_pages( items ):

	for i in range(len(items)):
		item = items[i]
		thispage = item['name'] + ".html"
		nextpage = "#"
		if (i+1<len(items)):
			nextitem = items[i+1]
			nextpage = nextitem['name'] + ".html"
	
		# produce the html string...	
		html =  "<html>"
		html += "<body>"
		path = os.path.join( ASSET_PREFIX, item['path'] )	
		path = os.path.join( path, item['file'] )
		html += "<a href='" + nextpage + "'><img src='" + path + "' /></a>"
		html += "</body>"
		html += "</html>"

		# write the file...
		fpath = os.path.join("artists", thispage )
		f = open(fpath,'w')
		print "writing file->", fpath
		f.write(html)
		f.flush()
		f.close()
		

if __name__=="__main__":
	items = get_items()	
	print items

	gen_pages( items )


		
