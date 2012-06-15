#
#
# Configuration...
#

IMAGES_DEF = "https://docs.google.com/spreadsheet/pub?key=0AuRz1oxD7nNEdFd0ZV81SS1yZmZqQnpGdVBUeTlvVEE&output=csv"

MOVIES1_PREFIX = "../phil_assets"
MOVIES2_PREFIX = "../movies"


#
# Library...
#
import common
import os

def expand_item( asset_def, images_dct, onclick):
        print "asset_def->", asset_def
        asset_name = asset_def["asset_name"]
        item_def = images_dct[asset_name][0]
        print "item_def->", item_def

        htmlid = asset_name

        image_path = get_item_path( asset_name, images_dct )
        x = asset_def['x']
        y = asset_def['y']

        style  = common.emit_line( "<style>" )
        style += common.emit_line( "#%s {" % htmlid )
        style += common.emit_line( "position: absolute;")
        style += common.emit_line( "left: %dpx;" % int(x) )
        style += common.emit_line( "top: %dpx;" % int(y) )
        style += common.emit_line( "}" )
        style += common.emit_line( "</style>")

	if onclick:
		content = common.emit_line( "<img id=%s src=\"%s\" onclick=\"%s\" >" % (htmlid,image_path, onclick) )
	else:
		content = common.emit_line( "<img id=%s src=\"%s\" >" % (htmlid,image_path ) )
		
        return [ style, content ]

def get_item_path( name, images_dct ):
        item_def = images_dct[name][0]
        path = item_def['path']
        fname = item_def['filename']
        fpath = os.path.join(path,fname)
        fpath = fpath.replace("MOVIES1",MOVIES1_PREFIX)
        fpath = fpath.replace("MOVIES2",MOVIES2_PREFIX)
        return fpath

def get_dct():
	items = common.parse_spreadsheet1( IMAGES_DEF )
	dct = common.dct_join( items,'name')
	return dct

if __name__ == "__main__":
	dct = get_dct()
	print dct
