#
# Configuration...
#

#MOVIES_DEF = "https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdHFxcjk0RlA3RkxlaWdxdmIyZWJlM1E&output=csv"

MOVIES_DEFS = { "home": "https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdGIwRUFBYWVabjN3amhvc2dXVTZDQWc&output=csv", \
		"partners":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdHpsQWhEMi02UDJBeEl1S09uLTYxeEE&output=csv", \
		"animation_gallery":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdHhXaDVyU3k0c1YtTXZ0Z0RJRG5wZ1E&output=csv",\
		"motiondesign_gallery":"https://docs.google.com/spreadsheet/pub?key=0AvPzUVdJ7YGedHYzLUxpQ2M5X0FaakFvZmVwSEcwQnc&output=csv", \
		"previs":"https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdFB5cFJiaEhIaF9lY0Q0cVg5Njl0clE&output=csv", \
		"interactive":"https://docs.google.com/spreadsheet/pub?key=0AvPzUVdJ7YGedE5xOGE0SlFwaWFmZS1DWnFPSWdsQ3c&output=csv" }

MOVIES1_PREFIX = "../phil_assets"
PHIL_PREFIX = "../phil_assets"
MOVIES2_PREFIX = "../videos"

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
		items = common.parse_spreadsheet1( MOVIES_DEFS[code], "movies %s" % code )
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
        fpath = fpath.replace("PHIL",PHIL_PREFIX)
	return fpath
	

def expand_item( accum_ids, asset_def, images_dct, movies_dct ):

	asset_name = asset_def["asset_name"]
	item_def = movies_dct[asset_name][0]
	
	htmlid = common.get_id( asset_name, accum_ids )
	accum_ids.append(htmlid)

	poster_path = ""
	if item_def["poster"].strip()!="":
		poster = item_def["poster"].strip()
		poster_path = gen_images.get_item_path( poster, images_dct )

	movie_path = get_item_path( asset_name, movies_dct )
	x = asset_def['x']
	y = asset_def['y']
	z = asset_def['z']

	style  = ""
	#style  = common.emit_line( "<style>" )
	style += common.emit_line( "#%s {" % htmlid )
	style += common.emit_line( "position: absolute;")
	style += common.emit_line( "left: %dpx;" % int(x) )
	style += common.emit_line( "top: %dpx;" % int(y) )
	style += common.emit_line( "z-index: %d;" % int(z) )
	style += common.emit_line( "}" )
	#style += common.emit_line( "</style>")

	if poster_path == "":	
		content = common.emit_line( "<video controls id=%s ><source src=\"%s\" />CANNOT LOAD</video>" % (htmlid, movie_path) )
	else:	
		content = common.emit_line( "<video controls id=%s poster=\"%s\" ><source src=\"%s\" /></video>" % (htmlid, poster_path, movie_path) )

	scriptlet_dct = {}
	scriptlet_dct['on'] = "document.getElementById('%s').style.visibility='visible';" % htmlid
	scriptlet_dct['off'] = "document.getElementById('%s').style.visibility='hidden';" % htmlid
	scriptlet_dct['init'] = "document.getElementById('%s').style.visibility='visible';" % htmlid
	
	return [ style, content, scriptlet_dct ]

if __name__ == "__main__":
	dct = get_dct()
	print dct
