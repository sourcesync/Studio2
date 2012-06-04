#
# Configuration...
#

#MOVIES_DEF = "https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdHFxcjk0RlA3RkxlaWdxdmIyZWJlM1E&output=csv"

MOVIES_DEFS = { "home": "https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdGIwRUFBYWVabjN3amhvc2dXVTZDQWc&output=csv" }

MOVIES1_PREFIX = "../phil_assets"
MOVIES2_PREFIX = "../movies"

#
# Library...
#
import common
import os

import gen_images

def get_dct(pagekeys=None):
	if pagekeys==None:
		pagekeys = MOVIES_DEFS.keys()
	newdct = {}
	for code in pagekeys:
		if not MOVIES_DEFS.has_key(code): continue
		items = common.parse_spreadsheet1( MOVIES_DEFS[code] )
		dct = common.dct_join( items,'name')
		for ky in dct.keys():
			newdct[ky] = dct[ky]
	return newdct

def get_item_path( name, movies_dct ):
	item_def = movies_dct[name][0]
	path = item_def['path']
        fname = item_def['filename']
        fpath = os.path.join(path,fname)
        fpath = fpath.replace("MOVIES1",MOVIES1_PREFIX)
        fpath = fpath.replace("MOVIES2",MOVIES2_PREFIX)
	return fpath
	

def expand_item( accum_ids, asset_def, images_dct, movies_dct ):

	asset_name = asset_def["asset_name"]
	item_def = movies_dct[asset_name][0]

	print "ITEMDEF->", item_def
	
	htmlid = common.get_id( asset_name, accum_ids )
	accum_ids.append(htmlid)

	poster_path = ""
	if item_def["poster"].strip()!="":
		poster = item_def["poster"].strip()
		poster_path = gen_images.get_item_path( poster, images_dct )

	movie_path = get_item_path( asset_name, movies_dct )
	x = asset_def['x']
	y = asset_def['y']

	style  = ""
	#style  = common.emit_line( "<style>" )
	style += common.emit_line( "#%s {" % htmlid )
	style += common.emit_line( "position: absolute;")
	style += common.emit_line( "left: %dpx;" % int(x) )
	style += common.emit_line( "top: %dpx;" % int(y) )
	style += common.emit_line( "}" )
	#style += common.emit_line( "</style>")

	if poster_path == "":	
		content = common.emit_line( "<video controls id=%s ><source src=\"%s\" /></video>" % (htmlid, movie_path) )
	else:	
		content = common.emit_line( "<video controls id=%s poster=\"%s\" ><source src=\"%s\" /></video>" % (htmlid, poster_path, movie_path) )
	
	return [ style, content ]

if __name__ == "__main__":
	dct = get_dct()
	print dct
