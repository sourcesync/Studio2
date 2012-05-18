#
# Configuration...
#

MOVIES_PANEL_DEF = "https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdHpERzFkdWxHMGpobXAzMHp3dkVNWkE&output=csv"

MOVIES1_PREFIX = "../phil_assets"
MOVIES2_PREFIX = "../movies"

#
# Library...
#
import common
import os

def get_dct():
	items = common.parse_spreadsheet1( MOVIES_PANEL_DEF )
	dct = common.dct_join( items,'name')
	return dct

def get_item_path( name, movies_dct ):
	item_def = movies_dct[name][0]
	path = item_def['path']
        fname = item_def['filename']
        fpath = os.path.join(path,fname)
        fpath = fpath.replace("MOVIES1",MOVIES1_PREFIX)
        fpath = fpath.replace("MOVIES2",MOVIES2_PREFIX)
	return fpath
	

def expand_item( asset_def, movies_dct, images_dct ):
	asset_name = asset_def["asset_name"]
	item_def = movies_dct[asset_name][0]

	htmlid = asset_name

	poster_path = ""
	if item_def["poster"].strip()!="":
		poster_path = gen_images.get_item_path( poster )

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
